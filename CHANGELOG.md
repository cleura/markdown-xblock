# Changelog

## Unreleased

- Add agentic coding guidelines.
- Remove extraneous dependencies.
- Create this changelog (to replace the earlier `reno`-based change tracking approach).

## Version 2.4.1 (2026-11-04)

- Add Python 3.13 and 3.14 to the test matrix.
- Drop `edx-i18n-tools`; replace `path` usage with `pathlib`.
- Update pip to v26.2.2.

## Version 2.4.0 (2026-09-01)

- Automate PyPI releases via GitHub Actions.
- Review and update test dependencies.

## Version 2.3.0 (2026-02-16)

- Moved to a modern `pyproject.toml` settings file (truncate `setup.py`).
- Update requirements for the Open edX Verawood release.

## Version 2.2.0 (2025-08-01)

- Update tests for URL handling in safe mode.
- Bump requirements for the Open edX Ulmo release.

## Version 2.1.0 (2025-01-03)

- Bump requirements to support Open edX Teak release.

## Version 2.0.0 (2024-10-16)

- Drop support for Python 3.8; require XBlock ≥2.
- Bump GitHub action versions.

## Version 1.6.0 (2024-08-02)

- Add pipdeptree to the CI test matrix.
- Remove Python 3.10 from the test matrix.
- Add support for Open edX Redwood release.

## Version 1.5.0 (2024-04-15)

- Add support for Python 3.12.

## Version 1.4.0 (2023-12-21)

- Bump requirements for the Open edX Quince release.
- Update README.

## Version 1.3.0 (2023-03-14)

- Use `tox<4` for GitHub Actions workflow.
- Bump requirements for the Open edX Olive release.

## Version 1.2.0 (2022-07-21)

- The XBlock can now also be used in a public course.

## Version 1.1.1 (2022-04-22)

- Default CSS for tables to match the current raw-HTML XBlock table styling for a better user experience.
- Add bumpversion support to `tox.ini`.
- Update requirements to support the Open edX Maple release.

## Version 1.1.0 (2021-07-06)

- The XBlock settings now support the string values `"replace"` and `"escape"` for `safe_mode`, just like the upstream Markdown2 library does.
  A Boolean value of `True` is considered to be equivalent to `"replace"`.
  A value of `False`, `None`, or the empty string disables safe mode.
- Removed support for Python 3.5.
  Python 3.8 is the recommended Python release.
- The XBlock now renders normally in "read-only" ("masquerading") mode, which applies when a course instructor (a user with either per-course or platform- wide Staff permissions) selects "View this course as" → "Specific learner" in the Open edX LMS.

## Version 1.0.7 (2020-10-16)

- Course export: markdown content is written to a separate `.md` file instead of the markdown element's `data` attribute, and is read from that file during course import.
- Course export: each markdown file is no longer accompanied by a separate XML file with XBlock attributes.
  The attributes are now included in the markdown node, defined in a vertical block.

## Version 1.0.6 (2020-10-13)

- Course authors can now export and import markdown content as separate files.

## Version 1.0.5 (2020-09-25)

- The XBlock now has a new editable field `classes` that allows course authors to add custom CSS classes to the component.

## Version 1.0.4 (2020-09-23)

- Fix course export (write `.md` files to the export filesystem).

## Version 1.0.3 (2020-09-21)

- Course authors using Open edX Studio can now use syntax highlighting, which previously did not work due to missing CodeMirror JavaScript and CSS files.

## Version 1.0.2 (2020-09-21)

- Unit testing, linting, and CI are configured via tox and flake8.
  A `.gitlab-ci.yml` file is included for GitLab mirrors of the repository.
- Add reno for change-log management.
- Add pre-commit and pre-push Git hooks.
- Use setuptools-scm to determine package version automatically.
- Various README and PyPI badge fixes.

## Version 1.0.1 (2020-09-17)

- Build a Markdown XBlock based on the HTML XBlock by OpenCraft.
- Substitute `%%USER_ID%%` and `%%COURSE_ID%%` keywords in rendered content.

## Version 1.0.0 (2020-07-24)

- Update for Open edX Juniper release.
