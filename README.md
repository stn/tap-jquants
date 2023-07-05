# tap-jquants

![GitHub Action](https://github.com/stn/tap-jquants/actions/workflows/ci_workflow.yml/badge.svg)

`tap-jquants` is a Singer tap for JQuants.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

- Pulls raw data from [J-Quants](https://jpx-jquants.com/)
- Extracts the following resources:
  - [daily_quotes](https://jpx.gitbook.io/j-quants-ja/api-reference/daily_quotes)
  - [announcement](https://jpx.gitbook.io/j-quants-ja/api-reference/announcement)
  - [dividend](https://jpx.gitbook.io/j-quants-ja/api-reference/dividend)
  - [statements](https://jpx.gitbook.io/j-quants-ja/api-reference/statements)
  - [index_option](https://jpx.gitbook.io/j-quants-ja/api-reference/index_option)
  - [topix](https://jpx.gitbook.io/j-quants-ja/api-reference/topix)
  - [listed_info](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info)
  - [breakdown](https://jpx.gitbook.io/j-quants-ja/api-reference/breakdown)
  - [prices_am](https://jpx.gitbook.io/j-quants-ja/api-reference/prices_am)
  - [short_selling](https://jpx.gitbook.io/j-quants-ja/api-reference/short_selling)
  - [trades_spec](https://jpx.gitbook.io/j-quants-ja/api-reference/trades_spec)
  - [weekly_margin_interest](https://jpx.gitbook.io/j-quants-ja/api-reference/weekly_margin_interest)
  - [trading_calendar](https://jpx.gitbook.io/j-quants-ja/api-reference/trading_calendar)


## Installation

Install from GitHub:

```bash
pipx install git+https://github.com/stn/tap-jquants.git@main
```


## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`


## Configuration

### Accepted Config Options

<!--
This section can be created by copy-pasting the CLI output from:

```
tap-jquants --about --format=markdown
```
-->

| Setting      | Required | Default | Description                                                       |
|:-------------|:--------:|:-------:|:------------------------------------------------------------------|
| mail_address |   True   |  None   | The mail address to authenticate against the J-Quants API service |
| password     |   True   |  None   | The password to authenticate against the J-Quants API service     |
| start_date   |  False   |  None   | The earliest record date to sync                                  |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-jquants --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

You need `mail_address` and `password` for [J-Quants API](https://jpx-jquants.com/).

## Usage

You can easily run `tap-jquants` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-jquants --version
tap-jquants --help
tap-jquants --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` sub-folder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-jquants` CLI interface directly using `poetry run`:

```bash
poetry run tap-jquants --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-jquants
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-jquants --version
# Configure the tap-jquants:
meltano config tap-jquants set --interactive
# Select streams:
meltano select tap-jquants topix "*"
# And run a test `elt` pipeline:
meltano run tap-jquants target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

## References

- [J-Quants API Reference](https://jpx.gitbook.io/j-quants-ja/)
- [J-Quants API Reference (English)](https://jpx.gitbook.io/j-quants-en/)
- [Meltanoとtap-jquantsを用いたELT](https://zenn.dev/akrisn/articles/meltano_jquants_setup)
