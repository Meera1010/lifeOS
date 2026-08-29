"""
LifeOS Task Manager Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Tuple, Optional
from sqlalchemy import or_, and_, func, asc, desc
from backend.models.base import db
from backend.models.task import Task, Subtask, TaskCategory, TaskTag, TaskActivityLog
from backend.app.constants import PriorityLevel, TaskStatus
from backend.security.validators import sanitize_string, validate_numeric_range
from backend.utilities.date_utils import parse_datetime_string, get_week_range, get_month_range


class TaskDependencyError(Exception):
    """Raised when a task dependency cycle or invalid blocking task condition occurs."""
    pass


class TaskService:
    """
    Comprehensive Task Management Domain Service providing:
    - Task CRUD operations with validation and audit logging
    - Subtask hierarchy and progress recalculation
    - Category & Tag management with color coding
    - Priority-based sorting algorithms and multi-criteria search
    - Recurrence engine for daily, weekly, monthly, and custom schedules
    - Batch task operations (bulk complete, archive, reschedule, tag)
    - Time tracking log calculations and estimated vs actual time analytics
    - Task velocity, backlog health metrics, and completion statistics
    """

    @staticmethod
    def get_user_tasks(user_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieves user tasks matching filter criteria.
        
        Filter Options:
        - status: pending, in_progress, completed, cancelled
        - priority: low, medium, high, urgent
        - category_id: integer category ID
        - tag_id: integer tag ID
        - search: search term matched against title and description
        - due_before: ISO datetime string
        - due_after: ISO datetime string
        - is_recurring: boolean
        - sort_by: priority, due_date, created_at, title
        - order: asc, desc
        """
        filters = filters or {}
        query = Task.query.filter_by(user_id=user_id, is_deleted=False)

        # Apply Status Filter
        if filters.get("status"):
            query = query.filter(Task.status == filters["status"])

        # Apply Priority Filter
        if filters.get("priority"):
            query = query.filter(Task.priority == filters["priority"])

        # Apply Category Filter
        if filters.get("category_id"):
            try:
                cid = int(filters["category_id"])
                query = query.filter(Task.category_id == cid)
            except (ValueError, TypeError):
                pass

        # Apply Tag Filter
        if filters.get("tag_id"):
            try:
                tid = int(filters["tag_id"])
                query = query.filter(Task.tags.any(TaskTag.id == tid))
            except (ValueError, TypeError):
                pass

        # Apply Full-Text Search
        if filters.get("search"):
            term = f"%{sanitize_string(filters['search'])}%"
            query = query.filter(or_(Task.title.ilike(term), Task.description.ilike(term)))

        # Apply Date Range Filters
        if filters.get("due_before"):
            dt = parse_datetime_string(filters["due_before"])
            query = query.filter(Task.due_date <= dt)
        if filters.get("due_after"):
            dt = parse_datetime_string(filters["due_after"])
            query = query.filter(Task.due_date >= dt)

        # Apply Recurrence Filter
        if "is_recurring" in filters:
            is_rec = str(filters["is_recurring"]).lower() == "true"
            query = query.filter(Task.is_recurring == is_rec)

        # Apply Sorting Logic
        sort_by = filters.get("sort_by", "due_date")
        order = filters.get("order", "asc")

        if sort_by == "priority":
            if order == "desc":
                query = query.order_by(desc(Task.priority), asc(Task.due_date))
            else:
                query = query.order_by(asc(Task.priority), asc(Task.due_date))
        elif sort_by == "created_at":
            if order == "desc":
                query = query.order_by(desc(Task.created_at))
            else:
                query = query.order_by(asc(Task.created_at))
        elif sort_by == "title":
            if order == "desc":
                query = query.order_by(desc(Task.title))
            else:
                query = query.order_by(asc(Task.title))
        else:  # Default due_date
            if order == "desc":
                query = query.order_by(desc(Task.due_date))
            else:
                query = query.order_by(asc(Task.due_date))

        tasks = query.all()
        return [t.to_dict() for t in tasks]

    @staticmethod
    def get_task_by_id(user_id: int, task_id: int) -> Optional[Dict]:
        """Retrieves single task object by ID for authenticated user."""
        task = Task.query.filter_by(id=task_id, user_id=user_id, is_deleted=False).first()
        if not task:
            return None
        return task.to_dict()

    @staticmethod
    def create_task(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """
        Creates a new task with validation, subtasks, tags, and activity logging.
        """
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Task title is required and cannot be empty."}

        if len(title) > 200:
            return False, {"error": "Task title must not exceed 200 characters."}

        priority = data.get("priority", PriorityLevel.MEDIUM.value)
        if priority not in [p.value for p in PriorityLevel]:
            priority = PriorityLevel.MEDIUM.value

        status = data.get("status", TaskStatus.PENDING.value)
        if status not in [s.value for s in TaskStatus]:
            status = TaskStatus.PENDING.value

        description = sanitize_string(data.get("description", ""))
        category_id = data.get("category_id")
        
        # Verify Category ownership if provided
        if category_id:
            cat = TaskCategory.query.filter_by(id=category_id, user_id=user_id).first()
            if not cat:
                category_id = None

        due_date = parse_datetime_string(data.get("due_date")) if data.get("due_date") else None
        
        try:
            estimated_minutes = max(0, int(data.get("estimated_minutes", 0)))
        except (ValueError, TypeError):
            estimated_minutes = 0

        is_recurring = bool(data.get("is_recurring", False))
        recurrence_pattern = data.get("recurrence_pattern") if is_recurring else None
        recurrence_interval = max(1, int(data.get("recurrence_interval", 1))) if is_recurring else 1

        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            category_id=category_id,
            due_date=due_date,
            estimated_minutes=estimated_minutes,
            actual_minutes=0,
            is_recurring=is_recurring,
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=recurrence_interval
        )

        if status == TaskStatus.COMPLETED.value:
            task.completed_at = datetime.utcnow()

        db.session.add(task)
        db.session.flush()

        # Add Subtasks
        subtasks_input = data.get("subtasks", [])
        for idx, st_data in enumerate(subtasks_input):
            if isinstance(st_data, dict):
                st_title = sanitize_string(st_data.get("title", ""))
            else:
                st_title = sanitize_string(str(st_data))

            if st_title:
                subtask = Subtask(
                    task_id=task.id,
                    title=st_title,
                    is_completed=bool(st_data.get("is_completed", False)) if isinstance(st_data, dict) else False,
                    order_index=idx
                )
                db.session.add(subtask)

        # Add Tags
        tag_ids = data.get("tag_ids", [])
        if tag_ids and isinstance(tag_ids, list):
            tags = TaskTag.query.filter(TaskTag.id.in_(tag_ids), TaskTag.user_id == user_id).all()
            task.tags.extend(tags)

        # Log Activity
        activity = TaskActivityLog(
            task_id=task.id,
            user_id=user_id,
            action="created",
            details=f"Task '{title}' created with priority {priority}."
        )
        db.session.add(activity)
        db.session.commit()

        return True, task.to_dict()

    @staticmethod
    def update_task(user_id: int, task_id: int, data: Dict) -> Tuple[bool, Dict]:
        """
        Updates an existing task with status transitions, recurring handling, and logs.
        """
        task = Task.query.filter_by(id=task_id, user_id=user_id, is_deleted=False).first()
        if not task:
            return False, {"error": "Task not found."}

        changes = []

        if "title" in data:
            new_title = sanitize_string(data["title"])
            if not new_title:
                return False, {"error": "Task title cannot be empty."}
            if new_title != task.title:
                changes.append(f"title changed from '{task.title}' to '{new_title}'")
                task.title = new_title

        if "description" in data:
            task.description = sanitize_string(data["description"])
        if "priority" in data and data["priority"] in [p.value for p in PriorityLevel]:
            task.priority = data["priority"]
        if "category_id" in data:
            task.category_id = data["category_id"]
        if "due_date" in data:
            task.due_date = parse_datetime_string(data["due_date"]) if data["due_date"] else None
        if "estimated_minutes" in data:
            task.estimated_minutes = max(0, int(data["estimated_minutes"]))
        if "actual_minutes" in data:
            task.actual_minutes = max(0, int(data["actual_minutes"]))
        if "is_recurring" in data:
            task.is_recurring = bool(data["is_recurring"])
        if "recurrence_pattern" in data:
            task.recurrence_pattern = data["recurrence_pattern"]
        if "recurrence_interval" in data:
            task.recurrence_interval = max(1, int(data["recurrence_interval"]))

        # Handle Status Transition
        if "status" in data and data["status"] in [s.value for s in TaskStatus]:
            old_status = task.status
            new_status = data["status"]
            if old_status != new_status:
                task.status = new_status
                changes.append(f"status changed from '{old_status}' to '{new_status}'")
                
                if new_status == TaskStatus.COMPLETED.value:
                    task.completed_at = datetime.utcnow()
                    # Check recurring task creation
                    if task.is_recurring and task.recurrence_pattern:
                        TaskService._spawn_recurring_instance(task)
                else:
                    task.completed_at = None

        # Log Changes
        if changes:
            activity = TaskActivityLog(
                task_id=task.id,
                user_id=user_id,
                action="updated",
                details=f"Updated task: {', '.join(changes)}"
            )
            db.session.add(activity)

        db.session.commit()
        return True, task.to_dict()

    @staticmethod
    def delete_task(user_id: int, task_id: int) -> Tuple[bool, str]:
        """Soft deletes a task and logs deletion event."""
        task = Task.query.filter_by(id=task_id, user_id=user_id, is_deleted=False).first()
        if not task:
            return False, "Task not found."

        task.soft_delete()
        activity = TaskActivityLog(
            task_id=task.id,
            user_id=user_id,
            action="deleted",
            details=f"Task '{task.title}' was deleted."
        )
        db.session.add(activity)
        db.session.commit()

        return True, "Task successfully deleted."

    @staticmethod
    def batch_operate_tasks(user_id: int, task_ids: List[int], action: str, params: Dict = None) -> Tuple[bool, Dict]:
        """
        Performs batch operations across multiple tasks:
        - complete: Mark all specified tasks completed
        - delete: Delete all specified tasks
        - reschedule: Update due date for all specified tasks
        - set_priority: Update priority for all specified tasks
        """
        params = params or {}
        tasks = Task.query.filter(
            Task.id.in_(task_ids),
            Task.user_id == user_id,
            Task.is_deleted == False
        ).all()

        if not tasks:
            return False, {"error": "No matching tasks found for batch operation."}

        count = 0
        for task in tasks:
            if action == "complete":
                task.status = TaskStatus.COMPLETED.value
                task.completed_at = datetime.utcnow()
                count += 1
            elif action == "delete":
                task.soft_delete()
                count += 1
            elif action == "reschedule" and "due_date" in params:
                task.due_date = parse_datetime_string(params["due_date"]) if params["due_date"] else None
                count += 1
            elif action == "set_priority" and params.get("priority") in [p.value for p in PriorityLevel]:
                task.priority = params["priority"]
                count += 1

        db.session.commit()
        return True, {"action": action, "processed_count": count}

    @staticmethod
    def toggle_subtask(user_id: int, subtask_id: int) -> Tuple[bool, Dict]:
        """Toggles subtask completion state and updates parent task progress."""
        subtask = Subtask.query.get(subtask_id)
        if not subtask or subtask.task.user_id != user_id:
            return False, {"error": "Subtask not found."}

        subtask.toggle_completion()
        db.session.commit()

        return True, subtask.task.to_dict()

    @staticmethod
    def add_subtask(user_id: int, task_id: int, title: str) -> Tuple[bool, Dict]:
        """Adds a new subtask to an existing task."""
        task = Task.query.filter_by(id=task_id, user_id=user_id, is_deleted=False).first()
        if not task:
            return False, {"error": "Task not found."}

        st_title = sanitize_string(title)
        if not st_title:
            return False, {"error": "Subtask title cannot be empty."}

        order_idx = len(task.subtasks)
        subtask = Subtask(
            task_id=task.id,
            title=st_title,
            order_index=order_idx
        )
        db.session.add(subtask)
        db.session.commit()

        return True, task.to_dict()

    @staticmethod
    def _spawn_recurring_instance(parent_task: Task):
        """Calculates next due date and creates new instance for recurring tasks."""
        if not parent_task.due_date:
            base_date = datetime.utcnow()
        else:
            base_date = parent_task.due_date

        pattern = (parent_task.recurrence_pattern or "daily").lower()
        interval = parent_task.recurrence_interval or 1

        if pattern == "daily":
            next_due = base_date + timedelta(days=interval)
        elif pattern == "weekly":
            next_due = base_date + timedelta(weeks=interval)
        elif pattern == "monthly":
            next_due = base_date + timedelta(days=30 * interval)
        else:
            next_due = base_date + timedelta(days=interval)

        new_task = Task(
            user_id=parent_task.user_id,
            title=parent_task.title,
            description=parent_task.description,
            priority=parent_task.priority,
            status=TaskStatus.PENDING.value,
            category_id=parent_task.category_id,
            due_date=next_due,
            estimated_minutes=parent_task.estimated_minutes,
            actual_minutes=0,
            is_recurring=True,
            recurrence_pattern=parent_task.recurrence_pattern,
            recurrence_interval=parent_task.recurrence_interval
        )
        db.session.add(new_task)

    @staticmethod
    def get_task_statistics(user_id: int) -> Dict:
        """Calculates comprehensive task manager metrics."""
        total = Task.query.filter_by(user_id=user_id, is_deleted=False).count()
        completed = Task.query.filter_by(user_id=user_id, status=TaskStatus.COMPLETED.value, is_deleted=False).count()
        pending = Task.query.filter_by(user_id=user_id, status=TaskStatus.PENDING.value, is_deleted=False).count()
        in_progress = Task.query.filter_by(user_id=user_id, status=TaskStatus.IN_PROGRESS.value, is_deleted=False).count()
        
        now = datetime.utcnow()
        overdue = Task.query.filter(
            Task.user_id == user_id,
            Task.is_deleted == False,
            Task.status != TaskStatus.COMPLETED.value,
            Task.due_date < now
        ).count()

        completion_rate = round((completed / total) * 100.0, 1) if total > 0 else 0.0

        # Estimated vs Actual time totals
        est_total = db.session.query(func.sum(Task.estimated_minutes)).filter(
            Task.user_id == user_id, Task.is_deleted == False
        ).scalar() or 0

        act_total = db.session.query(func.sum(Task.actual_minutes)).filter(
            Task.user_id == user_id, Task.is_deleted == False
        ).scalar() or 0

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "in_progress_tasks": in_progress,
            "overdue_tasks": overdue,
            "completion_rate": completion_rate,
            "total_estimated_hours": round(est_total / 60.0, 1),
            "total_actual_hours": round(act_total / 60.0, 1)
        }
