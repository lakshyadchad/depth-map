import cv2
import torch
import matplotlib.pyplot as plt
import os
from pathlib import Path

# 1. Load the MiDaS model
# "DPT_Large" is more accurate but slower. 
# "MiDaS_small" is faster (good for generating thousands of images).
model_type = "MiDaS_small" 

print(f"Loading {model_type} model...")
midas = torch.hub.load("intel-isl/MiDaS", model_type)  # type: ignore[no-untyped-call]

# Move model to GPU if available (much faster)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)  # type: ignore[attr-defined]
midas.eval()  # type: ignore[attr-defined] # Set to evaluation mode

# 2. Load the Transform pipeline
# MiDaS requires images to be a specific size and normalization
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")  # type: ignore[no-untyped-call]

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform  # type: ignore[attr-defined]
else:
    transform = midas_transforms.small_transform  # type: ignore[attr-defined]

# 3. Set up paths
dataset_folder = r""
output_folder = r""

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.jfif', '.webp']

# Get all image files recursively
image_files = []
for root, dirs, files in os.walk(dataset_folder):
    for file in files:
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(os.path.join(root, file))

print(f"Found {len(image_files)} images to process")

# Process each image
for idx, filename in enumerate(image_files, 1):
    print(f"Processing {idx}/{len(image_files)}: {os.path.basename(filename)}")
    
    # Load image
    img = cv2.imread(filename)
    
    # Check if image was loaded successfully
    if img is None:
        print(f"  ⚠ Skipping - Could not load image: {filename}")
        continue
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert OpenCV BGR to RGB
      # Transform and Predict
    input_batch = transform(img).to(device)
    
    with torch.no_grad(): # We don't need gradients for inference
        prediction = midas(input_batch)  # type: ignore[misc]
        
        # Resize the prediction to match the original image size
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()
    
    # Move prediction back to CPU for processing
    depth_map = prediction.cpu().numpy()
    
    # Normalize to 0 - 1 range
    depth_min = depth_map.min()
    depth_max = depth_map.max()
    normalized_depth = (depth_map - depth_min) / (depth_max - depth_min)
    
    # Create output path that preserves folder structure
    rel_path = os.path.relpath(filename, dataset_folder)
    output_path = os.path.join(output_folder, rel_path)
    
    # Create subdirectories if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Change extension to .png for depth map (no _depth suffix)
    output_path = os.path.splitext(output_path)[0] + '.png'
    
    # Save the depth map
    cv2.imwrite(output_path, (normalized_depth * 255).astype('uint8'))
    print(f"  ✓ Saved to: {output_path}")

print(f"\n✓ Completed! Processed {len(image_files)} images")
print(f"Depth maps saved in: {output_folder}")

