---
name: include-arch-diagrams
description: Extract architecture diagrams from downloaded papers and insert them into the literature review file right after the paper titles.
---

# Literature Review: Stage 3 - Include Architecture Diagrams

This skill is the **third and final stage** of the literature review process. It should be executed after you have successfully read the papers and taken notes in the `literature_review.md` file.

## Instructions

1. **Extract Diagrams**: Run the `extract_architecture_diagrams.py` script located within the specific track folder (e.g., `4D/extract_architecture_diagrams.py`).
   - This script will automatically process the PDFs in the `papers/` directory and save the extracted images into the `architecture_diagrams/` folder for that track.
2. **Insert into Notes**: Once the extraction script completes, edit the `literature_review.md` file for that track to include the newly extracted architecture diagrams.
3. **Placement (CRITICAL)**: You must insert the markdown image links **exactly after the Title of the respective paper** and **before the rest of the text/notes**.
   - Example format:
     ```markdown
     ## CVPR2026_MeshSplatting
     
     ![Architecture Diagram](architecture_diagrams/CVPR2026_MeshSplatting_arch_1.png)
     
     **Problem Statement:**
     ...
     ```
4. **Relative Paths**: Ensure all image links use the correct relative path (e.g., `architecture_diagrams/filename.png`).
