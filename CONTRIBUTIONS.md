# Contributions Guide

**Current Status**

TimeEd is a personal learning project.
I am currently not accepting contributions from others.

The goal is for me to handle all aspects of development myself to maximize learning.

Feedback and suggestions (through issues or discussions) are welcome, but direct code contributions (pull requests, forks, etc.) will not be merged at this time.

**Why does this exist then?**

It serves as a benchmark/reference for myself.

## Code Specs

- **Code Quality**: Clean, readable code following best practices. (e.g., PEP8 for Python)
- **Consistency**: Follow the existing style and structure of the project.
- **Commit Messages**: Clear and descriptive commit messages.

## More Info on Commit Messages

All commit messages must follow this format:

`Action(module): description.`

**List of Actions**

- `Feat`: A new feature/block of code has been introduced.
- `Refactor`: A feature/block of code has been refactored/removed. (no bug necessarily existed)
- `Fix`: A bug/issue has been fixed.
- `Chore`: Non-functional changes. (formatting, variable names, typos, etc...)

**List of Modules**

- `frontend`: Frontend-related code.
- `backend`: backend-related code.
- `db`: Database-related code.
- `tests`: Test-related code.
- `infra`: Project infrastructure-related code, git hooks, file management, gitignore, dependency management.
- `docs`: Doc files like README, LICENSE, etc.

**Description Specs**

- Be concise.
- Use infinitive verbs, e.g. add instead of added.
- Max 60 chars. (Add a description if you need more)
