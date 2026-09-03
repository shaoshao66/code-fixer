# Agent configuration

This page documents the configuration objects used to specify the behavior of an agent.
To learn about the agent class itself, see the [agent class reference page](agent.md).

It might be easiest to simply look at some of our example configurations in the [config dir](https://github.com/shaoshao66/code-fixer/tree/main/config).

<details>
<summary>Example: default config <code>default.yaml</code></summary>

```yaml
--8<-- "config/default.yaml"
```
</details>

Currently, there are three main agent classes:

* `DefaultAgentConfig`: This is the default agent.
* `RetryAgentConfig`: A "meta agent" that instantiates multiple agents for multiple attempts and then picks the best solution.
* `ShellAgentConfig`: Config for `ShellAgent` (invoked with `codefixer sh`), which is an experimental mode for quick & interactive (human-in-the-loop) workflows.

::: codefixer.agent.agents.RetryAgentConfig

::: codefixer.agent.agents.DefaultAgentConfig

::: codefixer.agent.agents.ShellAgentConfig