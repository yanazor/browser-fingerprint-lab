# Security Policy

## Supported Versions

Security fixes are applied to the latest version of the project available on
the default branch.

Older commits, forks, and locally modified deployments are not actively
supported.

## Reporting a Vulnerability

Do not disclose a suspected vulnerability in a public issue, discussion, pull
request, log, database, or screenshot.

Use GitHub private vulnerability reporting if the repository provides the
"Report a vulnerability" option.

If private vulnerability reporting is unavailable, open a public issue titled:

    [Security] Request for private reporting channel

Do not include vulnerability details in that issue. The maintainer will provide
an appropriate private communication method.

A useful private report should contain:

- a concise description of the vulnerability;
- the affected project version or commit;
- the affected Python, browser, and Docker versions;
- minimal reproduction steps;
- the potential security or privacy impact;
- sanitized proof-of-concept data;
- suggested remediation, if known.

Do not submit real browser fingerprints, cookies, session identifiers,
authorization headers, access tokens, passwords, request dumps, production
databases, or personal information.

## Response Process

This is a small independently maintained educational project without a
guaranteed service level agreement.

The maintainer will make a reasonable effort to:

1. acknowledge a complete report;
2. reproduce and assess the issue;
3. determine its security and privacy impact;
4. prepare a fix or mitigation where appropriate;
5. coordinate disclosure after a fix is available.

## Security Scope

Examples of relevant security issues include:

- exposure of logs or database content through static files;
- arbitrary file read or write;
- command, template, SQL, or script injection;
- unsafe handling of malformed request data;
- unauthorized access to collected records;
- disclosure of cookies, authorization headers, or session identifiers;
- unintended transmission of fingerprint data to third parties;
- a vulnerable dependency with a practical impact on this application;
- container configuration that exposes files or services unexpectedly.

Browser fingerprint collection that is clearly documented and intentionally
implemented as part of the educational lab is not, by itself, considered a
security vulnerability.

Undocumented collection, transmission, or exposure of data may be considered a
security or privacy issue.

## Safe Research Requirements

Use only synthetic or personally controlled test data.

Do not test the application against systems, browsers, accounts, or users
without authorization.

Do not include real fingerprint records or personal data in vulnerability
reports.

Use fictional values such as:

    192.0.2.10
    browser.example.test
    example-session-id
    synthetic-user-agent

## Dependency Vulnerabilities

A dependency advisory alone may not demonstrate that this project is
exploitable.

Reports should explain, where possible:

- which dependency and version are affected;
- whether the vulnerable code path is used;
- how the issue affects this application;
- which safe upgrade or mitigation is available.
