# Contributing to Browser Fingerprint Lab

Thank you for your interest in improving Browser Fingerprint Lab.

Contributions are welcome, including bug fixes, documentation improvements,
privacy improvements, compatibility updates, tests, and small usability
enhancements.

## Before You Start

Check the existing issues before opening a new one.

Use the appropriate issue template when reporting a bug or suggesting a
feature. For security vulnerabilities, follow the instructions in
`SECURITY.md` instead of creating a public issue.

## Project Scope

This project is an educational and experimental browser fingerprinting lab.

Contributions must preserve its research and demonstration purpose. Changes
must not introduce covert tracking, deceptive collection, credential theft,
or collection of data unrelated to the documented browser fingerprint
experiment.

## Development Environment

A typical development environment includes:

- Python;
- Flask and the dependencies listed by the project;
- Docker, where Docker-based execution is used;
- a modern web browser;
- Git.

Create and activate a virtual environment when working locally:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip

Install project dependencies using the dependency file provided by the
repository.

For example:

    python -m pip install -r requirements.txt

## Making Changes

1. Fork or clone the repository.
2. Create a separate branch:

       git switch -c fix/short-description

3. Keep each change focused on one problem.
4. Preserve existing behaviour unless the change intentionally modifies it.
5. Update documentation when changing collected attributes, storage,
   dependencies, routes, Docker behaviour, or user-visible output.
6. Avoid unrelated formatting or refactoring in the same pull request.

Python changes should:

- use clear names and readable control flow;
- handle malformed or missing input safely;
- avoid logging unnecessary request data;
- avoid exposing database contents or logs through static files;
- use parameterized database queries;
- fail with clear and useful error messages.

Frontend changes should:

- avoid unnecessary third-party dependencies;
- document newly collected browser attributes;
- avoid sending data to external services unless explicitly documented;
- preserve clear user visibility into what information is collected.

## Privacy and Test Data

Never commit or include in issues, logs, screenshots, or pull requests:

- real browser fingerprint records;
- production database files;
- real IP addresses linked to users;
- cookies or session identifiers;
- authorization headers;
- access tokens or passwords;
- full request dumps containing personal data;
- private browsing history;
- real internal hostnames;
- screenshots containing personal or infrastructure information.

Use synthetic or clearly fictional test data.

Safe examples include:

    192.0.2.10
    user-agent-example
    example-session-id
    browser.example.test

Database files generated during local testing should not be committed unless
they are explicitly documented synthetic fixtures.

## Testing

Run the available automated tests:

    python -m pytest

If the project does not yet contain automated tests, perform a manual check
and describe it in the pull request.

Verify that:

- the application starts successfully;
- the main page loads;
- fingerprint attributes are displayed as expected;
- submitted data is handled without server errors;
- malformed or incomplete requests do not expose stack traces or secrets;
- logs do not contain unnecessary sensitive information;
- generated databases, logs, and temporary files are not added to Git.

If Docker files are changed, build the image:

    docker build -t browser-fingerprint-lab:test .

Run the container using the documented port and confirm that the application
responds correctly.

## Dependency Changes

Explain why a new dependency is required.

Avoid adding a dependency when the same result can be achieved clearly with
the standard library or an existing project dependency.

When updating JavaScript or Python dependencies, check for breaking changes
and update the documentation where necessary.

## Pull Requests

A pull request should:

- explain what was changed and why;
- describe how the change was tested;
- identify changes to collected or stored data;
- remain limited to one logical change;
- include documentation updates where necessary;
- pass the repository's automated checks;
- contain no real fingerprint data or other sensitive information.

Small and focused pull requests are easier to review than large unrelated
changes.

## Commit Messages

Use concise, descriptive commit messages, for example:

    Fix fingerprint submission validation
    Document collected browser attributes
    Remove duplicate frontend dependency
    Improve Docker startup instructions

## License

By submitting a contribution, you agree that it may be distributed under the
license used by this repository.
