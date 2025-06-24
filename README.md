# TimeEd

**Status:** Work in progress.

## Vision

TimeEd is designed to aid teachers in managing students and course material, automating the boring stuff and making the process more efficient.

## Tech Stack

- **Flask** (server-side rendering)
- **SQLAlchemy**
- **HTML**, **CSS**, **vanilla JS**

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:DracoTato/TimeEd.git
cd TimeEd
```

### 2. Install dependencies (using [Poetry](https://python-poetry.org/))

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

### 3. Move `.env.example` to `.env` (required for configuration)

- You can find more details on Flask environment variables in [flask docs](https://flask.palletsprojects.com/en/stable/config/#environment-and-debugging)
- The log-related variables are explained in `app/logging.py` under the `setup_logging` function.

### 4. Run the application

```bash
poetry run flask run
```

By default, the app will be available at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

## License

TimeEd is licensed under the **MIT license**.

For full details, see [LICENSE.md](./LICENSE.md).

## Contributions

TimeEd is a personal learning project.
Contributions are not currently accepted.

For more details, see the [contribution guide](./CONTRIBUTIONS.md)

**Feedback and suggestions are always welcome!**

Special thanks to [AATANKI](https://github.com/AA-TANKI) for contributing to **eTeach**.
