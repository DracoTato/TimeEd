# TimeEd

Formerly know as eTeach, TimeEd is a time management web application designed to help teachers and students organize their schedules, track progress, and boost productivity. Built with Flask (Server-Side Rendering), TimeEd aims to simplify session and group management for educational purposes.


## Features

### For Teachers:
- **Create and Manage Groups**: Add groups with specific descriptions and manage their details.
- **Schedule and Manage Sessions**: Set, edit, or cancel sessions with ease.
- **Track Attendance**: Stay updated with students' attendance for sessions.

### For Students:
- **View and Join Groups**: Keep track of your enrolled groups and join new ones.
- **Session Updates**: Receive session reminders and notifications about cancellations.
- **Request Absence**: Notify teachers if you are unable to attend a session.


## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, and JavaScript (SSR)
- **Database**: SQLite (for development), extendable to PostgreSQL or MySQL
- **Deployment**: Render


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TimeEd.git
   cd TimeEd
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`.


## Deployment

### On Render
1. Push your code to GitHub.
2. Sign in to [Render](https://render.com) and connect your GitHub repository.
3. Create a new "Web Service" with the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy and access your application at the provided Render URL.


## License

TimeEd may be used for personal and/or learning purposes, however it may NOT be used for commercial use without consent from the owner.


## About

TimeEd is created and maintained by **DracoTato**. The app is inspired by the need to simplify time management for teachers and students. Feedback and suggestions are always welcome!