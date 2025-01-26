# MiDaS TouchDesigner Integration
 
A TouchDesigner component (.tox) that implements the MiDaS depth estimation model using ONNX runtime.

## Overview

This project provides a TouchDesigner implementation of the MiDaS depth estimation model, allowing real-time depth estimation directly within TouchDesigner. The implementation uses ONNX runtime for efficient inference.

## Project Structure

```
├── td_scripts/          # Python scripts for TouchDesigner integration
├── dep/                 # Dependencies
│   └── python/         # Python dependencies
├── toxes/              # TouchDesigner components
└── midas-touchdesigner.toe  # Main TouchDesigner project file
```

## Requirements

- TouchDesigner 2022.28160 or later
- Python 3.7+
- ONNX Runtime

## Installation

1. Download the required model file:
   - Download the DPT Hybrid model (`dpt_hybrid.onnx`)
   - Place it in the project directory

2. Open the TouchDesigner project:
   - Open `midas-touchdesigner.toe`
   - The component is ready to use

## Usage

1. Import the .tox component into your TouchDesigner project
2. Connect your input video/image source to the input TOP
3. The depth map will be output through the output TOP

## Credits

This implementation is based on the MiDaS model:
- [MiDaS GitHub Repository](https://github.com/isl-org/MiDaS)
- [ONNX Model Zoo](https://github.com/onnx/models/tree/main/vision/depth_estimation/midas)
