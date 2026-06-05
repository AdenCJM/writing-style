# Security

## Reporting a vulnerability

Please report security issues privately through GitHub's "Report a vulnerability"
button under the repository's **Security** tab, rather than opening a public
issue. We'll respond as quickly as we can.

## GitHub Actions safety

The evaluation harness runs in two workflows under `.github/workflows/`. They're
set up so an untrusted pull request can't reach secrets or write access:

- **`ANTHROPIC_API_KEY` is never exposed to pull requests.** The jobs that use it
  (the live eval and the improve step) run only on manual dispatch and the weekly
  schedule. The `pull_request` trigger runs the deterministic `check` job alone,
  with read-only permissions and no secrets.
- **The improve workflow is manual only.** It holds write access so it can open a
  pull request, but it never commits to the default branch, and the change it
  proposes is reviewed before it lands.
- **Least privilege.** Each workflow declares the narrowest permissions it needs.

### Recommended repository setting

Under **Settings → Actions → General**, set workflow approval to "Require
approval for all external collaborators" (or keep GitHub's default approval for
first-time contributors). This stops a stranger's pull request from running CI on
the runner until a maintainer approves it.
