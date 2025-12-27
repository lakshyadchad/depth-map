# 🗺️ Depth Map Generator

Transform your images into depth maps using AI! This tool analyzes photos and creates grayscale depth maps showing how far objects are from the camera.

![Depth Map Example](https://raw.githubusercontent.com/isl-org/MiDaS/master/figures/monodepth.png)

## 🎯 What Does This Do?

This Python script takes regular photos and generates **depth maps** - images where brightness represents distance:
- **Bright/White pixels** = Objects close to the camera
- **Dark/Black pixels** = Objects far from the camera

### Real-World Example:
```
Input Image:              Depth Map Output:
🏔️ Mountain (far)   →    🖤 Dark Gray
🌳 Trees (medium)   →    ⚪ Light Gray  
👤 Person (close)   →    ⬜ White
```

---

## 🚀 How to Use

### 1️⃣ Install Requirements
First, install the necessary Python packages:
```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install torch torchvision opencv-python matplotlib
```

### 2️⃣ Set Your Paths
Open `generate_depth.py` and edit these lines:
```python
dataset_folder = r"C:\your\images\folder"  # Your input images
output_folder = r"C:\your\output\folder"   # Where to save depth maps
```

### 3️⃣ Run the Script
```bash
python generate_depth.py
```

### 4️⃣ Wait and Done! ✨
The script will:
- Find all images in your input folder (including subfolders)
- Process each image using the MiDaS AI model
- Save depth maps with the same filename and folder structure
- Show progress in the terminal

---

## 📊 What Gets Created?

### Input/Output Structure:
```
📁 Input Folder                    📁 Output Folder
├── photo1.jpg           →         ├── photo1.png (depth map)
├── photo2.png           →         ├── photo2.png (depth map)
└── 📁 vacation                    └── 📁 vacation
    ├── beach.jpg        →             ├── beach.png (depth map)
    └── sunset.jpg       →             └── sunset.png (depth map)
```

**Key Points:**
- ✅ Preserves your folder structure
- ✅ Converts all formats to `.png`
- ✅ Same filename (original extension replaced)
- ✅ Normalized to 0-255 grayscale values

---

## 🤖 Model Comparison: MiDaS_small vs DPT_Large

The script supports two AI models. Choose based on your needs:

| Feature | MiDaS_small (Current) | DPT_Large |
|---------|----------------------|-----------|
| **Speed** | ⚡ Very Fast | 🐢 Slower (3-5x) |
| **Accuracy** | ✅ Good | 🎯 Excellent |
| **GPU Memory** | 💚 Low (~2GB) | 🔴 High (~8GB) |
| **Best For** | Batch processing thousands of images | High-quality, detailed depth maps |
| **File Size** | 📦 ~100MB | 📦 ~1.2GB |

### 🔄 How to Switch Models:
Change line 11 in `generate_depth.py`:
```python
# For speed:
model_type = "MiDaS_small"

# For accuracy:
model_type = "DPT_Large"

# For balance:
model_type = "DPT_Hybrid"
```

### 📈 Performance Example:
- **1000 images** with MiDaS_small: ~15-20 minutes (with GPU)
- **1000 images** with DPT_Large: ~60-90 minutes (with GPU)

---

## 🛠️ How to Contribute & Improve

Want to make this tool even better? Here are some ideas:

### 🌟 Easy Contributions:
- [ ] Add a progress bar (using `tqdm` library)
- [ ] Create a GUI interface (using `tkinter` or `gradio`)
- [ ] Add batch size options for faster processing
- [ ] Include a config file instead of hardcoded paths
- [ ] Add colored depth maps (heatmap visualization)

### 🚀 Medium Difficulty:
- [ ] Support video depth map generation
- [ ] Add depth map quality comparison tool
- [ ] Implement multi-GPU support for faster processing
- [ ] Create before/after preview window
- [ ] Add command-line arguments (argparse)

### 💎 Advanced Features:
- [ ] 3D point cloud generation from depth maps
- [ ] Depth map refinement using multiple models
- [ ] Real-time webcam depth estimation
- [ ] Export to 3D formats (.obj, .ply)
- [ ] API/web service deployment

### 📝 How to Contribute:
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### ❌ "CUDA out of memory"
**Solution:** Switch to `MiDaS_small` or process fewer images at once

### ❌ "Could not load image"
**Solution:** Check if the image file is corrupted or in an unsupported format

### ❌ Slow processing without GPU
**Solution:** Install CUDA-enabled PyTorch: https://pytorch.org/get-started/locally/

### ❌ Import errors
**Solution:** Make sure all dependencies are installed:
```bash
pip install --upgrade torch torchvision opencv-python matplotlib
```

---

## 📄 License

This project uses the MiDaS model, which is released under the MIT license. Please refer to the [MiDaS repository](https://github.com/isl-org/MiDaS) for more details.

---

## 🙏 Acknowledgments

- **Intel ISL** for creating the MiDaS depth estimation model
- **PyTorch** for the deep learning framework
- **OpenCV** for image processing capabilities

---

## 📞 Need Help?

- Check the [MiDaS GitHub Issues](https://github.com/isl-org/MiDaS/issues)
- Review PyTorch documentation for GPU setup
- Ensure your paths use raw strings (r"path\to\folder") on Windows

---