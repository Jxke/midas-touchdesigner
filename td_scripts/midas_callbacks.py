# Import required modules
import numpy as np
import cv2

# Global debug mode flag
debugMode = False

def setDebugMode(mode):
    """Set the global debug mode"""
    global debugMode
    debugMode = mode

def process_frame(scriptOp, img):
    """Process a single frame through MiDaS"""
    try:
        # Get model from parent
        parent_comp = scriptOp.parent()
        model = parent_comp.fetch('midas_model')
        input_name = parent_comp.fetch('midas_input_name')
        output_name = parent_comp.fetch('midas_output_name')
        
        if model is None:
            if debugMode:
                print("Error: Model not loaded")
            return img
            
        # Save original dimensions
        original_height, original_width = img.shape[:2]
        
        # Ensure input is float32 and normalized
        if img.dtype != np.float32:
            img = img.astype(np.float32)
        if img.max() > 1.0:
            img = img / 255.0
            
        # Resize to model input size (256x256)
        img = cv2.resize(img, (256, 256))
        
        # Keep only RGB channels if RGBA
        if img.shape[2] == 4:
            img = img[:, :, :3]
            
        # Convert to CHW format and add batch dimension
        img = img.transpose(2, 0, 1)[None, ...]
        
        if debugMode:
            print(f"Input shape before inference: {img.shape}")
        
        # Run inference
        depth = model.run([output_name], {input_name: img})[0]
        
        if debugMode:
            print(f"Output shape after inference: {depth.shape}")
        
        # Post-process depth map
        depth = depth.squeeze()
        
        # Resize back to original size
        depth = cv2.resize(depth, (original_width, original_height))
        
        # Normalize depth for visualization
        depth = (depth - depth.min()) / (depth.max() - depth.min())
        
        # Convert to RGB format for display
        depth = np.stack([depth] * 3, axis=-1)
        
        if debugMode:
            print(f"Final output shape: {depth.shape}")
            
        return depth.astype(np.float32)
        
    except Exception as e:
        if debugMode:
            print(f"Error processing frame: {str(e)}")
        return img

def cook(scriptOp):
    """Called when TouchDesigner cooks the operator"""
    try:
        # Get input image
        img = scriptOp.inputs[0].numpyArray()
        if debugMode:
            print(f"Input image shape: {img.shape}")
        
        # Process through MiDaS
        depth = process_frame(scriptOp, img)
        
        # Set output
        scriptOp.copyNumpyArray(depth)
        
    except Exception as e:
        print(f"Error in cook: {str(e)}")