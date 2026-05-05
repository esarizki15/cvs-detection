import cv2
import mediapipe as mp
import numpy as np
import time

# --- KONFIGURASI & INISIALISASI ---
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)
pose = mp_pose.Pose(min_detection_confidence=0.5)

# Indeks Mata & Pipi untuk Jarak
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
CHEEK_POINTS = [234, 454] # Titik pipi kiri & kanan untuk estimasi jarak

# --- KONSTANTA KALIBRASI ---
KNOWN_WIDTH = 15       # Lebar rata-rata wajah manusia (cm)
FOCAL_LENGTH = 500     # Nilai fokus kamera hasil kalibrasi awal
ALERT_IBI = 10         # Batas waktu tidak kedip (detik)
ALERT_DIST = 60        # Batas minimal jarak aman (cm)

# --- FUNGSI EAR ---
def calculate_ear(landmarks, eye_points):
    v1 = np.linalg.norm(np.array([landmarks[eye_points[1]].x, landmarks[eye_points[1]].y]) - 
                        np.array([landmarks[eye_points[5]].x, landmarks[eye_points[5]].y]))
    v2 = np.linalg.norm(np.array([landmarks[eye_points[2]].x, landmarks[eye_points[2]].y]) - 
                        np.array([landmarks[eye_points[4]].x, landmarks[eye_points[4]].y]))
    h = np.linalg.norm(np.array([landmarks[eye_points[0]].x, landmarks[eye_points[0]].y]) - 
                       np.array([landmarks[eye_points[3]].x, landmarks[eye_points[3]].y]))
    return (v1 + v2) / (2.0 * h)

# --- VARIABEL MONITORING ---
cap = cv2.VideoCapture(0)
blink_counter = 0
eye_closed = False
last_blink_time = time.time()

print("Sistem Berjalan... Tekan 'ESC' untuk berhenti.")

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    current_time = time.time()
    image = cv2.flip(image, 1)
    h_img, w_img, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Inferensi MediaPipe
    face_results = face_mesh.process(rgb_image)
    pose_results = pose.process(rgb_image)

    # 1. LOGIKA FACE MESH (Mata & Jarak)
    if face_results.multi_face_landmarks:
        mesh_coords = face_results.multi_face_landmarks[0].landmark
        
        # A. Deteksi Kedipan (EAR)
        ear = (calculate_ear(mesh_coords, LEFT_EYE) + calculate_ear(mesh_coords, RIGHT_EYE)) / 2
        if ear < 0.23: # Threshold sensitif
            if not eye_closed:
                blink_counter += 1
                eye_closed = True
                last_blink_time = current_time 
        else:
            eye_closed = False

        # B. Estimasi Jarak Wajah
        p1 = np.array([mesh_coords[CHEEK_POINTS[0]].x * w_img, mesh_coords[CHEEK_POINTS[0]].y * h_img])
        p2 = np.array([mesh_coords[CHEEK_POINTS[1]].x * w_img, mesh_coords[CHEEK_POINTS[1]].y * h_img])
        face_width_pixel = np.linalg.norm(p1 - p2)
        current_distance = (KNOWN_WIDTH * FOCAL_LENGTH) / face_width_pixel

        # C. Timer Alert (Idle Time)
        idle_time = current_time - last_blink_time
        
        # --- UI DISPLAY ---
        cv2.putText(image, f"Blinks: {blink_counter}", (30, 40), 1, 1.5, (0, 255, 0), 2)
        cv2.putText(image, f"Distance: {int(current_distance)} cm", (30, 80), 1, 1.5, (255, 255, 255), 2)
        cv2.putText(image, f"Idle: {int(idle_time)}s", (30, 120), 1, 1.5, (255, 255, 0), 2)

        # TRIGGER ALERT: JARAK TERLALU DEKAT
        if current_distance < ALERT_DIST:
            cv2.rectangle(image, (0, 0), (w_img, h_img), (0, 0, 255), 3)
            cv2.putText(image, "TERLALU DEKAT! MUNDUR", (w_img//4, h_img//2), 1, 2, (0, 0, 255), 3)

        # TRIGGER ALERT: MATA KERING
        if idle_time > ALERT_IBI:
            cv2.putText(image, "PERINGATAN: BERKEDIP SEKARANG!", (30, h_img - 30), 1, 1.5, (0, 0, 255), 2)

    # 2. LOGIKA POSTUR (Shoulder Alignment)
    if pose_results.pose_landmarks:
        p_landmarks = pose_results.pose_landmarks.landmark
        shoulder_diff = abs(p_landmarks[11].y - p_landmarks[12].y)
        
        if shoulder_diff > 0.05:
            cv2.putText(image, "POSTUR: MIRING", (30, 160), 1, 1.5, (0, 0, 255), 2)
        else:
            cv2.putText(image, "POSTUR: NORMAL", (30, 160), 1, 1.5, (0, 255, 0), 2)

    cv2.imshow('Advanced Computer Vision - UTS', image)
    if cv2.waitKey(5) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()