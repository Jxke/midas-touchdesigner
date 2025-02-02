"""
MiDaS loader extension for TouchDesigner
"""

import os
import onnxruntime
import numpy as np
import cv2

def onStart():
    """Initialize when script starts"""
    try:
        # Get the model path relative to the project
        model_path = project.folder + '/dep/midas_models/midas-small.onnx'
        model_path = tdu.expandPath(model_path)
        
        print(f"Project folder: {project.folder}")
        print(f"Model path: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"Error: Model not found at {model_path}")
            return
            
        print("Loading model...")
        model = onnxruntime.InferenceSession(model_path)
        input_name = model.get_inputs()[0].name
        output_name = model.get_outputs()[0].name
        print("Model loaded successfully")
        
        # Store in parent component
        parent_comp = me.parent()
        parent_comp.store('midas_model', model)
        parent_comp.store('midas_input_name', input_name)
        parent_comp.store('midas_output_name', output_name)
        print("Model stored in parent component")
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")

# Run initialization
onStart()
