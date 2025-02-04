# Model Converter

This directory contains scripts for converting and inspecting MiDaS models.

## Requirements

- Python 3.x
- Git (for cloning MiDaS repository)

All other dependencies (PyTorch, ONNX) will be automatically installed when running the scripts.

## Scripts

### pt_to_onnx.py

Converts PyTorch models (.pt) to ONNX format for use in TouchDesigner.

Usage:
```bash
python pt_to_onnx.py
```

The script will:
1. Load a DPT-Swin2 PyTorch model from `dep/midas_models/.pt/`
2. Convert it to ONNX format
3. Save the converted model to `dep/midas_models/`

### inspect_model.py

Utility script to inspect model layer shapes and configurations.

Usage:
```bash
python inspect_model.py
```

This will print out:
- All layer shapes from the checkpoint
- Output convolution layer details

## Note

The scripts will automatically:
1. Install required Python packages if they're not present
2. Clone the MiDaS repository into the `model_converter/MiDaS` directory if it doesn't exist
3. Add the MiDaS package to the Python path

The MiDaS directory is git-ignored, so it won't be tracked in version control.
