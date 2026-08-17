---
name: take-notes
description: Read downloaded research papers in detail and add structured notes to the literature review file in reverse chronological order.
---

# Literature Review: Stage 2 - Read Papers & Take Notes

This skill is the **second stage** of the literature review process. It should be executed *after* the user has successfully run the `download_papers.sh` script and the PDFs are available in the track's `papers/` directory.

## Role
You are an expert AI Researcher and Senior Technical Reviewer. Your task is to read the provided academic research paper and extract its key components into a structured, highly technical markdown summary.

## Instructions

1. **Locate Papers**: Go into the `papers/` directory of the corresponding track (e.g., `4D/papers/`, `Surface_Quality/papers/`, or `Pruning_Efficiency/papers/`).
2. **Read in Detail**: Go through every single downloaded paper one by one thoroughly.
3. **Take Notes**: For each paper, fill out the "Extraction Template" below exactly as formatted.
   - **Be concise but highly technical.** Avoid fluff. Use appropriate mathematical and domain-specific terminology.
   - **Read between the lines.** Do not just copy what the authors claim; critically analyze the text. Pay special attention to identifying underlying assumptions and practical limitations that the authors might not highlight prominently.
   - If certain information is missing from the paper, explicitly state "Not provided in text."
4. **Update Literature Review**: Append your notes to the `literature_review.md` file located in the root of that specific track.
5. **Reverse Chronological Order (CRITICAL)**: You must organize the papers in the `literature_review.md` file in **reverse chronological order**. 
   - The **latest (newest)** papers must be placed at the **top** of the document.
   - The **older** papers must be placed towards the **bottom**.
   - Sort them properly by their publication year/conference based on their filenames (e.g., CVPR2026 goes above CVPR2025).

---

## Output: Extraction Template

The notes for each paper should strictly be in this structured markdown format.

```markdown
# Title (conference-year)

### 1. Metadata
*   **Paper Title:** [Exact title of the paper]
*   **Authors & Lab:** [List key authors, particularly first and last, and their affiliated university or corporate lab]
*   **Venue & Year:** [e.g., CVPR 2024, arXiv 2023]
*   **Code/Data Availability:** [Provide links to GitHub, project pages, or datasets if mentioned. State if closed-source]

### 2. Core Contribution
*   **Main Problem Statement:** [1-2 sentences defining the exact problem being solved]
*   **Novelty / Core Insight:** [What is the singular clever trick, new formulation, or architectural shift that makes this work? Distill this to its essence]
*   **Methodology / Key Ideas:** [A concise technical summary of the proposed method, architecture, or mathematical formulation]
*   **Achievements (Results):** [Key headline numbers. Did they achieve SOTA? By what margin? On what metrics?]

### 3. Critical Analysis
*   **Datasets & Baselines:** [List the specific datasets evaluated on and the primary prior works they compared against]
*   **Underlying Assumptions:** [What conditions must be true for this method to work? e.g., assumes static lighting, requires multi-view setup, assumes rigid objects]
*   **Limitations / Failure Cases:** [Where does this method break down? What remains unsolved? Critically evaluate beyond just the authors' stated limitations]
*   **Future Work:** [What do the authors propose as the next logical steps for this research?]
*   **Strategic Relevance:** [Analyze how this paper pushes the field forward. What specific piece of this work could be reused or adapted by other researchers in the field?]
```