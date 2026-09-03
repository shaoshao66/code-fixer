# Code-Fixer command line interface

All functionality of Code-Fixer is available via the command line interface via the `codefixer` command.

You can run `codefixer --help` to see all subcommands.

## Running Code-Fixer

* `codefixer run`: Run Code-Fixer on a single issue ([tutorial](hello_world.md)).
* `codefixer run-batch`: Run Code-Fixer on a batch of issues ([tutorial](batch_mode.md)).
* `codefixer run-replay`: Replay a trajectory file or a demo file. This means that you take all actions from the trajectory and execute them again in the environment. Useful for debugging your [tools](../config/tools.md) or for building new [demonstrations](../config/demonstrations.md).

## Inspecting runs

* `codefixer inspect` or `codefixer i`: Open the command line inspector ([more information](inspector.md)).
* `codefixer inspector` or `codefixer I`: Open the web-based inspector ([more information](inspector.md)).
* `codefixer quick-stats` or `codefixer qs`: When executed in a directory with trajectories, displays a summary of `exit_status` and more

## Advanced scripts

* `codefixer merge-preds`: Merge multiple prediction files into a single file.
* `codefixer traj-to-demo`: Convert a trajectory file to an easy to edit demo file ([more information on demonstrations](../config/demonstrations.md)).
* `codefixer remove-unfinished`: Remove unfinished trajectories
