import os
import sys
import subprocess
import importlib.util

def install_requirements():
    """Install required packages if they're not already installed."""
    required_packages = ['torch', 'onnx', 'git']
    for package in required_packages:
        if package == 'git':
            # Check if git is installed
            try:
                subprocess.run(['git', '--version'], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                print(f'Error: git is not installed. Please install git first.')
                sys.exit(1)
            continue
            
        if importlib.util.find_spec(package) is None:
            print(f'Installing {package}...')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def setup_midas():
    """Clone or update MiDaS repository if needed."""
    midas_dir = os.path.join(os.path.dirname(__file__), 'MiDaS')
    midas_url = 'https://github.com/isl-org/MiDaS.git'

    if not os.path.exists(midas_dir):
        print('Cloning MiDaS repository...')
        subprocess.run(['git', 'clone', midas_url, midas_dir], check=True)
    else:
        print('MiDaS repository already exists.')

    # Add MiDaS to Python path
    if midas_dir not in sys.path:
        sys.path.append(midas_dir)

# Install requirements and setup MiDaS
install_requirements()
setup_midas()

# Now we can safely import torch
import torch

def convert_pt_to_onnx(pt_model_path, output_dir='dep/midas_models'):
    """
    Convert a DPT-Swin2 PyTorch model (.pt) to ONNX format.
    """
    if not os.path.exists(pt_model_path):
        raise FileNotFoundError(f"Model file not found: {pt_model_path}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model_name = os.path.splitext(os.path.basename(pt_model_path))[0] + ".onnx"
    onnx_model_path = os.path.join(output_dir, model_name)

    print(f"Loading PyTorch model from {pt_model_path}")

    from midas.dpt_depth import DPTDepthModel

    # Create DPTDepthModel with correct backbone & features
    model = DPTDepthModel(
        path=None,
        backbone="swin2t16_256",
        non_negative=True,
        features=256,  # Match the checkpoint's feature dimensions
        head_features_1=256,  # Match the checkpoint's head dimensions
        head_features_2=32,  # Match the checkpoint's head dimensions
    )
    model.eval()

    # Load checkpoint
    state_dict = torch.load(pt_model_path, map_location=torch.device('cpu'))

    # Load the state dict directly without modifications
    try:
        model.load_state_dict(state_dict)
    except Exception as e:
        print(f"Error during loading state dict: {str(e)}")
        raise e

    # Export to ONNX
    try:
        # Create dummy input
        x = torch.randn(1, 3, 256, 256)

        # Export the model
        print(f"Exporting model to {onnx_model_path}")
        torch.onnx.export(
            model,
            x,
            onnx_model_path,
            opset_version=13,
            input_names=['input'],
            output_names=['depth'],
            dynamic_axes={
                'input': {0: 'batch_size'},
                'depth': {0: 'batch_size'}
            }
        )
        print("Export successful!")
    except Exception as e:
        print(f"Error during ONNX export: {str(e)}")
        raise e

if __name__ == "__main__":
    PT_MODEL_PATH = "dep/midas_models/.pt/dpt_swin2_tiny_256.pt"
    OUTPUT_DIR = "dep/midas_models"

    try:
        convert_pt_to_onnx(PT_MODEL_PATH, OUTPUT_DIR)
    except Exception as e:
        print(f"Error: {str(e)}")
        convert_pt_to_onnx(PT_MODEL_PATH, OUTPUT_DIR)
    except Exception as e:
        print(f"Error during conversion: {e}")
