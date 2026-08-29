# LifeOS — Data Flow Diagrams & Request Lifecycle

This document describes the end-to-end data processing pipelines within **LifeOS**.

## 1. Authentication Data Flow

```
[ Client Form ] ---> ( POST /api/auth/login ) ---> [ AuthMiddleware / AuthService ]
                                                          |
                                            Validate Password (PBKDF2)
                                                          |
                                            Generate JWT Bearer Token
                                                          |
[ Client Store ] <--- ( Token + User JSON ) <-------------+
```

## 2. Dynamic Life Score Pipeline

```
[ Database ORM ] ---> ( Tasks, Habits, Goals, Finance, Learning, Focus Services )
                                      |
                     Compute 6 Pillar Sub-Scores (0-100%)
                                      |
                      Apply Pillar Weights (20/20/20/15/15/10)
                                      |
                     [ Composite Life Score & Insights ]
```
