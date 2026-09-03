# Environment variables

This page details all environment variables that are currently in use by Code-Fixer.

* All API keys (for LMs and GitHub) can be set as an environment variable. See [here](../installation/keys.md) for more information.
* `CODE_FIXER_CONFIG_ROOT`: Used to resolve relative paths in the [config](config.md). E.g., if `CODE_FIXER_CONFIG_ROOT=/a/b/c` and you set
  add a tool bundle as `tools/my_bundle`, it will be resolved to `/a/b/c/tools/my_bundle`. The default of `CODE_FIXER_CONFIG_ROOT` is the
  the `code-fixer` package directory.

The following variables can only be set as environment variables, not in the config file.

If you install `code-fixer` without the `--editable` option, please make sure to set

* `CODE_FIXER_CONFIG_DIR` (default `<PACKAGE>/config`)
* `CODE_FIXER_TOOLS_DIR` (default `<PACKAGE>/tools`)
* `CODE_FIXER_TRAJECTORY_DIR` (default `<PACKAGE>/trajectories`)

In addition, the following env variables allow to configure the logging.

* `CODE_FIXER_LOG_TIME`: Add timestamps to log
* `CODE_FIXER_LOG_STREAM_LEVEL`: Level of logging that is shown on the command line interface (`TRACE` being a custom level below `DEBUG`). Will have no effect for `run-batch`.

!!! hint "Persisting environment variables"
    Most environment variables can also be added to `.env` instead.