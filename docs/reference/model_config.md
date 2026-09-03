# Models

!!! hint "Tutorial"

    Please see the [model section in the installation guide](../installation/keys.md) for an overview of the different models and how to configure them.

This page documents the configuration objects used to specify the behavior of a language model (LM).

In most cases, you will want to use the `GenericAPIModelConfig` object.

## API LMs

::: codefixer.agent.models.GenericAPIModelConfig
    options:
        heading_level: 3

::: codefixer.agent.models.RetryConfig
    options:
        heading_level: 3


## Manual models for testing

The following two models allow you to test your environment by prompting you for actions.
This can also be very useful to create your first [demonstrations](../config/demonstrations.md).

::: codefixer.agent.models.HumanModel
    options:
        heading_level: 3

::: codefixer.agent.models.HumanModelConfig
    options:
        heading_level: 3

::: codefixer.agent.models.HumanThoughtModel
    options:
        heading_level: 3

::: codefixer.agent.models.HumanThoughtModelConfig
    options:
        heading_level: 3

## Replay model for testing and demonstrations

::: codefixer.agent.models.ReplayModel
    options:
        heading_level: 3

::: codefixer.agent.models.ReplayModelConfig
    options:
        heading_level: 3

::: codefixer.agent.models.InstantEmptySubmitModelConfig
    options:
        heading_level: 3
