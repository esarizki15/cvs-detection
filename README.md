# AI-Driven CVS & Posture Monitor

### Real-Time Computer Vision System for Computer Vision Syndrome (CVS) Prevention

## Overview

AI-Driven CVS & Posture Monitor merupakan sistem berbasis Computer Vision yang dirancang untuk membantu mendeteksi risiko **Computer Vision Syndrome (CVS)** secara real-time menggunakan webcam standar.

Sistem memanfaatkan model pretrained dari MediaPipe untuk melakukan analisis visual terhadap perilaku pengguna komputer melalui pendekatan landmark-based monitoring, meliputi:

* Deteksi laju kedipan mata (*blink rate*)
* Estimasi jarak wajah ke layar monitor
* Analisis postur bahu
* Peringatan visual ergonomis secara real-time

Project ini dikembangkan sebagai implementasi mata kuliah **Advanced Computer Vision** pada Program Pascasarjana Teknik Informatika Universitas Pamulang.

---

# Full Research Report

Laporan penelitian lengkap dapat diakses melalui link berikut:

[View Full Research Report](https://docs.google.com/document/d/1PUmUg0opMD3qEety40Sjh8DKpqbVUSDB_2ww4GW-3eE/edit?usp=drive_link)

---

# Demo

## Normal Condition

![Normal](assets/normal.png)

Sistem berhasil mendeteksi kondisi pengguna dalam keadaan normal tanpa pelanggaran ambang batas ergonomis.

---

## Alert Condition

![Alert](assets/alert.png)

Sistem memberikan peringatan visual secara real-time ketika terdeteksi:

* Jarak wajah terlalu dekat dengan layar
* Pengguna terlalu lama tidak berkedip
* Postur tubuh tidak ergonomis

---

# Features

## 1. Real-Time Blink Detection

Menggunakan metode **Eye Aspect Ratio (EAR)** untuk mendeteksi aktivitas kedipan mata berdasarkan landmark wajah.

Sistem memberikan peringatan apabila pengguna terlalu lama tidak berkedip yang dapat memicu gejala *dry eye syndrome*.

---

## 2. Face-to-Screen Distance Estimation

Mengestimasi jarak wajah terhadap layar menggunakan landmark pipi dan pendekatan *pin-hole camera model*.

Sistem akan menampilkan peringatan apabila jarak pengguna terlalu dekat dengan layar monitor.

---

## 3. Ergonomic Posture Monitoring

Memantau keseimbangan posisi bahu menggunakan pose landmark dari MediaPipe Pose.

Sistem mendeteksi indikasi postur miring yang berpotensi menyebabkan ketegangan otot leher dan bahu akibat penggunaan komputer dalam durasi panjang.

---

## 4. Real-Time Visual Alerts

Memberikan overlay peringatan secara langsung pada frame video ketika kondisi berisiko terdeteksi.

Contoh peringatan:

* TERLALU DEKAT! MUNDUR
* PERINGATAN: BERKEDIP SEKARANG!
* POSTUR: MIRING

---

# AI & Deep Learning Components

Project ini memanfaatkan model Deep Learning pretrained dari MediaPipe untuk melakukan inferensi landmark wajah dan tubuh secara real-time.

Komponen yang digunakan meliputi:

* BlazeFace
* Face Mesh
* BlazePose

Landmark yang dihasilkan kemudian diproses menggunakan pendekatan rule-based behavioral analysis untuk mendeteksi indikasi Computer Vision Syndrome (CVS) dan gangguan ergonomis pengguna komputer.

---

# System Pipeline

```text
Webcam Input
      ↓
OpenCV Frame Processing
      ↓
MediaPipe Face Mesh & Pose
      ↓
Landmark Extraction
      ↓
Behavior Analysis
(EAR, Distance, Posture)
      ↓
Real-Time Alert System
```

---

# Technical Details

## Eye Aspect Ratio (EAR)

Sistem menghitung keterbukaan mata menggunakan rumus:

```text
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 ||p1 - p4||)
```

Threshold:

* EAR < 0.23 → mata dianggap tertutup

---

## Distance Estimation

Estimasi jarak wajah dilakukan menggunakan rumus:

```text
Distance = (RealWidth × FocalLength) / PixelWidth
```

Threshold:

* Distance < 60 cm → peringatan terlalu dekat

---

## Idle Blink Monitoring

Jika pengguna tidak berkedip selama lebih dari 10 detik:

* Sistem akan memberikan peringatan mata kering

---

# Tech Stack

* Python 3
* OpenCV
* MediaPipe
* NumPy

---

# Installation

Clone repository:

```bash
git clone https://github.com/esarizki15/cvs-detection.git
cd cvs-detection
```

Buat virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

# Running the Application

```bash
python app.py
```

Tekan tombol ESC untuk keluar dari aplikasi.

---

# Project Structure

```text
cvs-detection/
│
├── assets/
│   ├── normal.png
│   └── alert.png
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Limitations

* Sensitif terhadap kondisi pencahayaan rendah
* Estimasi jarak dipengaruhi posisi kamera dan kalibrasi
* Threshold EAR dapat berbeda pada tiap individu
* Belum mendukung multi-user detection

---

# Future Improvements

* Integrasi audio alert
* Logging data dan dashboard monitoring
* Adaptive threshold personalization
* Multi-user monitoring system
* Integrasi model fatigue prediction berbasis CNN/LSTM

---

# Research References

1. Dewansyah, F., Asfian, P., & Yunawati, I. (2025). Faktor yang Berhubungan dengan Computer Vision Syndrome (CVS) pada Pekerja Pengguna Komputer. *Jurnal Kesehatan dan Keselamatan Kerja Universitas Halu Oleo*, 6(2), 151–161.

2. Sugeng, S., & Nizar, T. N. (2023). Deteksi Aktivitas Mata, Mulut dan Kemiringan Kepala sebagai Fitur untuk Deteksi Kantuk Pada Pengendara Mobil. *Komputika: Jurnal Sistem Komputer*, 12(1), 83–91.

3. Suradi, A. A. M., Manguma, T. T. F., Alam, S., & Afifah, A. N. N. (2025). Deteksi dan Peringatan Jarak Wajah Otomatis Menggunakan MediaPipe dan Computer Vision untuk Kesehatan Pengguna Komputer. *JUKI: Jurnal Komputer dan Informatika*, 7(2), 127–135.

4. Zheng, Q., Wang, L., Wen, H., Ren, Y., Huang, S., Bai, F., Li, N., Craig, J. P., Tong, L., & Chen, W. (2022). Impact of incomplete blinking analyzed using a deep learning model with the Keratograph 5M in dry eye disease. *Translational Vision Science & Technology*, 11(3), 38.

5. Hidayat, M. A. N., Iriyanti, A. S., Hakim, J., Ndala, S., & Sasono, D. S. (2026). Perbandingan Efektivitas Arsitektur CNN Pada Sistem Klasifikasi Kelelahan Pada Wajah Pengemudi. *RIGGS: Journal of Artificial Intelligence and Digital Business*, 4(4), 15319–15326.

---

# Author

**Esa Rizki Hari Utama**
Master of Data Science Student
Universitas Pamulang

---

# License

This project is licensed under the MIT License.
