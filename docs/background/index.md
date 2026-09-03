# Project overview

This section of the documentation talks about the architecture and research goals of [Code-Fixer](#code-fixer).

## Code-Fixer <a name="code-fixer"></a>

Code-Fixer turns LMs (e.g. GPT-4) into software engineering agents that can fix issues in GitHub repositories.

On [SWE-bench](https://github.com/SWE-bench/SWE-bench), Code-Fixer resolves **12.29%** of issues, achieving the state-of-the-art performance on the full test set.

We accomplish our results by designing simple LM-centric commands and feedback formats to make it easier for the LM to browse the repository, view, edit and execute code files. We call this an 🤖 **Agent-Computer Interface (ACI)**.
Read more about the ACI [here](aci.md).

Code-Fixer is built and maintained by researchers from Princeton University.

For a quick introduction, watch the following video:

<iframe width="560" height="315" src="https://www.youtube.com/embed/CeMtJ4XObAM?si=W2tyY9EpEe-v12EU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

A longer lecture touching on the project's motivation, research findings, as well as providing a hands-on tutorial on how to install, use, and configure Code-Fixer is provided here:

<iframe width="560" height="315" src="https://www.youtube.com/embed/d9gcXpiiDao" title="NeurIPS Hacker Cup AI: Codefixer" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

For in-depth information, read our [paper](https://arxiv.org/abs/2405.15793). If you found this work helpful, please consider using the following citation:

```bibtex
@inproceedings{yang2024codefixer,
  title={{SWE}-agent: Agent-Computer Interfaces Enable Automated Software Engineering},
  author={John Yang and Carlos E Jimenez and Alexander Wettig and Kilian Lieret and Shunyu Yao and Karthik R Narasimhan and Ofir Press},
  booktitle={The Thirty-eighth Annual Conference on Neural Information Processing Systems},
  year={2024},
  url={https://arxiv.org/abs/2405.15793}
}
```

## Code-Fixer <span class="enigma">EnIGMA</span> <a name="enigma"></a>

!!! warning "Compatibility"
    Code-Fixer <span class="enigma">EnIGMA</span> is currently only available for Code-Fixer v0.7.0.

Code-Fixer <span class="enigma">EnIGMA</span> adds advanced **offensive cybersecurity capabilities**.

On the [NYU CTF benchmark](https://github.com/NYU-LLM-CTF/LLM_CTF_Database), EnIGMA solves **13.5%** of the capture the flag (CTF) challenges, achieving the state-of-the-art performance on the full test set of 200 challenges, **surpassing previous agents by more than 3x** ([leaderboard](https://enigma-agent.com#results)).

We accomplish our results by extending the [🤖 ACIs](../background/aci.md) concept first introduced in Code-Fixer, to the cybersecurity domain. We establish the novel [**:gear: Interactive Agent Tools** (IATs)](https://github.com/shaoshao66/code-fixer/0.7/background/iat/) concept, which enables our agent to use interactive tools such as a debugger, in a multitasking way such that the agent still has access to the main shell while using the debugger.

We also use a new **Summarizer** concept integrated into the agent to deal with long context. Read more about our different summarizers [here](https://github.com/shaoshao66/code-fixer/0.7/config/summarizers/).

Specific [demonstrations](../config/demonstrations.md) were built per each CTF category (cryptography, reverse-engineering, forensics, ...), to enhance the model ability to solve new tasks from the same category.

EnIGMA is built and maintained by researchers from Tel-Aviv University, New York University and Princeton University.

For a quick introduction, watch the following video:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IJxqOsNFiCc?si=xtIxyCcriM9FJexK" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

For all the details, read our [paper](https://arxiv.org/abs/2409.16165). If you found this work helpful, please consider using the following citation:

```bibtex
@misc{abramovich2024enigmaenhancedinteractivegenerative,
      title={EnIGMA: Enhanced Interactive Generative Model Agent for CTF Challenges},
      author={Talor Abramovich and Meet Udeshi and Minghao Shao and Kilian Lieret and Haoran Xi and Kimberly Milner and Sofija Jancheska and John Yang and Carlos E. Jimenez and Farshad Khorrami and Prashanth Krishnamurthy and Brendan Dolan-Gavitt and Muhammad Shafique and Karthik Narasimhan and Ramesh Karri and Ofir Press},
      year={2024},
      eprint={2409.16165},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2409.16165},
}
```
