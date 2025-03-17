# **TimeED**

Formerly known as **eTeach**, **TimeED** is a **time management web application** designed to help **teachers and students** organize their schedules, track progress, and boost productivity.

Built with **Flask (Server-Side Rendering)**, TimeED simplifies **session and group management** for educational purposes.

## **✨ Features**

### **For Teachers**

✅ **Create & Manage Groups** – Set up groups with descriptions and manage them easily.  
✅ **Schedule & Manage Sessions** – Plan, edit, or cancel sessions effortlessly.  
✅ **Track Attendance** – Stay updated on student attendance.

### **For Students**

✅ **View & Join Groups** – Track enrolled groups and discover new ones.  
✅ **Session Updates** – Receive reminders and cancellation alerts.  
✅ **Request Absence** – Notify teachers if you can't attend a session.

## **🛠️ Tech Stack**

-   **Backend:** Flask (Python)
-   **Frontend:** HTML, CSS, JavaScript (SSR)
-   **Database:** SQLite, extendable to PostgreSQL/MySQL

## **📦 Installation**

### 1️⃣ Clone the repository:

```bash
git clone git@github.com:DracoTato/TimeEd.git
cd TimeEd
```

### 2️⃣ Install dependencies (using [Poetry](https://python-poetry.org/)):

If you don't have **Poetry**, install it first:

```bash
pip install poetry
```

Then, install the required dependencies:

```bash
poetry install
```

### 3️⃣ Create a `.env` file (required for configuration)

Inside the project directory, create a `.env` file and add:

```bash
FLASK_ENV=development
FLASK_APP=app
FLASK_DEBUG=1
FLASK_RUN_HOST=0.0.0.0  # Only if on a trusted network
LOG_FOLDER=logs
LOG_FILE=timeed.log
LOG_LEVEL=20
LOG_MAX_BYTES=100
LOG_BACKUP=2

ADMIN_EMAIL=admin@timeed.com
ADMIN_GENDER=male # or female
ADMIN_NAME="Super Admin"
ADMIN_PASSWORD=Admin-Password
```

-   Search `flask environment variables list` online for more details on Flask's built-in variables.
-   The log variables are explained in `app/logging.py` under the `setup_logging` function.

### 4️⃣ Run the application:

```bash
poetry run flask run
```

By default, the app will be available at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

## **📜 License**

TimeED is licensed under a **custom restrictive license**.  
You may **view, run, and analyze** the code, but you **cannot** modify, redistribute, or use it for commercial purposes.

✅ **Contributions are welcome via pull requests**, but all changes require approval.  
❌ **Forking for personal modifications or redistribution is prohibited.**

For full details, see [LICENSE.md](./LICENSE.md).

## **👤 About**

TimeED is created and maintained by **DracoTato**. The app was inspired by the need to simplify time management for teachers and students.

**Feedback and suggestions are always welcome!**

Special thanks to [AATANKI](https://github.com/AA-TANKI) for contributing to the previous version of TimeED (**eTeach**).
