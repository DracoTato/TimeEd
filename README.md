# TimeEd

**Status:** Work In Progress.

**History**

TimeEd was built based on the experiences and lessons learned from a previous project, eTeach. While eTeach was less mature and had a less defined vision, TimeEd is much more refined, thanks to the lessons learned from eTeach's shortcomings.

**Vision**

TimeEd is designed to aid teachers in managing students and course material, automating the boring stuff and making the process more efficient.

**Tech Stack**

Built with **Flask (Server-Side Rendering)** and **SQLalchemy** as the back-end.

**HTML**, **CSS**, and **vanilla JS** for the front-end.

## Features

**For Teachers**

-   **Create & Manage Groups** – Divide your students into smaller groups that can be manage individually.
-   **Schedule & Manage Sessions** – Plan, edit, or cancel sessions effortlessly.
-   **Track Attendance** – Stay updated on student attendance.

**For Students**

-   **View & Join Groups** – Track enrolled groups and discover new ones.
-   **Session Updates** – Receive reminders and cancellation alerts.
-   **Request Absence** – Notify teachers if you can't attend a session.

## Installation

### 1️⃣ Clone the repository:

```bash
git clone git@github.com:DracoTato/TimeEd.git
cd TimeEd
```

### 2️⃣ Install dependencies (using [Poetry](https://python-poetry.org/)):

If you don't have **Poetry**, install it first using **pip** or any other package manger:

```bash
pip install poetry
```

Then, install the required dependencies:

```bash
poetry install
```

Install dev dependencies (optional):

```bash
poetry install --dev
```

### 3️⃣ Create a `.env` file (required for configuration)

Inside the project directory, create a `.env` file and add (TimeEd/.env):

```bash
FLASK_ENV=development # or production
FLASK_APP=app
FLASK_RUN_HOST=0.0.0.0  # Allows the server to be accessible on your local network (use on trusted networks only)
LOG_FOLDER=logs # Name of the log folder (will be created)
LOG_FILE=timeed.log # Name of the log file
LOG_LEVEL=20 # Min log level to write in log file (20=INFO)
LOG_MAX_BYTES=100 # Max number of bytes per file
LOG_BACKUP=2 # Number of log files to keep, before removing older ones

# Admin credentials
ADMIN_EMAIL=admin@timeed.com
ADMIN_GENDER=male # Or female
ADMIN_NAME="Super Admin"
ADMIN_PASSWORD=Admin-Password # Make sure it's secure
```

-   You can find more details on Flask environment variables [here](https://flask.palletsprojects.com/en/stable/config/#environment-and-debugging)
-   The log-related variables are explained in `app/logging.py` under the `setup_logging` function.

### 4️⃣ Run the application:

```bash
poetry run flask run
```

By default, the app will be available at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

## License

TimeED is licensed under a **custom restrictive license**.

You may **view, study, and use it for personal purposes**. You **cannot** redistribute, or use it for commercial purposes.

For full details, see [LICENSE.md](./LICENSE.md).

## Contributions

TimeEd is a personal learning project.
At this stage, I prefer to build everything myself to maximize my learning.
Contributions are not currently accepted.

In the future, I may allow contributions and fully open-source the project — but for now, that's not the case.

For more details, see the [contribution guide](./Contributions.md)

> **Note**  
> The Contributions Guide is a personal document for tracking contribution rules and ideas. It's not meant for public contributions at this stage.

**Feedback and suggestions are always welcome!**

Special thanks to [AATANKI](https://github.com/AA-TANKI) for contributing to **eTeach**.
