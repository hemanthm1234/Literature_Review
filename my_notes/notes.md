> # `HiLite-4D`: High-Fidelity, Lightweight Surface Reconstruction for Dynamic Scenes


<div align="center">

![High Fidelity](https://img.shields.io/badge/High%20Fidelity-blue)
![4D SURFACE RECONSTRUCTION](https://img.shields.io/badge/4D%20SURFACE%20RECONSTRUCTION-orange)
![Efficient](https://img.shields.io/badge/Efficient-brightgreen)

</div>

![poster](../assets/poster.png)

> ## Baselines:

![Baseline Conference Timeline](../Surface_Quality/baseline_graph_combined.png)

![Baseline Representation Timeline](../Surface_Quality/baseline_graph_representation.png)

1) `Speede3DGS`
2) `4DSurf`

> ## Datasets:

1) `CMU Panoptic`: Ian3, Haggling-b2, Band1, Cello1, and Pizza1.

    * Captured with a circular rig of 10 RGB-D cameras at 1920 × 1080 resolution.
    * Each scene spans 24 timesteps and provides ground-truth point clouds.

    **Papers:**
    - 4DSurf

2) `Hi4D`: Backhug02, Basketall13, Fight17, Football18, Talk22, and Cheers37.

    * Captured with 8 RGB cameras at 940 × 1280 resolution.
    * On average, each sequence contains 118 timesteps and each timestep is annotated with a high-quality textured 3D mesh.

    **Papers:**
    - 4DSurf

* Compared with CMU Panoptic, Hi4D features larger motions, longer sequences, and multi-human scene.

> ## Metrics:

### Surface Quality:

<details>
  <summary><h4 style="display: inline;">1. Chamfer Distance (CD)</h4></summary>
<div style="height: 10px;"></div>


Chamfer Distance measures the discrepancy between two 3D point clouds (or surfaces sampled as point clouds). It calculates the average distance from each point in the first set to its nearest neighbor in the second set, and vice versa.

**Formula:**
$$d_{CD}(S_1, S_2) = \frac{1}{|S_1|} \sum_{x \in S_1} \min_{y \in S_2} ||x - y||_2^2 + \frac{1}{|S_2|} \sum_{y \in S_2} \min_{x \in S_1} ||x - y||_2^2$$

**Symbols:**
- $S_1, S_2$: The two point sets being compared (e.g., the reconstructed point cloud and the ground truth point cloud).
- $x, y$: Individual 3D points belonging to sets $S_1$ and $S_2$, respectively.
- $|S_1|, |S_2|$: The total number of points in sets $S_1$ and $S_2$.
- $||x - y||_2^2$: The squared Euclidean distance between point $x$ and point $y$.
- $\min_{y \in S_2}$: Finds the closest point in $S_2$ for a given point $x \in S_1$.

**Papers:**
- 4DSurf
</details>