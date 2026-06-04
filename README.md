# Todo App Backend

## Overview
A secure Todo Backend API built using **FastAPI** and **PostgreSQL**. This application features user authentication using JWTs, refresh token rotation, token versioning for secure logouts/password changes, and complete CRUD operations for tasks and users.

The project is configured for deployment on **Vercel** serverless functions.

🚀 **Live API URL**: [https://todo-app-backend-plum.vercel.app](https://todo-app-backend-plum.vercel.app)  
📖 **Interactive Swagger Docs**: [https://todo-app-backend-plum.vercel.app/docs](https://todo-app-backend-plum.vercel.app/docs)

---

## 🚀 Features

### 🔒 Security & Authentication
- **JWT Authentication**: Custom middleware to secure endpoints using JWT bearer tokens.
- **Refresh Token Rotation**: Long-lived refresh tokens securely stored as SHA-256 hashes in the database, allowing users to request new short-lived access tokens without re-authenticating.
- **Session Revocation via Token Versioning**: A security mechanism where password changes, logouts, or key user operations increment a database `token_version`. If a decoded access token has an outdated version, it is rejected.
- **Password Hashing**: Secure password hashing using `bcrypt`.

### 📝 User Management (CRUD)
- **Sign Up**: Register new users with validated details (name, email, secure password).
- **Log In**: Authenticate users and issue JWT Access and Refresh tokens.
- **Log Out**: Instantly invalidates the current session by revoking the refresh token and incrementing the token version.
- **Change Password**: Safely update passwords and revoke all other active sessions across devices.
- **Delete Account**: Permanently deletes a user's account along with all their associated tasks in a cascading SQL operation.

### 📋 Todo Task Management (CRUD)
- **Create Task**: Create new todos with custom title, optional description, and priority level.
- **Read Tasks**: Retrieve all tasks associated exclusively with the authenticated user.
- **Update Task**: Dynamically update task details (title, description, completion status, or priority level).
- **Delete Task**: Permanently remove a specific task.
- **Priority Classification**: Tasks support priority levels (`low`, `medium`, `high`) powered by PostgreSQL custom ENUM types.

---

## 🛠️ Stack & Technologies

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Database Driver & Pool**: [Psycopg2-binary](https://initd.org/psycopg/) (using `SimpleConnectionPool`)
- **Authentication**: [PyJWT](https://pyjwt.readthedocs.io/)
- **Hashing**: [Bcrypt](https://pypi.org/project/bcrypt/) & [Hashlib](https://docs.python.org/3/library/hashlib.html) (SHA-256)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/) & [Email-Validator](https://pypi.org/project/email-validator/)
- **Configuration Management**: [Python-Decouple](https://pypi.org/project/python-decouple/)
- **Deployment Platform**: [Vercel](https://vercel.com/) (Serverless Python runtime)

---

## 📂 Project Structure

The project adheres to a clean, decoupled **Layered Architecture (Router-Service-Repository)**:

```text
todo_proj/
├── app/
│   ├── core/
│   │   └── database.py        # Connection pooling and database connection config
│   ├── repository/
│   │   ├── auth_repo.py       # SQL database operations for authentication
│   │   ├── tasks_repo.py      # SQL database operations for tasks
│   │   └── user_repo.py       # SQL database operations for user data
│   ├── routers/
│   │   ├── auth.py            # Routes for signup, login, refresh, logout, password change
│   │   ├── routes.py          # Master route registration config
│   │   └── task.py            # Protected routes for task CRUD operations
│   ├── schema/
│   │   ├── auth.py            # Pydantic schemas for auth requests/responses
│   │   ├── task.py            # Pydantic schemas for todo tasks
│   │   └── user.py            # Pydantic schema for standard user profile
│   ├── service/
│   │   ├── auth_service.py    # Main auth & session logic
│   │   ├── hash_service.py    # Wrapper for password hashing and string verification
│   │   ├── jwt_service.py     # Access/Refresh token creation and verification
│   │   └── tasks_service.py   # Business logic for task management
│   └── util/
│       ├── init_db.py         # DB startup script (Table creation & custom ENUM creation)
│       └── protect_route.py   # FastAPI Dependency injection for route protection
├── main.py                    # Application entry point & lifespan events
├── requirements.txt           # Python project dependencies
├── vercel.json                # Vercel deployment configuration
└── .env                       # Local environment variables configuration (Ignored by Git)
```

---

## 📡 API Endpoints

### Authentication `/auth`
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **POST** | `/auth/signup` | Create a new account | No |
| **POST** | `/auth/login` | Authenticate and get JWT & Refresh tokens | No |
| **POST** | `/auth/refresh-token` | Generate a new access token using a refresh token | No |
| **POST** | `/auth/change-password` | Update account password and invalidate active tokens | **Yes** |
| **GET** | `/auth/logout` | Revoke tokens and log out of the current session | **Yes** |
| **GET** | `/auth/delete-account` | Delete user profile and all associated tasks | **Yes** |

### Tasks `/todo`
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **POST** | `/todo/create-task` | Create a new task | **Yes** |
| **GET** | `/todo/get-tasks` | Get all tasks belonging to the current user | **Yes** |
| **POST** | `/todo/{task_id}/update-task` | Modify attributes of a specific task | **Yes** |
| **GET** | `/todo/{task_id}/delete-task` | Delete a specific task | **Yes** |

---

## 💡 Key Takeaways & What I Learned

Building this backend provided key insights into developing secure, structured APIs:

1. **Advanced JWT Session Control**:
   - I learned that simple stateless JWTs cannot be revoked easily. By implementing a **Token Versioning Pattern** (checking the database token version against the decoded JWT claim), I built a system that allows instant server-side token invalidation on demand (e.g., for logout and password changes) without losing the performance benefits of JWTs.
2. **Refresh Token Rotation**:
   - Access tokens should be short-lived to minimize exposure if compromised. I implemented long-lived, SHA-256 hashed refresh tokens stored in the database to securely renew access tokens without interrupting the user experience.
3. **Database Security & Decoupling**:
   - I utilized **bcrypt** for secure one-way salted password hashing, making user password storage resilient against brute-force attacks.
   - I separated SQL access logic into a **Repository Pattern** and business logic into a **Service Pattern**, making the codebase highly structured and clean.
4. **Efficient Database Operations**:
   - Rather than spinning up a new database connection for every API request, I utilized a `SimpleConnectionPool` to reuse connections, which optimizes backend performance.
   - I used custom PostgreSQL ENUM types (`priority_level`) to guarantee database-level validation of task priority levels.
5. **Serverless PostgreSQL Deployments**:
   - Deploying Python to Vercel requires configuring `vercel.json` and adapting to stateless environments. I learned how to handle database connection configurations under a serverless model, including cleaning database connection URIs to prune deployment-specific query parameters.

---

## ⚙️ Local Setup Guide

### 1. Prerequisites
- Python 3.9+ installed.
- PostgreSQL database running locally or hosted online (e.g., Supabase, Neon).

### 2. Clone the Repository
```bash
git clone <repository-url>
cd todo_proj
```

### 3. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://your_db_username:your_db_password@your_db_host:5432/your_db_name
JWT_SECRET=your_super_secret_jwt_signing_key_here
JWT_ALGORITHM=HS256
```

### 6. Run the Application locally
```bash
uvicorn main:app --reload
```
The server will start at `http://127.0.0.1:8000`. You can access the interactive API docs at `http://127.0.0.1:8000/docs`.

---

## ☁️ Deployment on Vercel

This application is fully compatible with **Vercel** serverless functions.

> [!IMPORTANT]
> **Database Configuration:** Because Vercel operates in a stateless serverless environment, a local PostgreSQL database (`localhost`) will not work. You must use a remote PostgreSQL instance. You can either create a database directly in Vercel (e.g., using Vercel Postgres) or use an external provider like Supabase or Neon, and set the `DATABASE_URL` environment variable to point to it.

1. Ensure the `vercel.json` file is in the root directory:
   ```json
   {
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```
2. Push the code to your GitHub repository.
3. Go to the [Vercel Dashboard](https://vercel.com/) and import the linked GitHub repository.
4. Add the required environment variables (`DATABASE_URL`, `JWT_SECRET`, `JWT_ALGORITHM`) under **Settings > Environment Variables** in the Vercel Dashboard.
5. Click **Deploy**. Vercel will automatically build and serve the application, triggering new deployments on every subsequent git push.
