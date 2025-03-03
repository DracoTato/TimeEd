# TimeEd

Formerly know as eTeach, TimeEd is a time management web application designed to help teachers and students organize their schedules, track progress, and boost productivity. Built with Flask (Server-Side Rendering), TimeEd aims to simplify session and group management for educational purposes.

## Features

### For Teachers:

-   **Create and Manage Groups**: Add groups with specific descriptions and manage their details.
-   **Schedule and Manage Sessions**: Set, edit, or cancel sessions with ease.
-   **Track Attendance**: Stay updated with students' attendance for sessions.

### For Students:

-   **View and Join Groups**: Keep track of your enrolled groups and join new ones.
-   **Session Updates**: Receive session reminders and notifications about cancellations.
-   **Request Absence**: Notify teachers if you are unable to attend a session.

## Tech Stack

-   **Backend**: Flask (Python)
-   **Frontend**: HTML, CSS, and JavaScript (SSR)
-   **Database**: SQLite (for development), extendable to PostgreSQL or MySQL
-   **Deployment**: Render

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/TimeEd.git
    cd TimeEd
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv .venv
    source venv/bin/activate  # On Windows powershell: venv\bin\activate.ps1
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create `.env` file in root directory:

    ```bash
    FLASK_ENV=development
    FLASK_APP=app
    FLASK_DEBUG=1
    FLASK_RUN_HOST=0.0.0.0 # Only if on trusted network
    LOG_FOLDER=logs
    LOG_FILE=timeed.log
    LOG_LEVEL=20
    LOG_MAX_BYTES=100
    LOG_BACKUP=2
    ```

    - search `flask environment variables list` on the internet for more detail on flask's built-in variables
    - the log variables are documented in the `app/logging.py`:`setup_logging` function.

5. Run the application:
    ```bash
    flask run
    ```
    Assuming you used the default settings, The application will be available at `http://127.0.0.1:5000`.

## Deployment

### On Render

1. Push your code to GitHub.
2. Sign in to [Render](https://render.com) and connect your GitHub repository.
3. Create a new "Web Service" with the following settings:
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `gunicorn app:app`
4. Deploy and access your application at the provided Render URL.

### On PythonAnyWhere

1. Create a new web service.
2. Create a deploy SSH key.
3. Specify your application variable in the wsgi file.
4. pull from the GitHub repo.

## License

TimeEd may be used for personal and/or learning purposes, however it may NOT be used for commercial use without consent from the owner.

## About

TimeEd is created and maintained by **DracoTato**. The app is inspired by the need to simplify time management for teachers and students. Feedback and suggestions are always welcome!
