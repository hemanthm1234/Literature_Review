---
name: download-papers
description: Search for research papers from top conferences (CVPR, ECCV, ICML, ICLR, AAAI, NeurIPS, SIGGRAPH, etc.) and add them to the download_papers.sh script.
---

# Literature Review: Stage 1 - Download Papers

This skill is the **first stage** of the literature review process. It is used to find relevant research papers from top AI/CV conferences like (CVPR, ECCV, ICML, ICLR, AAAI, NeurIPS, SIGGRAPH, etc.) or ArXiv and prepare them for downloading. I prefer papers to be form CVPR, ECCV, ICML, ICLR, AAAI, NeurIPS, SIGGRAPH, etc. over arxiv preprints, unless the arxiv preprint is very recent (from 2026) and from a very good research group/author and is very relevant to our PS. Don't chose any 2025 or before arxiv preprints.

## Instructions

1. **Determine Track**: First, determine which of the three tracks (`4D`, `Surface_Quality`, or `Pruning_Efficiency`) the topic belongs to.
2. **Search for Papers**: Use the `search_arxiv.py` script (located in the corresponding track's folder) or your web search tools to find relevant papers.
3. **Add to Script**: Append the papers you find to the `download_papers.sh` script located in the **corresponding track's folder**. The `papers/` folder should be created inside the track's folder.
4. **DO NOT Run the Script**: Just append the new papers to the script. The user will run the script manually to download the papers into the `papers/` folder. Stop your task here.

## Naming Convention

When adding a paper to the `download_papers.sh` script, use the `download_paper` function with the following arguments:
`download_paper "[Short Title]" "[PDF URL]" "[Filename]" &`

The `[Filename]` MUST follow this strict naming convention:
`[Conference][Year]_[ShortTitle].pdf`

For example:
- `CVPR2026_MeshSplatting.pdf`
- `ArXiv2025_Instant4D.pdf`
- `NeurIPS2025_4DGS-1K.pdf`

Example of what to append:
`download_paper "MeshSplatting" "https://arxiv.org/pdf/2512.06818.pdf" "CVPR2026_MeshSplatting.pdf" &`

Make sure to include the `&` at the end of the command to ensure parallel downloading.
