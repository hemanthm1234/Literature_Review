# Workspace Agent Rules

This file contains rules and guidelines specific to this workspace.

<RULE>

# Current Problem Statement Context

> **Project:** HiLite-4D: High-Fidelity, Lightweight Surface Reconstruction for Dynamic Scenes

**Background:** Modelling 4D dynamic scenes is of utmost importance in fields like AR/VR, digital twins, telepresence, and robotics. For these applications to be practical, the reconstructed assets must be both computationally efficient (capable of real-time rendering and fast optimization) and high-fidelity (yielding high fidelity surfaces geometry).

**Current Methods:** Existing works which focus on High Fidelity reconstruction use a lot of Gaussians and are compute intensive. Papers that focus on improving speed generally opt for pruning techniques that lead to bad surface reconstruction.

**Goal:** Bridge the gap between Speed and Quality of surface reconstruction to enable practical usage of 4D assets on low compute devices.

**Scope:** Exploring various techniques for High Fidelity reconstruction like different regularisation losses, different surface representations, etc. Exploring efficiency techniques like pruning number of gaussians, different representations of motion, etc. Understanding current baselines and existing trade-off better.
</RULE>

---

<RULE>

## Workspace Specific Context/Rules

1. **Research Tracks**:
   We are currently surveying literature across three different tracks. Each track has its own dedicated directory in the workspace containing its own `papers/`, `notes/`, `architecture_diagrams/`, scripts, and documentation files:
   - **`4D/` Track**: For general 4D-related papers.
   - **`Surface_Quality/` Track**: For surveying papers that focus on improving surface reconstruction quality (does not need to be exclusively 4D; applies to general surface quality improvements).
   - **`Pruning_Efficiency/` Track**: For papers focused on reducing compute requirements (e.g., pruning Gaussians, improving efficiency, reducing memory).

2. **Scripts & Automation (Per Track)**:
   When working within a specific track directory (e.g., `Surface_Quality/`), use the scripts located in or designated for that directory:
   - `search_arxiv.py`: Find relevant research papers.
   - `download_papers.sh`: Download papers into that track's `papers/` directory.
   - `extract_architecture_diagrams.py`: Parse papers in the `papers/` directory and extract diagrams into the track's `architecture_diagrams/` folder.

3. **Documentation & Notes (Per Track)**:
   - `literature_review.md`: Update or consult this file (inside the track's folder) when synthesizing findings.
   - `problem_statement_ideas.md`: Use this file to brainstorm ideas for the problem statement relevant to the track. Not very relevant now because now we have identified a specific research gap to focus on.
   - `Problem_Statement.md`: The formal draft for the overall problem statement.
   - Keep any rough notes in the track's `notes/` directory.

</RULE>