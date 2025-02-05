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

- TouchDesigner 2022.32660 or later
- Python 3.9.5+
- ONNX Runtime Library

## Installation

1. Download the required model file:
   - Download the models required: DPT Hybrid (`dpt_hybrid.onnx`)/DPT Swin2 Tiny (`dpt_swin2_tiny_256.onnx`)/midas-small (`midas-small.onnx`)/etc
   - Place it in the project directory

2. Open the TouchDesigner project:
   - Open `midas-touchdesigner.toe`
   - Click on the midas Base, go to the `Setup` parameter page, and pulse the `Install Dependencies`
   - Navigate to the `dep` folder
      - Windows Users: double click `dep_install_windows.cmd`
      - Mac Users: 
        1. Open Terminal and change directory (`cd`) to the `dep` folder
        2. For Intel Macs:
           ```bash
           chmod +x dep_install_mac_intel.sh
           ./dep_install_mac_intel.sh
           ```
        3. For Apple Silicon Macs (M1/M2):
           ```bash
           chmod +x dep_install_mac_arm.sh
           ./dep_install_mac_arm.sh
           ```
        Note: The scripts will automatically check if you're using the correct version for your Mac's architecture.
   - Back to TouchDesigner, go to the midas Base, moving to the `Runtime` parameter page and pulse `Run Paths` first then `Load MiDaS Model`
   - Now the model should be loaded and ready to use.

## Model Conversion

If you need to convert a PyTorch (.pt) model to ONNX format, you can use the provided conversion script:

1. Place your PyTorch model file in the project directory
2. Modify the `PT_MODEL_PATH` in `model_converter/pt_to_onnx.py` to point to your model file
3. Run the conversion script:
   ```bash
   python model_converter/pt_to_onnx.py
   ```
The script will generate an ONNX model file with the same name as your PT file but with the .onnx extension.


## Usage

1. Import the .tox component into your TouchDesigner project
2. Connect your input video/image source to the input TOP
3. The depth map will be output through the output TOP

## Credits

This implementation is based on the MiDaS model:
- [MiDaS GitHub Repository](https://github.com/isl-org/MiDaS)
- [ONNX Model Zoo](https://github.com/onnx/models/tree/main/vision/depth_estimation/midas)
