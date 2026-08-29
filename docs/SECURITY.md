# LifeOS — Security Architecture & Threat Mitigation

Security is integrated at every architectural tier of LifeOS.

## Security Controls Overview

1. **Password Protection & Hashing**
   - Passwords are encrypted using Werkzeug PBKDF2 with SHA-256 and salt. Plaintext passwords are never stored or logged.
   - Account lockout mechanism locks accounts for 15 minutes after 5 consecutive failed attempts.

2. **Authentication & Session Tokens**
   - JWT tokens signed with HS256 algorithm and 7-day expiration.
   - Fallback database session validation with active expiration timestamps.

3. **Role-Based Access Control (RBAC)**
   - Strict separation between `User` and `Admin` capabilities.
   - Admin routes guarded by `@require_admin` decorator.

4. **Input Validation & XSS Prevention**
   - HTML special character escaping on all string inputs.
   - Strict validation of email regex, username characters, and numeric bounds.

5. **SQL Injection Prevention**
   - Parameterized queries enforced via SQLAlchemy ORM.

6. **Audit Logging**
   - Comprehensive audit logging for all critical security actions (`USER_LOGIN`, `USER_REGISTERED`, `PASSWORD_CHANGED`, `ADMIN_DELETED_USER`).
