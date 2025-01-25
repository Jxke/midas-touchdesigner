# TDMiDaS

TDMiDaS is a user-friendly, open-source TouchDesigner component designed to integrate real-time depth estimation using MiDaS. This `.tox` file allows creators to seamlessly add depth mapping and color feed capabilities to their TouchDesigner projects with minimal setup.

## Features
- **Camera Selection**: Choose the input camera directly from the component.
- **Color and Depth Outputs**: Outputs include both the color map (camera feed) and depth map as TOPs.
- **Real-Time Performance**: Powered by MiDaS models running locally for efficient depth estimation.
- **Cross-Platform**: Works on macOS and Windows, leveraging WebAssembly for GPU acceleration where available.
- **Offline Ready**: Bundled MiDaS models and web assets ensure the component runs without an internet connection.
- **Seamless Integration**: Drag and drop the `.tox` file into your TouchDesigner project, and you're ready to go.

## Repository Structure
```
project/
├── src/            # Holds the MiDaS web assets and scripts.
├── td_scripts/     # Python scripts for TouchDesigner integration.
├── toxes/          # Contains the main TDMiDaS .tox file.
├── package.json    # Node.js configuration for the web app.
└── README.md       # Project documentation.
```

## Getting Started
### Prerequisites
- [TouchDesigner](https://derivative.ca/) (latest version recommended)
- [Node.js](https://nodejs.org/) (for building the web assets)

### Setup Instructions
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/tdmidas.git
   ```
2. Navigate to the project folder and install dependencies:
   ```bash
   cd tdmidas
   yarn install
   ```
3. Download and setup the MiDaS model:
   ```bash
   ./scripts/setup_model.sh
   ```
   Note: You'll need a Kaggle account and API key to download the model. Set up your Kaggle credentials following [these instructions](https://github.com/Kaggle/kaggle-api#api-credentials).

4. Build the MiDaS web app:
   ```bash
   yarn build
   ```
5. Open the `.tox` file in TouchDesigner (found in the `toxes` folder).

## Roadmap
- **Improved UI**: Adding more user controls and feedback mechanisms.
- **Model Options**: Support for multiple MiDaS models for varying speed/accuracy.
- **Additional Outputs**: Optionally output metadata like resolution and framerate.
- **Enhanced Cross-Platform Support**: Further optimizations for macOS and Windows.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the project.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [MiDaS](https://github.com/isl-org/MiDaS) for the depth estimation models.
- [TouchDesigner](https://derivative.ca/) for their powerful visual programming environment.
- Inspiration from [MediaPipe TouchDesigner Plugin](https://github.com/torinmb/mediapipe-touchdesigner).

---
For any questions or issues, feel free to open an issue on this repository or contact the maintainers.
