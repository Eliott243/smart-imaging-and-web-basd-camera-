import cv2
import requests
import threading
import time
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


# Default settings
DEFAULT_IP = "192.168.1.100"  # Default fallback IP


class ESP32CamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32-CAM Control Dashboard")
        self.root.geometry("1250x780")
        self.root.configure(bg="#071018")

        self.running = True
        self.auto_capture_running = False
        self.capture_count = 0

        self.x_angle = tk.IntVar(value=90)
        self.y_angle = tk.IntVar(value=90)

        self.save_folder = os.getcwd()

        self.servo_after_id = None
        self.servo_busy = False

        self.build_ui()

        self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()
        self.update_clock()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="ESP32-CAM Control Dashboard",
            font=("Segoe UI", 24, "bold"),
            bg="#071018",
            fg="#e2e8f0"
        )
        title.pack(pady=10)

        stats_frame = tk.Frame(self.root, bg="#071018")
        stats_frame.pack(pady=10)

        # IP Configuration Box
        host_frame = tk.Frame(stats_frame, bg="#111d28", padx=25, pady=10)
        host_frame.pack(side="left", padx=10)
        tk.Label(host_frame, text="Camera IP / Host", font=("Segoe UI", 9), bg="#111d28", fg="#94a3b8").pack()
        
        self.ip_entry = tk.Entry(
            host_frame, 
            font=("Segoe UI", 13, "bold"), 
            bg="#071018", 
            fg="#e2e8f0", 
            insertbackground="#e2e8f0", 
            relief="flat",
            justify="center",
            width=18
        )
        self.ip_entry.insert(0, "esp32cam.local")
        self.ip_entry.pack(pady=2)

        self.clock_label = self.stat_box(stats_frame, "Current Time", "--:--:--")
        self.capture_label = self.stat_box(stats_frame, "Capture Count", "0")

        main_frame = tk.Frame(self.root, bg="#071018")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        video_panel = tk.Frame(main_frame, bg="#111d28")
        video_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(
            video_panel,
            text="Live Camera",
            font=("Segoe UI", 16, "bold"),
            bg="#111d28",
            fg="#e2e8f0"
        ).pack(pady=10)

        self.video_label = tk.Label(video_panel, bg="black")
        self.video_label.pack(padx=15, pady=15)

        control_panel = tk.Frame(main_frame, bg="#111d28", width=420)
        control_panel.pack(side="right", fill="y", padx=10)

        tk.Label(
            control_panel,
            text="Pan and Tilt",
            font=("Segoe UI", 16, "bold"),
            bg="#111d28",
            fg="#e2e8f0"
        ).pack(pady=10)

        self.create_slider(control_panel, "Pan / X Axis", self.x_angle)
        self.create_slider(control_panel, "Tilt / Y Axis", self.y_angle)

        tk.Button(
            control_panel,
            text="Center Servos",
            font=("Segoe UI", 11, "bold"),
            bg="#5eead4",
            fg="#042f2e",
            relief="flat",
            command=self.center_servos
        ).pack(pady=8, ipadx=30, ipady=5)

        self.build_auto_capture_ui(control_panel)

        self.status_label = tk.Label(
            control_panel,
            text="Ready",
            wraplength=360,
            font=("Segoe UI", 10),
            bg="#111d28",
            fg="#94a3b8"
        )
        self.status_label.pack(pady=12)

    def build_auto_capture_ui(self, parent):
        frame = tk.Frame(parent, bg="#0f1b26", padx=20, pady=18)
        frame.pack(fill="x", padx=15, pady=12)

        top = tk.Frame(frame, bg="#0f1b26")
        top.pack(fill="x")

        tk.Label(
            top,
            text="Capture Control",
            font=("Segoe UI", 16, "bold"),
            bg="#0f1b26",
            fg="#e2e8f0"
        ).pack(side="left")

        tk.Label(
            top,
            text="Saved on this device",
            font=("Segoe UI", 10),
            bg="#12333b",
            fg="#5eead4",
            padx=14,
            pady=6
        ).pack(side="right")

        tk.Label(
            frame,
            text="Manual or scheduled captures are saved locally on your PC.",
            font=("Segoe UI", 10),
            bg="#0f1b26",
            fg="#94a3b8",
            wraplength=350,
            justify="left"
        ).pack(anchor="w", pady=(15, 12))

        btn_row = tk.Frame(frame, bg="#0f1b26")
        btn_row.pack(fill="x", pady=5)

        tk.Button(
            btn_row,
            text="Capture Now",
            font=("Segoe UI", 10, "bold"),
            bg="#5eead4",
            fg="#042f2e",
            relief="flat",
            command=self.capture_image
        ).pack(side="left", ipadx=20, ipady=7)

        tk.Button(
            btn_row,
            text="Choose Folder",
            font=("Segoe UI", 10, "bold"),
            bg="#111827",
            fg="#e2e8f0",
            relief="flat",
            command=self.choose_folder
        ).pack(side="left", padx=12, ipadx=20, ipady=7)

        grid = tk.Frame(frame, bg="#0f1b26")
        grid.pack(fill="x", pady=10)

        tk.Label(
            grid,
            text="Start Time",
            bg="#0f1b26",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            grid,
            text="Duration (minutes)",
            bg="#0f1b26",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        ).grid(row=0, column=1, sticky="w", padx=(15, 0))

        now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.start_time_entry = tk.Entry(
            grid,
            font=("Segoe UI", 10),
            bg="#071018",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat"
        )
        self.start_time_entry.insert(0, now_text)
        self.start_time_entry.grid(row=1, column=0, sticky="ew", pady=5, ipady=8)

        self.duration_entry = tk.Entry(
            grid,
            font=("Segoe UI", 10),
            bg="#071018",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat"
        )
        self.duration_entry.insert(0, "10")
        self.duration_entry.grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=5, ipady=8)

        tk.Label(
            grid,
            text="Interval (seconds)",
            bg="#0f1b26",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        ).grid(row=2, column=0, sticky="w", pady=(10, 0))

        tk.Label(
            grid,
            text="Quick Start",
            bg="#0f1b26",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        ).grid(row=2, column=1, sticky="w", padx=(15, 0), pady=(10, 0))

        self.interval_entry = tk.Entry(
            grid,
            font=("Segoe UI", 10),
            bg="#071018",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat"
        )
        self.interval_entry.insert(0, "30")
        self.interval_entry.grid(row=3, column=0, sticky="ew", pady=5, ipady=8)

        tk.Button(
            grid,
            text="Start From Now",
            font=("Segoe UI", 10, "bold"),
            bg="#fbbf24",
            fg="#221700",
            relief="flat",
            command=self.start_from_now
        ).grid(row=3, column=1, sticky="ew", padx=(15, 0), pady=5, ipady=8)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        bottom_row = tk.Frame(frame, bg="#0f1b26")
        bottom_row.pack(fill="x", pady=8)

        tk.Button(
            bottom_row,
            text="Start Schedule",
            font=("Segoe UI", 10, "bold"),
            bg="#5eead4",
            fg="#042f2e",
            relief="flat",
            command=self.start_auto_capture
        ).pack(side="left", ipadx=18, ipady=7)

        tk.Button(
            bottom_row,
            text="Stop Schedule",
            font=("Segoe UI", 10, "bold"),
            bg="#a85568",
            fg="#1f050b",
            relief="flat",
            command=self.stop_auto_capture
        ).pack(side="left", padx=12, ipadx=18, ipady=7)

        self.folder_label = tk.Label(
            frame,
            text=f"Ready. Captures will be saved to: {self.save_folder}",
            wraplength=350,
            bg="#0f1b26",
            fg="#94a3b8",
            font=("Segoe UI", 10),
            justify="left"
        )
        self.folder_label.pack(anchor="w", pady=(8, 0))

    def stat_box(self, parent, title, value):
        frame = tk.Frame(parent, bg="#111d28", padx=25, pady=10)
        frame.pack(side="left", padx=10)

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 9),
            bg="#111d28",
            fg="#94a3b8"
        ).pack()

        label = tk.Label(
            frame,
            text=value,
            font=("Segoe UI", 13, "bold"),
            bg="#111d28",
            fg="#e2e8f0"
        )
        label.pack()

        return label

    def create_slider(self, parent, title, variable):
        frame = tk.Frame(parent, bg="#09111a", padx=15, pady=12)
        frame.pack(fill="x", padx=20, pady=8)

        value_label = tk.Label(
            frame,
            text=f"{title}: {variable.get()}°",
            font=("Segoe UI", 11, "bold"),
            bg="#09111a",
            fg="#5eead4"
        )
        value_label.pack(anchor="w")

        slider = ttk.Scale(
            frame,
            from_=0,
            to=180,
            orient="horizontal",
            variable=variable,
            command=lambda value: self.slider_changed(value_label, title, variable)
        )
        slider.pack(fill="x", pady=8)

    def get_url(self, type):
        ip = self.ip_entry.get().strip()
        if not ip: ip = "esp32cam.local"
        
        if type == "stream": return f"http://{ip}:81/stream"
        if type == "control": return f"http://{ip}/control"
        if type == "snapshot": return f"http://{ip}/jpg"
        return ""

    def slider_changed(self, label, title, variable):
        angle = int(float(variable.get()))
        label.config(text=f"{title}: {angle}°")

        if self.servo_after_id is not None:
            self.root.after_cancel(self.servo_after_id)

        self.servo_after_id = self.root.after(100, self.send_servo_angles)

    def send_servo_angles(self):
        if self.servo_busy:
            return

        self.servo_busy = True

        x = int(self.x_angle.get())
        y = int(self.y_angle.get())

        def worker():
            try:
                requests.get(
                    self.get_url("control"),
                    params={"x": x, "y": y},
                    timeout=1.0  # Increased timeout for better reliability
                )

                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text=f"Servo updated: X={x}°, Y={y}°",
                        fg="#5eead4"
                    )
                )
            except:
                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text="Servo command failed (check IP)",
                        fg="#fda4af"
                    )
                )
            finally:
                self.servo_busy = False

        threading.Thread(target=worker, daemon=True).start()

    def center_servos(self):
        self.x_angle.set(90)
        self.y_angle.set(90)
        self.send_servo_angles()
        self.status_label.config(text="Servos centered", fg="#5eead4")

    def choose_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.save_folder = folder
            self.folder_label.config(
                text=f"Ready. Captures will be saved to: {self.save_folder}"
            )

    def capture_image(self):
        threading.Thread(target=self.capture_worker, daemon=True).start()

    def capture_worker(self):
        try:
            response = requests.get(self.get_url("snapshot"), timeout=5)

            if response.status_code == 200:
                filename = datetime.now().strftime("esp32cam_%Y-%m-%d_%H-%M-%S.jpg")
                filepath = os.path.join(self.save_folder, filename)

                with open(filepath, "wb") as file:
                    file.write(response.content)

                self.capture_count += 1

                self.root.after(
                    0,
                    lambda: self.capture_label.config(text=str(self.capture_count))
                )

                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text=f"Saved locally: {filename}",
                        fg="#5eead4"
                    )
                )
                return True

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="Capture failed",
                    fg="#fda4af"
                )
            )
            return False

        except Exception as e:
            self.root.after(
                0,
                lambda: self.status_label.config(
                    text=f"Could not capture image: {e}",
                    fg="#fda4af"
                )
            )
            return False

    def start_from_now(self):
        now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, now_text)
        self.start_auto_capture()

    def start_auto_capture(self):
        if self.auto_capture_running:
            self.status_label.config(
                text="Auto capture is already running",
                fg="#fbbf24"
            )
            return

        try:
            start_time = datetime.strptime(
                self.start_time_entry.get(),
                "%Y-%m-%d %H:%M:%S"
            )

            duration_minutes = float(self.duration_entry.get())
            interval_seconds = float(self.interval_entry.get())

            if duration_minutes <= 0 or interval_seconds <= 0:
                raise ValueError

        except:
            self.status_label.config(
                text="Invalid schedule. Use: YYYY-MM-DD HH:MM:SS",
                fg="#fda4af"
            )
            return

        self.auto_capture_running = True

        threading.Thread(
            target=self.auto_capture_loop,
            args=(start_time, duration_minutes, interval_seconds),
            daemon=True
        ).start()

        self.status_label.config(
            text="Auto capture programmed",
            fg="#5eead4"
        )

    def auto_capture_loop(self, start_time, duration_minutes, interval_seconds):
        end_time = start_time + timedelta(minutes=duration_minutes)

        while self.auto_capture_running and datetime.now() < start_time:
            remaining = int((start_time - datetime.now()).total_seconds())

            self.root.after(
                0,
                lambda r=remaining: self.status_label.config(
                    text=f"Waiting to start auto capture in {r} seconds",
                    fg="#fbbf24"
                )
            )

            time.sleep(1)

        while self.auto_capture_running and datetime.now() <= end_time:
            self.capture_worker()

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="Auto capture saved image",
                    fg="#5eead4"
                )
            )

            time.sleep(interval_seconds)

        self.auto_capture_running = False

        self.root.after(
            0,
            lambda: self.status_label.config(
                text="Auto capture finished",
                fg="#5eead4"
            )
        )

    def stop_auto_capture(self):
        self.auto_capture_running = False
        self.status_label.config(text="Auto capture stopped", fg="#fda4af")

    def video_loop(self):
        while self.running:
            url = self.get_url("stream")
            self.root.after(0, lambda: self.status_label.config(text=f"Connecting to {url}...", fg="#fbbf24"))
            
            cap = cv2.VideoCapture(url)

            if not cap.isOpened():
                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text="Could not connect. Verify IP address.",
                        fg="#fda4af"
                    )
                )
                time.sleep(2)  # Wait before retrying
                continue

            self.root.after(0, lambda: self.status_label.config(text="Connected", fg="#5eead4"))

            while self.running:
                # If IP was changed in GUI, reconnect
                if self.get_url("stream") != url:
                    break
                    
                ret, frame = cap.read()

                if ret:
                    try:
                        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                        frame = cv2.resize(frame, (640, 480))
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        image = Image.fromarray(frame)
                        photo = ImageTk.PhotoImage(image=image)

                        self.video_label.imgtk = photo
                        self.video_label.configure(image=photo)
                    except Exception as e:
                        print(f"Frame error: {e}")
                else:
                    self.root.after(0, lambda: self.status_label.config(text="Stream lost. Reconnecting...", fg="#fbbf24"))
                    break

                time.sleep(0.01)

            cap.release()
            time.sleep(1)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def close(self):
        self.running = False
        self.auto_capture_running = False
        self.root.destroy()


root = tk.Tk()
app = ESP32CamApp(root)
root.protocol("WM_DELETE_WINDOW", app.close)
root.mainloop()