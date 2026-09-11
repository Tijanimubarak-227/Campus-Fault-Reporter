1. Branching Strategy
* We use trunk-based branching.
* All new development work must take place on short-lived feature branches named using the pattern `feature/*` (e.g., `feature/login-page`).

2. Pull Request (PR) & Code Review Rules
* Every PR must be reviewed and approved by a teammate who did not write the code before merging into `main`.

3. Commit Message Standards
* All commit messages must follow the Conventional Commits specification (e.g., `feat: ...`, `fix: ...`, `docs: ...`).

## 4. Environment Variables & Secrets
* Secrets and private configuration data must only be stored in environment variables (`.env`). Never commit credentials or API keys directly to the repository.

## 5. Deployment & Rollback Owner
* The designated **on-call** team member serves as the official rollback owner responsible for production stability.
