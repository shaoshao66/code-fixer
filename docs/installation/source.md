# Installation from source

Installation from source is the preferred way to set up Code-Fixer on your machine.

1. Clone the repository, for example with
    ```bash
    git clone https://github.com/shaoshao66/code-fixer.git
    ```
2. Run
    ```
    python -m pip install --upgrade pip && pip install --editable .
    ```
    at the repository root (as with any python setup, it's recommended to use [conda][] or [virtual environments][] to manage dependencies).
3. Set up your language model of choice as explained [here](keys.md).

Let's run a quick check:

```bash
codefixer --help
```

should show an overview over the available top-level commands.

<details>
<summary>Command not found?</summary>

You might also try <code>python -m codefixer</code>. If this also doesn't work,
please check with <code>which python</code> that you're using the same python as
when you installed Code-Fixer.

</details>

**Optional installation steps:**

1. The default backend for Code-Fixer is docker, so we recommend to install Docker
   ([follow the docs](https://github.com/docker/docker-install) or use the [get-docker.sh script for linux](https://github.com/docker/docker-install)),
   then start Docker locally. Problems? See [docker issues](tips.md#docker).
   If you do not want to use docker, you can still use Code-Fixer with code evaluation in the cloud.
2. If you plan on using the web-based GUI: Install [`Node.js`][nodejs-install].

[nodejs-install]: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

!!! tip "Installation tips"
    * If you run into docker issues, see the [installation tips section](tips.md) for more help.
    * Code-Fixer is still in active development. Features and enhancement are added often.
    To make sure you are on the latest version, periodically run `git pull`
    (there is no need to redo the `pip install`).
    * Code-Fixer EnIGMA is currently only compatible with `v0.7` of Code-Fixer. Please run `git switch v0.7` after step 1 to switch to the correct version.
    * Want to modify Code-Fixer? Great! There are a few extra steps and tips:
    Please check our [contribution guide](../dev/contribute.md).

[conda]: https://docs.conda.io/en/latest/
[virtual environments]: https://realpython.com/python-virtual-environments-a-primer/

{% include-markdown "../_footer.md" %}
