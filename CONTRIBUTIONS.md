# Contributions Guide

**Current Status**

TimeEd is a personal learning project.
I am currently not accepting contributions from others.

The goal is for me to handle all aspects of development myself to maximize learning.

Feedback and suggestions (through issues or discussions) are welcome, but direct code contributions (pull requests, forks, etc.) will not be merged at this time.

**Why does this exist then?**

It serves as a benchmark/reference for myself.

## Code Specs

-   **Code Quality**: Clean, readable code following best practices. (e.g., PEP8 for Python)
-   **Consistency**: Follow the existing style and structure of the project.
-   **Commit Messages**: Clear and descriptive commit messages.

## More Info on Commit Messages

All commit messages must follow this format:

`Action(module): description.`

**List of Actions**

-   `Feat`: A new feature or block of code is introduced.
-   `Refactor`: A feature/block of code has been refactored. (no bug necessarily existed)
-   `Fix`: A bug has been fixed.
-   `Style`: Cosmetic changes, e.g., formatting, renaming variables/functions, etc.
-   `Chore`: Non-functional changes. (configs, dependencies, gitignore, etc...)

**List of Modules**

-   `front-end`: Front-end related code.
-   `routes`: Route related code.
-   `logs`: Log related code.
-   `forms`: WTForms.
-   `config`: Config related code.
-   `db`: Database related code.
-   `utils`: Utility/helper functions.
-   `docs`: Doc files like README, LICENSE — use with `Chore` and `Style`.
-   `messages`: Any modifications to app messages — use with `Chore` and `Style`.
-   `poetry`: Dependency management — use with `Chore` and `Style`.
-   `hooks`: Git hooks — use with `Chore` and `Style`.

> **Note**  
> You can use multiple modules, if you _need_, e.g. `Feat(front-end/blueprint): desc.`
> Prioritize the most relevant module when multiple apply.

**Description Specs**

-   Be concise.
-   Use infinitive verbs, e.g. add instead of added.
-   Max 60 chars. (use double messages if you need to add more)
