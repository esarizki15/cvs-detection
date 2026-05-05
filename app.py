import cv2
import mediapipe as mp
import numpy as np
import time

# --- KONFIGURASI & INISIALISASI ---
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)
pose = mp_pose.Pose(min_detection_confidence=0.5)

# Indeks mata MediaPipe (Landmarks)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# --- FUNGSI MATEMATIKA EAR ---
def calculate_ear(landmarks, eye_points):
    # Jarak Vertikal
    v1 = np.linalg.norm(np.array([landmarks[eye_points[1]].x, landmarks[eye_points[1]].y]) - 
                        np.array([landmarks[eye_points[5]].x, landmarks[eye_points[5]].y]))
    v2 = np.linalg.norm(np.array([landmarks[eye_points[2]].x, landmarks[eye_points[2]].y]) - 
                        np.array([landmarks[eye_points[4]].x, landmarks[eye_points[4]].y]))
    # Jarak Horizontal
    h = np.linalg.norm(np.array([landmarks[eye_points[0]].x, landmarks[eye_points[0]].y]) - 
                       np.array([landmarks[eye_points[3]].x, landmarks[eye_points[3]].y]))
    return (v1 + v2) / (2.0 * h)

# --- VARIABEL MONITORING ---
cap = cv2.VideoCapture(0)
blink_counter = 0
eye_closed = False
last_blink_time = time.time()
ALERT_THRESHOLD = 10  # Detik (Bisa diubah sesuai referensi penelitian)

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

    # 1. LOGIKA MATA (CVS Detection)
    if face_results.multi_face_landmarks:
        mesh_coords = face_results.multi_face_landmarks[0].landmark
        ear = (calculate_ear(mesh_coords, LEFT_EYE) + calculate_ear(mesh_coords, RIGHT_EYE)) / 2

        # Deteksi Kedipan
        if ear < 0.22:
            if not eye_closed:
                blink_counter += 1
                eye_closed = True
                last_blink_time = current_time # Reset timer kedipan
        else:
            eye_closed = False

        # Hitung durasi sejak kedipan terakhir
        idle_time = current_time - last_blink_time
        
        # UI Monitoring Mata
        cv2.putText(image, f"Blinks: {blink_counter}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(image, f"Idle: {int(idle_time)}s", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # TRIGGER ALERT (Mata Kering)
        if idle_time > ALERT_THRESHOLD:
            cv2.rectangle(image, (0, h_img-60), (w_img, h_img), (0, 0, 255), -1)
            cv2.putText(image, "PERINGATAN: MATA KERING! SILAKAN BERKEDIP", (70, h_img-20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # 2. LOGIKA POSTUR (Ergonomics)
    if pose_results.pose_landmarks:
        p_landmarks = pose_results.pose_landmarks.landmark
        l_shld = [p_landmarks[11].x, p_landmarks[11].y]
        r_shld = [p_landmarks[12].x, p_landmarks[12].y]
        
        shoulder_diff = abs(l_shld[1] - r_shld[1])
        status_postur = "POSTURE: GOOD" if shoulder_diff < 0.05 else "POSTURE: BAD (LEANING)"
        color = (0, 255, 0) if shoulder_diff < 0.05 else (0, 0, 255)
        
        cv2.putText(image, status_postur, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Render Frame
    cv2.imshow('Advanced CV - UTS Project', image)
    if cv2.waitKey(5) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()