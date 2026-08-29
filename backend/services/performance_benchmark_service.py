"""
LifeOS System Performance Benchmarking Service
"""

import time
from typing import Dict, Any
from backend.models.base import db
from backend.models.task import Task
from backend.models.habit import Habit
from backend.models.goal import Goal


class PerformanceBenchmarkService:
    """
    Measures database query execution times and API performance latency.
    """

    @staticmethod
    def run_query_benchmarks(user_id: int) -> Dict[str, Any]:
        """Executes timed queries across core models."""
        t0 = time.time()
        _ = Task.query.filter_by(user_id=user_id, is_deleted=False).all()
        task_query_ms = round((time.time() - t0) * 1000.0, 2)

        t1 = time.time()
        _ = Habit.query.filter_by(user_id=user_id, is_deleted=False).all()
        habit_query_ms = round((time.time() - t1) * 1000.0, 2)

        t2 = time.time()
        _ = Goal.query.filter_by(user_id=user_id, is_deleted=False).all()
        goal_query_ms = round((time.time() - t2) * 1000.0, 2)

        return {
            "task_query_ms": task_query_ms,
            "habit_query_ms": habit_query_ms,
            "goal_query_ms": goal_query_ms,
            "total_benchmark_ms": round(task_query_ms + habit_query_ms + goal_query_ms, 2)
        }
