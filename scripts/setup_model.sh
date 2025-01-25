#!/bin/bash

# Create the models directory if it doesn't exist
mkdir -p src/midas_models

# Download the model
echo "Downloading MiDaS DPT-Hybrid model..."
curl -L -o model.tar.gz \
  https://www.kaggle.com/api/v1/models/intel/midas-3.0/transformers/dpt-hybrid-midas/1/download

# Extract the model
echo "Extracting model..."
tar -xzf model.tar.gz

# Move the ONNX model to the correct location
echo "Moving model to src/midas_models..."
mv dpt-hybrid-midas.onnx src/midas_models/dpt_hybrid.onnx

# Clean up
echo "Cleaning up..."
rm -f model.tar.gz

echo "Setup complete! The model is now in src/midas_models/dpt_hybrid.onnx"
