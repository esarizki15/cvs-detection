# AI-Driven CVS & Posture Monitor: A Multimodal Approach

## Overview
Proyek ini dikembangkan untuk memenuhi output mata kuliah **Advanced Computer Vision** (Pascasarjana Teknik Informatika). Fokus utama sistem ini adalah mitigasi *Computer Vision Syndrome (CVS)* melalui pemantauan real-time terhadap dua metrik utama:

- **Blink Rate (Laju Kedipan)**
- **Shoulder Alignment (Postur Bahu)**

Di tengah meningkatnya tren kerja remote, sistem ini hadir sebagai asisten kesehatan preventif yang memanfaatkan teknik *Deep Learning* untuk menjaga kesehatan mata dan ergonomi pengguna secara otomatis.

---

## Features

- **Real-time Blink Detection**  
  Menggunakan algoritma *Eye Aspect Ratio (EAR)* untuk deteksi kedipan dengan akurasi tinggi.

- **Temporal Inactivity Alert**  
  Memberikan peringatan visual jika pengguna tidak berkedip selama lebih dari 10 detik.

- **Posture Analysis**  
  Mengestimasi kemiringan bahu menggunakan landmark tubuh untuk mencegah *Musculoskeletal Disorders (MSDs)*.

- **Low Latency Inference**  
  Implementasi ringan berbasis MediaPipe, dapat berjalan di perangkat lokal tanpa GPU diskrit.

---

## Scientific Basis

- **Blink Frequency**  
  Tsubota & Nakamori (1993) menyatakan bahwa laju kedipan menurun signifikan saat menatap layar, meningkatkan risiko mata kering.

- **Inter-Blink Interval (IBI)**  
  Bento et al. (2015) menyarankan intervensi visual jika interval kedipan melebihi 10 detik untuk menjaga stabilitas lapisan air mata.

---

## Tech Stack

- **Language**: Python 3.9+  
- **Libraries**: OpenCV, MediaPipe, NumPy  
- **Framework**: BlazeFace (Face Mesh) & BlazePose  

---

## Getting Started

### Prerequisites

- Python (Mac / Windows / Linux)  
- Webcam yang berfungsi  

---

### Installation

Clone repository:

```bash
git clone https://github.com/esarizki15/cvs-detection.git
cd cvs-detection
```

Buat dan aktifkan virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

## Running the App

```bash
python app.py
```

---

## Technical Details

Sistem menghitung **Eye Aspect Ratio (EAR)** menggunakan perbandingan jarak Euclidean antar landmark mata:

```markdown
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 ||p1 - p4||)
```

- Threshold deteksi: **0.22 – 0.25 (adaptif)**  
- Menggunakan **state machine** untuk memastikan validitas siklus kedipan  

---

## Project Structure

```
cvs-detection/
│── app.py             # Main application logic
│── requirements.txt   # List of dependencies
│── README.md          # Project documentation
│── .gitignore         # Files to ignore in git
```

---

## Future Improvements

- Integrasi notifikasi suara (audio alert)
- Logging data untuk analisis jangka panjang
- Dashboard monitoring berbasis web
- Model personalisasi berbasis user behavior

---

## Author

**Nama**: Esa Rizki Hari Utama
**Position**: Master of Data Science Student  

---

## License

This project is licensed under the MIT License.