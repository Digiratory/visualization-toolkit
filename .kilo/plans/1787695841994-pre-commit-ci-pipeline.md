# Plan: Add Pre-commit Validation as First Step of Testing Pipeline

**Issue**: [#29](https://github.com/Digiratory/visualization-toolkit/issues/29) - [CI/CD] Add Pre-commit Validation as First Step of Testing Pipeline

**Goal**: Implement GitHub Actions workflow to run pre-commit validation as the first gate in CI/CD pipeline, preventing style/lint issues from entering the codebase.

---

## Current State

- `.pre-commit-config.yaml` exists with hooks: `pre-commit-hooks` v6.0.0, `isort` v7.0.0, `black` v25.12.0
- `.github/workflows/` contains only `nightly-build-and-publish.yml` and `publish-to-pypi.yml`
- No main CI workflow (`test-and-release.yml`) exists
- Python >=3.10 required per `pyproject.toml`
- No `CONTRIBUTION.md` exists

---

## Implementation Steps

### Step 1: Create Reusable Pre-commit Validation Workflow

**File**: `.github/workflows/reusable-pre-commit-validation.yml`

```yaml
name: Reusable - Pre-commit Validation

on:
  workflow_call:
    outputs:
      cache-key:
        description: 'The cache key used for pip dependencies'
        value: ${{ jobs.pre-commit-validation.outputs.cache-key }}

permissions:
  contents: read

jobs:
  pre-commit-validation:
    runs-on: ubuntu-latest
    outputs:
      cache-key: ${{ steps.cache-pip.outputs.key || 'pip-precommit-' }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Cache pip dependencies
        id: cache-pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-precommit-${{ hashFiles('**/pyproject.toml', '**/.pre-commit-config.yaml') }}
          restore-keys: |
            pip-precommit-

      - name: Install pre-commit
        shell: bash
        run: |
          python -m pip install --upgrade pip
          pip install pre-commit

      - name: Run pre-commit validation
        shell: bash
        run: |
          pre-commit run --all-files
```

**Key decisions**:
- Use `actions/checkout@v4`, `actions/setup-python@v5`, `actions/cache@v4` (matching existing workflow versions)
- Python 3.10 to match `pyproject.toml` requirement
- Output `cache-key` for downstream jobs

---

### Step 2: Create Main CI Workflow

**File**: `.github/workflows/test-and-release.yml`

```yaml
name: Test and Release

on:
  push:
    branches: [master, main]
    tags:
      - 'release/*'
  pull_request:
    branches: [master, main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  # FIRST STEP: Pre-commit validation
  pre-commit-validation:
    uses: ./.github/workflows/reusable-pre-commit-validation.yml

  # Test job depends on pre-commit passing
  test:
    name: Run Tests
    needs: pre-commit-validation
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[stats]"
          pip install pytest

      - name: Run tests
        run: |
          pytest tests/ -v

  # Build job depends on pre-commit passing
  build:
    name: Build Package
    needs: pre-commit-validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip setuptools wheel build setuptools-scm

      - name: Build package
        run: |
          python -m build --wheel

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/*.whl
```

**Key decisions**:
- Pre-commit runs first; test/build jobs use `needs:` to depend on it
- Test matrix covers Python 3.10, 3.11, 3.12
- Build job uploads wheel as artifact for potential release workflow

---

### Step 3: Update CONTRIBUTION.md

**File**: `CONTRIBUTION.md` (new file)

Add section documenting:
- How to install pre-commit locally: `pip install pre-commit && pre-commit install`
- How to run manually: `pre-commit run --all-files`
- CI will run pre-commit on all PRs and pushes to main/master
- All checks must pass before tests/builds execute

---

### Step 4: Validation Checklist

Verify the following acceptance criteria:

- [ ] Pre-commit validation runs on `pull_request` events
- [ ] Pre-commit validation runs on `push` to `master`/`main`
- [ ] Manual trigger via `workflow_dispatch` works
- [ ] Workflow fails fast if pre-commit checks fail (downstream jobs don't execute)
- [ ] Pip dependencies are cached
- [ ] Python version matches `pyproject.toml` (3.10)
- [ ] Local developers can run `pre-commit run --all-files`
- [ ] CONTRIBUTION.md documents the CI pre-commit requirement

---

## Agent Workflow

### Phase 1: Development (agent: code)
- Create `.github/workflows/reusable-pre-commit-validation.yml`
- Create `.github/workflows/test-and-release.yml`
- Create `CONTRIBUTION.md` with pre-commit documentation
- Verify YAML syntax validity

### Phase 2: Testing (agent: test-engineer)
- Validate workflow YAML syntax (e.g., `actionlint` or manual review)
- Verify pre-commit config works locally: `pre-commit run --all-files`
- Confirm all existing code passes pre-commit hooks
- Test that workflow triggers match specification (PR, push, workflow_dispatch)

### Phase 3: Debugging (if required) (agent: debug)
- Investigate any pre-commit hook failures on existing code
- Fix code formatting issues if hooks fail on current codebase
- Resolve any YAML syntax errors in workflow files
- Address any CI configuration issues discovered during testing

### Phase 4: Code Review (agent: code-reviewer)
- Review workflow files for GitHub Actions best practices
- Verify caching strategy is correct
- Check that `needs:` dependencies properly enforce execution order
- Review CONTRIBUTION.md for clarity
- Ensure no security issues (e.g., pinning action versions)

### Phase 5: Code Review Feedback Handling (agent: code)
- Address any feedback from code review
- Make necessary adjustments to workflow files
- Update CONTRIBUTION.md based on review comments
- Re-run validation if changes were made

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Existing code fails pre-commit hooks | Run `pre-commit run --all-files` locally first; fix any violations before CI |
| Cache invalidation issues | Use `restore-keys` fallback pattern |
| Python version mismatch | Pin to 3.10 in workflows (matches pyproject.toml) |
| Breaking existing PRs | Consider `continue-on-error: true` during initial rollout if needed |

---

## Out of Scope

- Modifying `.pre-commit-config.yaml` hook versions (already up to date)
- Adding new pre-commit hooks beyond existing configuration
- Modifying existing `nightly-build-and-publish.yml` or `publish-to-pypi.yml` workflows
- Implementing release automation (separate concern)
