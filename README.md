# Vein Visualization Project

This project uses a **Raspberry Pi NoIR Camera** with **infrared illumination** to visualize human veins in real-time.  
The system leverages **OpenCV**, **CLAHE (Contrast Limited Adaptive Histogram Equalization)**, and **morphological operations** to enhance vein patterns captured under IR light.  

---

## 📌 Features
- Real-time video capture using **PiCamera2**  
- HSV-based filtering for isolating vein-colored regions  
- Contrast enhancement using **CLAHE**  
- Noise reduction via **bilateral filtering**  
- **Adaptive thresholding** and morphological processing to highlight veins  
- **Contour detection** to outline vein structures  
- Semi-transparent overlay for clear visualization  

---

## 🖥️ Requirements
- Raspberry Pi (with Raspberry Pi OS)  
- Raspberry Pi **NoIR Camera** (infrared sensitive)  
- Infrared (IR) light source for illumination  

### Software Dependencies:
Install required Python packages:
```bash
pip install opencv-python numpy picamera2
