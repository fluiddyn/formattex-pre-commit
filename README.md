# formattex-pre-commit-mirror

A [pre-commit](https://pre-commit.com/) hook for
[formattex](https://pypi.org/project/formattex/) and
[formatbibtex](https://pypi.org/project/formatbibtex/).


## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/fluiddyn/formattex-pre-commit
  # Formattex version.
  rev: 0.1.4
  hooks:
    # Run the formatter for tex files.
    - id: formattex
    # Run the formatter for bibtex files.
    - id: formatbibtex
```
