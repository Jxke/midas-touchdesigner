// Initialize ONNX runtime
let ort;

const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('depth_map');
const canvasContext = canvasElement.getContext('2d');

// Set canvas dimensions
canvasElement.width = 640;
canvasElement.height = 480;

let session;
let modelLoaded = false;
let lastProcessingTime = 0;
const processingInterval = 50; // Process every 50ms

// Initialize ONNX runtime
async function initONNX() {
  try {
    ort = await import('onnxruntime-web');
    console.log('ONNX Runtime loaded:', ort);
    
    // Configure WASM backend
    if (ort.env && ort.env.wasm) {
      ort.env.wasm.wasmPaths = '/node_modules/onnxruntime-web/dist/';
      ort.env.wasm.proxy = false;
      ort.env.wasm.numThreads = 1;
    }
  } catch (error) {
    console.error('Error loading ONNX runtime:', error);
    throw error;
  }
}

// Initialize webcam
async function setupWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { 
        width: { ideal: 640 },
        height: { ideal: 480 }
      },
    });
    videoElement.srcObject = stream;
    return new Promise((resolve) => {
      videoElement.onloadedmetadata = () => {
        videoElement.play();
        resolve(videoElement);
      };
    });
  } catch (error) {
    console.error('Error setting up webcam:', error);
    throw error;
  }
}

// Load ONNX model
async function loadONNXModel() {
  try {
    console.log('Loading ONNX model...');
    
    // Configure ONNX runtime
    const options = {
      executionProviders: ['wasm'],
      graphOptimizationLevel: 'all',
      enableCpuMemArena: true,
      enableMemPattern: true,
      executionMode: 'sequential'
    };
    
    // Create inference session
    session = await ort.InferenceSession.create(
      './src/midas_models/dpt_hybrid.onnx',
      options
    );
    
    console.log('Model loaded successfully!');
    console.log('Model input names:', session.inputNames);
    console.log('Model output names:', session.outputNames);
    modelLoaded = true;
    return true;
  } catch (error) {
    console.error('Error loading ONNX model:', error);
    modelLoaded = false;
    throw error;
  }
}

// Process frame
async function processFrame() {
  if (!session || !modelLoaded) {
    console.warn('Model not loaded yet, skipping frame');
    return;
  }

  const currentTime = performance.now();
  if (currentTime - lastProcessingTime < processingInterval) {
    requestAnimationFrame(processFrame);
    return;
  }
  lastProcessingTime = currentTime;

  try {
    // Draw video frame to canvas
    const offscreenCanvas = document.createElement('canvas');
    const offscreenContext = offscreenCanvas.getContext('2d');
    offscreenCanvas.width = 384;
    offscreenCanvas.height = 384;
    offscreenContext.drawImage(videoElement, 0, 0, 384, 384);

    // Get image data
    const imageData = offscreenContext.getImageData(0, 0, 384, 384);
    const inputData = new Float32Array(1 * 3 * 384 * 384);
    
    // Normalize and transpose image (HWC -> NCHW)
    for (let y = 0; y < 384; y++) {
      for (let x = 0; x < 384; x++) {
        const pixelIndex = (y * 384 + x) * 4;
        const r = imageData.data[pixelIndex] / 255.0;
        const g = imageData.data[pixelIndex + 1] / 255.0;
        const b = imageData.data[pixelIndex + 2] / 255.0;
        
        inputData[0 * 384 * 384 + y * 384 + x] = r;
        inputData[1 * 384 * 384 + y * 384 + x] = g;
        inputData[2 * 384 * 384 + y * 384 + x] = b;
      }
    }

    // Create tensor
    const inputTensor = new ort.Tensor('float32', inputData, [1, 3, 384, 384]);
    const feeds = { 'input': inputTensor };

    // Run inference
    const outputMap = await session.run(feeds);
    const outputData = outputMap[session.outputNames[0]].data;

    // Render depth map
    renderDepthMap(outputData);
    requestAnimationFrame(processFrame);
  } catch (error) {
    console.error('Error processing frame:', error);
  }
}

// Render depth map
function renderDepthMap(depthMapData) {
  // Find min and max for normalization
  let min = Infinity;
  let max = -Infinity;
  for (let i = 0; i < depthMapData.length; i++) {
    min = Math.min(min, depthMapData[i]);
    max = Math.max(max, depthMapData[i]);
  }
  
  const range = max - min;
  const imageData = canvasContext.createImageData(384, 384);

  // Apply colormap (using turbo colormap for better visualization)
  for (let i = 0; i < depthMapData.length; i++) {
    // Normalize depth value to 0-1 range and invert (closer is brighter)
    const normalizedDepth = 1.0 - ((depthMapData[i] - min) / range);
    
    // Apply a gamma correction for better contrast
    const gamma = 0.7;
    const correctedDepth = Math.pow(normalizedDepth, gamma);
    
    // Convert to RGB (simple blue-red gradient)
    const r = Math.floor(correctedDepth * 255);
    const g = 0;
    const b = Math.floor((1 - correctedDepth) * 255);
    
    imageData.data[i * 4 + 0] = r;
    imageData.data[i * 4 + 1] = g;
    imageData.data[i * 4 + 2] = b;
    imageData.data[i * 4 + 3] = 255;
  }

  // Clear canvas
  canvasContext.clearRect(0, 0, canvasElement.width, canvasElement.height);
  
  // Create temporary canvas for resizing
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = 384;
  tempCanvas.height = 384;
  const tempContext = tempCanvas.getContext('2d');
  
  // Put the depth map on the temporary canvas
  tempContext.putImageData(imageData, 0, 0);
  
  // Apply slight blur for smoother visualization
  canvasContext.filter = 'blur(1px)';
  
  // Draw the temporary canvas onto the main canvas, scaling it up
  canvasContext.drawImage(tempCanvas, 0, 0, 384, 384, 0, 0, canvasElement.width, canvasElement.height);
  
  // Reset filter
  canvasContext.filter = 'none';
}

// Main function
async function main() {
  try {
    console.log('Starting application...');
    await initONNX();
    await setupWebcam();
    console.log('Webcam setup complete');
    await loadONNXModel();
    console.log('Starting frame processing');
    processFrame();
  } catch (error) {
    console.error('Error in main:', error);
  }
}

main();
