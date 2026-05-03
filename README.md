# Security Analysis and Performance Evaluation of Facial Biometry-Based Symmetric Key Generation for IoT Peer-to-Peer Communication

This repository contains a simplified reproducibility-oriented implementation of the biometric key-generation workflow described in the manuscript on facial-biometry-based symmetric key generation for IoT peer-to-peer communication.

The repository was prepared to make external verification easier. In this version, the scripts read biometric information directly from face images, so the pipeline can be executed in a standard environment without requiring the original mobile application. Users may also add their own images to the `images/` directory and test whether the key-generation process works on new biometric inputs.

## Repository structure

- `codes/` – Python scripts implementing the main stages of the experimental workflow.
- `images/` – example face images used as input for verification and testing.

## Files in `codes/`

- `face2_zmieniony.py`  
  Core implementation of the key-generation logic, including coordinate transformation, binary conversion, iterative processing, and export of generated keys.

- `extract_key_from_faces2.py`  
  Script for extracting facial landmark points from face images and generating a symmetric key from two input images.

- `main.py`  
  Experimental runner for repeated-session and multi-device simulations, including CSV logging and generation of timing statistics and basic plots.

- `gen_key.py`  
  Auxiliary analysis script used to evaluate how the number of processing rounds affects selected key properties, including entropy, diffusion, collision rate, and processing time.

- `image_mods.py`  
  Utility script for generating modified versions of input images (brightness change, blur, noise, rotation) in order to test the robustness of facial-feature extraction and the corresponding effect on key generation.

## Purpose of the repository

The purpose of this repository is not to provide a full production-ready application, but rather to make the key-generation concept easier to verify, inspect, and test. The provided scripts allow users to:

- reproduce the main stages of the proposed key-generation pipeline,
- test the method on example images,
- add their own face images to the `images/` folder,
- observe whether the extracted biometric data can be used to generate keys,
- analyse selected properties of the generated keys.

## Basic usage

1. Place example or custom face images in the `images/` directory.
2. Run the scripts from the `codes/` directory, depending on the test you want to perform:
   - use `extract_key_from_faces.py` to derive a key from two images,
   - use `main.py` to run repeated experiments and generate CSV outputs,
   - use `gen_key.py` to analyse entropy, diffusion, collision rate, and runtime,
   - use `image_mods.py` to create modified images for robustness testing.
3. Inspect the generated CSV files and plots.

## Reproducibility note

For simplified verification, this repository version reads facial biometric data directly from images. This makes it possible to test the key-generation aspect of the method in a standard computational environment, without reproducing the original mobile capture interface.

## Note

The repository is intended as a reproducibility supplement to the manuscript. It focuses on the key-generation workflow and related verification scripts rather than on the complete end-user application.
