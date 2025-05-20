# ijvMaster

This repository supports the study of factors affecting the **optimal source-detector separation (SDS) for quantifying internal jugular venous blood oxygen saturation**. The research integrates computational modeling, in-vivo experiments, medical image processing, and advanced data analysis to determine how tissue geometry and noise sources influence the optimal SDS for different subjects.

---

## Project Overview

- **Monte Carlo Simulation:**  
  Implements three-dimensional Monte Carlo tissue modeling to analyze how geometric and optical parameters affect light sensing sensitivity to the internal jugular vein (IJV). The core simulation code is located in the `mcx/` directory, which includes the MCX engine, GUI, and various simulation examples.

- **Ultrasound Image Processing:**  
  The `ultrasound_image_processing/` folder contains scripts and data for processing ultrasound images. These tools extract geometric features, such as the distance from the upper edge of the IJV to the skin surface, which is a key parameter affecting the sensitivity peak position.

- **Experimental Data Analysis:**  
  Python scripts located in the repository root (e.g., `I0_denoise_invivo.py`, `I1_analyze_stability_from_denoised_invivo.py`, etc.) handle signal denoising, noise modeling, SNR calculation, and comparison of simulation and experiment. These scripts analyze physiological and system noise, and evaluate subject-specific optimal SDS.

---

## Highlights

- **Flexible Tissue Modeling:**  
  Easily modify geometric and optical parameters to simulate a variety of physiological scenarios.

- **Noise Modeling & SNR Evaluation:**  
  Incorporates models for physiological and instrumental noise, supporting robust determination of optimal SDS.

- **End-to-End Pipeline:**  
  From ultrasound image segmentation, through simulation, to experimental validation and advanced data analysis.
