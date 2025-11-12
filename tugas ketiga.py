import cv2
import numpy as np
import time
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from plyer import notification
import platform
import os
import mediapipe as mp

# === Tambahan untuk suara ===
if platform.system() == "Windows":
    import winsound
    import pygame
else:
    import pygame

# === MediaPipe Setup ===
mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# === Parameter Awal ===
batas_tanpa_mata = 3.0
EAR_THRESHOLD = 0.22
running = False
last_eye_time = time.time()
alert_active = False
selected_resolution = (640, 480)
ringtone_path = None
is_expanded = False
drowsy_count = 0
drowsy_flag = False
max_drowsy = 5
max_alert_active = False

# === Password Developer ===
DEVELOPER_PASSWORD = "1234"  # 🔒 Ganti password di sini


# === Simpan & Muat Posisi dan Mode ===
def save_position(x, y):
    with open("position.txt", "w") as f:
        f.write(f"{x},{y}")

def load_position():
    if os.path.exists("position.txt"):
        try:
            with open("position.txt", "r") as f:
                x, y = map(int, f.read().strip().split(","))
                return x, y
        except:
            pass
    return 1250, 650

def save_mode():
    with open("mode.txt", "w") as f:
        f.write(mode_developer.get())

def load_mode():
    if os.path.exists("mode.txt"):
        try:
            with open("mode.txt", "r") as f:
                mode = f.read().strip()
                if mode in ["user", "developer"]:
                    return mode
        except:
            pass
    return "user"

# === Fungsi suara peringatan ===
def play_alert_sound(loop=False):
    global ringtone_path
    try:
        pygame.mixer.init()
        if ringtone_path and os.path.exists(ringtone_path):
            pygame.mixer.music.load(ringtone_path)
            pygame.mixer.music.play(-1 if loop else 0)
        else:
            if platform.system() == "Windows":
                if loop:
                    def beep_loop():
                        while max_alert_active:
                            winsound.Beep(800, 300)
                            time.sleep(0.2)
                    threading.Thread(target=beep_loop, daemon=True).start()
                else:
                    for _ in range(3):
                        winsound.Beep(800, 200)
                        time.sleep(0.1)
    except Exception as e:
        print("[ERROR] Gagal memutar nada dering:", e)

def stop_alert_sound():
    global max_alert_active
    max_alert_active = False
    try:
        pygame.mixer.music.stop()
    except:
        pass

def show_notification_once():
    global alert_active
    if not alert_active:
        alert_active = True
        notification.notify(
            title="⚠️ Peringatan: Kamu Mengantuk!",
            message="Mata tertutup lebih dari waktu yang ditentukan!",
            timeout=5,
            app_name="Deteksi Ngantuk"
        )
        play_alert_sound()

def show_max_notification():
    global max_alert_active
    if not max_alert_active:
        max_alert_active = True
        notification.notify(
            title="🚨 Bahaya! Batas Ngantuk Tercapai!",
            message="Segera istirahat. Sistem akan berbunyi terus hingga dihentikan.",
            timeout=10,
            app_name="Deteksi Ngantuk"
        )
        print("[ALERT] Batas maksimum ngantuk tercapai!")
        play_alert_sound(loop=True)

# === EAR (Eye Aspect Ratio) ===
def eye_aspect_ratio(landmarks, eye_indices):
    A = np.linalg.norm(np.array(landmarks[eye_indices[1]]) - np.array(landmarks[eye_indices[5]]))
    B = np.linalg.norm(np.array(landmarks[eye_indices[2]]) - np.array(landmarks[eye_indices[4]]))
    C = np.linalg.norm(np.array(landmarks[eye_indices[0]]) - np.array(landmarks[eye_indices[3]]))
    return (A + B) / (2.0 * C)

# === Deteksi Ngantuk ===
def detect_drowsiness():
    global running, last_eye_time, alert_active, drowsy_count, drowsy_flag, max_drowsy
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, selected_resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, selected_resolution[1])

    print(f"[INFO] Resolusi kamera: {selected_resolution}")
    print(f"[INFO] Mode: {mode_developer.get().capitalize()}")
    print(f"[INFO] Batas maksimum ngantuk: {max_drowsy}")

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)
            eyes_open = False

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    h, w, _ = frame.shape
                    landmarks = [(int(p.x * w), int(p.y * h)) for p in face_landmarks.landmark]
                    left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
                    right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
                    ear = (left_ear + right_ear) / 2.0
                    eyes_open = ear > EAR_THRESHOLD

                    state = "OPEN" if eyes_open else "CLOSED"
                    color = (0, 255, 0) if eyes_open else (0, 0, 255)
                    cv2.putText(frame, f"Mata: {state}", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            if eyes_open:
                last_eye_time = time.time()
                alert_active = False
                drowsy_flag = False
            else:
                waktu_tanpa_mata = time.time() - last_eye_time
                if waktu_tanpa_mata >= batas_tanpa_mata:
                    cv2.putText(frame, "NGANTUK !!!", (100, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    show_notification_once()
                    if not drowsy_flag:
                        drowsy_count += 1
                        print(f"[INFO] Jumlah ngantuk: {drowsy_count}")
                        drowsy_flag = True
                        if drowsy_count >= max_drowsy:
                            show_max_notification()

            cv2.putText(frame, f"Jumlah Ngantuk: {drowsy_count}/{max_drowsy}", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

            cv2.imshow("Deteksi Ngantuk (MediaPipe)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    stop_alert_sound()
    print("[INFO] Deteksi dihentikan.")

# === GUI ===
root = tk.Tk()
root.title("Deteksi Ngantuk v9 (Mode User/Developer)")
root.overrideredirect(True)
root.configure(bg="#2b2b2b")
root.attributes("-topmost", True)

# === Variabel GUI ===
mode_developer = tk.StringVar(value="user")

pos_x, pos_y = load_position()
root.geometry(f"70x70+{pos_x}+{pos_y}")

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    new_x = root.winfo_x() + deltax
    new_y = root.winfo_y() + deltay
    root.geometry(f"+{new_x}+{new_y}")
    save_position(new_x, new_y)

root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", do_move)

frame_main = tk.Frame(root, bg="#2b2b2b", bd=2, relief="ridge")
frame_main.pack(fill="both", expand=True)

# === Fungsi kontrol ===
def start_detection():
    global running, batas_tanpa_mata, max_drowsy
    if not running:
        batas_tanpa_mata = float(scale_drowsy_time.get())
        max_drowsy = int(scale_max_drowsy.get())
        running = True
        threading.Thread(target=detect_drowsiness, daemon=True).start()

def stop_detection():
    global running
    running = False
    stop_alert_sound()

def exit_app():
    global running
    running = False
    stop_alert_sound()
    save_mode()
    root.destroy()

def choose_ringtone():
    global ringtone_path
    file_path = filedialog.askopenfilename(
        title="Pilih Nada Dering",
        filetypes=[("Audio Files", "*.mp3 *.wav"), ("Semua File", "*.*")]
    )
    if file_path:
        ringtone_path = file_path
        lbl_ringtone.config(text=f"🎵 {os.path.basename(file_path)}")

def set_resolution_and_start():
    global selected_resolution
    res_str = selected_res_str.get()
    w, h = map(int, res_str.split('x'))
    selected_resolution = (w, h)
    start_detection()

# === Tambahan: Verifikasi Password ===
def verify_password():
    win = tk.Toplevel(root)
    win.title("Verifikasi Password Developer")
    win.geometry("300x150")
    win.config(bg="#2b2b2b")
    win.grab_set()
    tk.Label(win, text="Masukkan Password Developer:", bg="#2b2b2b", fg="white").pack(pady=10)
    entry = tk.Entry(win, show="*", width=25)
    entry.pack(pady=5)
    def confirm():
        if entry.get() == DEVELOPER_PASSWORD:
            messagebox.showinfo("Akses Diterima", "Mode Developer aktif.")
            win.destroy()
        else:
            messagebox.showerror("Salah", "Password salah! Kembali ke mode User.")
            mode_developer.set("user")
            win.destroy()
    tk.Button(win, text="OK", bg="#4CAF50", fg="white", command=confirm).pack(pady=10)

# === Panel utama ===
is_expanded = False

def toggle_panel():
    global is_expanded
    if is_expanded:
        for widget in frame_main.winfo_children():
            widget.place_forget()
        toggle_btn.place(x=10, y=10, width=50, height=50)
        root.geometry(f"70x70+{root.winfo_x()}+{root.winfo_y()}")
        is_expanded = False
    else:
        frame_main.config(bg="#2b2b2b")
        root.geometry(f"320x460+{root.winfo_x()}+{root.winfo_y()}")
        toggle_btn.place(x=260, y=10, width=50, height=50)

        tk.Label(frame_main, text="Mode:", bg="#2b2b2b", fg="white").place(x=40, y=20)
        mode_menu = tk.OptionMenu(frame_main, mode_developer, "user", "developer",
                                  command=lambda m: verify_password() if m == "developer" else save_mode())
        mode_menu.place(x=120, y=15, width=120)

        tk.Label(frame_main, text="🧠 Deteksi Ngantuk", font=("Arial", 14, "bold"),
                 bg="#2b2b2b", fg="white").place(x=60, y=50)

        if mode_developer.get() == "developer":
            tk.Label(frame_main, text="Resolusi:", bg="#2b2b2b", fg="white").place(x=40, y=90)
            res_combo.place(x=120, y=90, width=140)

            tk.Label(frame_main, text="Nada Dering:", bg="#2b2b2b", fg="white").place(x=40, y=130)
            choose_btn.place(x=150, y=130)
            lbl_ringtone.place(x=40, y=160)

            tk.Label(frame_main, text="Waktu Ngantuk (detik):", bg="#2b2b2b", fg="white").place(x=40, y=200)
            scale_drowsy_time.place(x=190, y=195, width=80)

            tk.Label(frame_main, text="Maks. Ngantuk:", bg="#2b2b2b", fg="white").place(x=40, y=240)
            scale_max_drowsy.place(x=190, y=235, width=80)

            start_btn.place(x=60, y=330, width=90)
            stop_btn.place(x=170, y=330, width=90)
            exit_btn.place(x=115, y=380, width=90)
        else:
            # === Tombol di tengah untuk mode user ===
            start_btn.place(x=115, y=200, width=90)
            stop_btn.place(x=115, y=260, width=90)
            exit_btn.place(x=115, y=320, width=90)

        is_expanded = True

toggle_btn = tk.Button(frame_main, text="⚙️", font=("Arial", 14, "bold"),
                       bg="#3c3f41", fg="white", relief="flat", command=toggle_panel)
toggle_btn.place(x=10, y=10, width=50, height=50)

# === Elemen GUI ===
res_options = ["640x480", "800x600", "1280x720"]
selected_res_str = tk.StringVar(value=res_options[0])
res_combo = tk.OptionMenu(frame_main, selected_res_str, *res_options)
choose_btn = tk.Button(frame_main, text="Pilih File", bg="#2196F3", fg="white", command=choose_ringtone)
lbl_ringtone = tk.Label(frame_main, text="(belum dipilih)", bg="#2b2b2b", fg="white")

scale_drowsy_time = tk.Scale(frame_main, from_=1, to=10, orient="horizontal",
                             bg="#2b2b2b", fg="white", troughcolor="#555",
                             highlightthickness=0, resolution=0.5)
scale_drowsy_time.set(3.0)

scale_max_drowsy = tk.Scale(frame_main, from_=1, to=20, orient="horizontal",
                            bg="#2b2b2b", fg="white", troughcolor="#555",
                            highlightthickness=0, resolution=1)
scale_max_drowsy.set(5)

start_btn = tk.Button(frame_main, text="Start", bg="#4CAF50", fg="white", command=set_resolution_and_start)
stop_btn = tk.Button(frame_main, text="Stop", bg="#f44336", fg="white", command=stop_detection)
exit_btn = tk.Button(frame_main, text="Exit", bg="#555", fg="white", command=exit_app)

root.mainloop()
