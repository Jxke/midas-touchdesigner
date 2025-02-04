import os
import sys

# Import dependency management from pt_to_onnx
from pt_to_onnx import install_requirements, setup_midas

# Install requirements and setup MiDaS
install_requirements()
setup_midas()

# Now we can safely import torch
import torch

# Load the model weights
model_path = "dep/midas_models/.pt/dpt_swin2_tiny_256.pt"
state_dict = torch.load(model_path, map_location=torch.device('cpu'))

# Print all layer shapes from checkpoint
print("\nCheckpoint layers:")
for key, value in state_dict.items():
    if isinstance(value, torch.Tensor):
        print(f"{key}: {value.shape}")

print("\nOutput conv layers:")
for key, value in state_dict.items():
    if isinstance(value, torch.Tensor) and 'output_conv' in key:
        print(f"{key}: {value.shape}")
