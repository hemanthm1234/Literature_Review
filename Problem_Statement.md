> # `HiLite-4D`: High-Fidelity, Lightweight Surface Reconstruction for Dynamic Scenes


<div align="center">

![High Fidelity](https://img.shields.io/badge/High%20Fidelity-blue)
![4D SURFACE RECONSTRUCTION](https://img.shields.io/badge/4D%20SURFACE%20RECONSTRUCTION-orange)
![Efficient](https://img.shields.io/badge/Efficient-brightgreen)

</div>

![poster](assets/poster.png)

## 1. Introduction & Motivation
Modelling 4D dynamic scenes is of utmost importance in fields like AR/VR, digital twins, telepresence, and robotics. For these applications to be practical, the reconstructed assets must be both `computationally efficient` (capable of real-time rendering and fast optimization) and `high-fidelity` (yielding high fidelity surfaces geometry).

## 2. The Core Problem (The Gap)

Existing works which focus on High Fidelity reconstruction use a lot of Gaussians and are compute intensive. Papers that focus on improving speed generally opt for pruning techniques that lead to bad surface reconstruction.

## 3. Goal

Bridge the gap between Speed and Quality of surface reconstruction to enable practical usage of 4D assets on low compute devices.

## 4. Scope

Exploring various techniques for High Fidelity reconstruction like different regularisation losses, different surface representations, etc. Exploring efficiency techniques like pruning number of gaussians, different representations of motion, etc. Understanding current baselines and existing trade-off better.