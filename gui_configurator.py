import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk

PROFILE_PATH = "patient_profile.json"
PHOTOS_DIR = "photos"
os.makedirs(PHOTOS_DIR, exist_ok=True)


class PatientProfileGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognitive Companion Configurator")

        self.data = self.load_data()

        self.build_profile_section()
        self.build_family_section()
        self.build_save_button()

    def load_data(self):
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                return json.load(f)
        return {
            "name": "",
            "preferred_name": "",
            "voice_tone": "",
            "medical_history": [],
            "daily_routine": [],
            "known_family": {}
        }

    def build_profile_section(self):
        frame = tk.LabelFrame(self.root, text="Patient Info", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar(value=self.data["name"])
        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, sticky="ew")

        tk.Label(frame, text="Preferred Name:").grid(row=1, column=0, sticky="w")
        self.pref_name_var = tk.StringVar(value=self.data["preferred_name"])
        tk.Entry(frame, textvariable=self.pref_name_var).grid(row=1, column=1, sticky="ew")

        tk.Label(frame, text="Voice Tone:").grid(row=2, column=0, sticky="w")
        self.tone_var = tk.StringVar(value=self.data["voice_tone"])
        tk.Entry(frame, textvariable=self.tone_var).grid(row=2, column=1, sticky="ew")

        tk.Label(frame, text="Medical History (comma separated):").grid(row=3, column=0, sticky="w")
        self.medical_text = tk.Text(frame, height=2)
        self.medical_text.insert("1.0", ", ".join(self.data["medical_history"]))
        self.medical_text.grid(row=3, column=1)

        tk.Label(frame, text="Daily Routine (comma separated):").grid(row=4, column=0, sticky="w")
        self.routine_text = tk.Text(frame, height=2)
        self.routine_text.insert("1.0", ", ".join(self.data["daily_routine"]))
        self.routine_text.grid(row=4, column=1)

    def build_family_section(self):
        frame = tk.LabelFrame(self.root, text="Known Family", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        self.family_frame = frame
        self.family_entries = []

        self.new_relation_var = tk.StringVar()
        self.new_name_var = tk.StringVar()

        for relation, name in self.data["known_family"].items():
            self.add_family_row(relation, name)

        new_row = len(self.family_entries)
        tk.Entry(frame, textvariable=self.new_relation_var, width=15).grid(row=new_row, column=0)
        tk.Entry(frame, textvariable=self.new_name_var, width=15).grid(row=new_row, column=1)
        tk.Button(frame, text="Add", command=self.add_family_row).grid(row=new_row, column=2)

    def add_family_row(self, relation=None, name=None):
        frame = self.family_frame
        row = len(self.family_entries)

        rel = relation or self.new_relation_var.get()
        name = name or self.new_name_var.get()
        if not rel or not name:
            return

        rel_var = tk.StringVar(value=rel)
        name_var = tk.StringVar(value=name)

        tk.Entry(frame, textvariable=rel_var, width=15).grid(row=row, column=0)
        tk.Entry(frame, textvariable=name_var, width=15).grid(row=row, column=1)
        tk.Button(frame, text="📷", command=lambda: self.capture_photo(rel, name)).grid(row=row, column=2)

        self.family_entries.append((rel_var, name_var))

        self.new_relation_var.set("")
        self.new_name_var.set("")

    def capture_photo(self, relation, name):
        def do_upload():
            file_path = filedialog.askopenfilename(
                title="Select a Photo",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
            )
            if file_path:
                filename = f"{relation.lower()}_{name.lower().replace(' ', '_')}.jpg"
                dest_path = os.path.join(PHOTOS_DIR, filename)
                shutil.copy(file_path, dest_path)
                messagebox.showinfo("Uploaded", f"Photo saved as {filename}")

        def do_camera_capture():
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                messagebox.showwarning("Camera Error", "Camera not available. Try uploading instead.")
                return do_upload()

            messagebox.showinfo("Instructions", "Press SPACE to capture, ESC to cancel.")
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame.")
                    break
                cv2.imshow("Capture", frame)
                key = cv2.waitKey(1)
                if key % 256 == 32:  # SPACE
                    filename = f"{relation.lower()}_{name.lower().replace(' ', '_')}.jpg"
                    save_path = os.path.join(PHOTOS_DIR, filename)
                    cv2.imwrite(save_path, frame)
                    print(f"✅ Saved photo to {save_path}")
                    break
                elif key % 256 == 27:  # ESC
                    print("Capture canceled.")
                    break
            cap.release()
            cv2.destroyAllWindows()

        # Show popup with choice
        option = simpledialog.askstring(
            "Photo Input",
            "Type 'upload' to upload photo or 'camera' to take a new photo:"
        )
        if not option:
            return
        option = option.lower().strip()

        if option == "upload":
            do_upload()
        elif option == "camera":
            do_camera_capture()
        else:
            messagebox.showinfo("Invalid Choice", "Please enter 'upload' or 'camera'.")

    def build_save_button(self):
        tk.Button(self.root, text="💾 Save Profile", bg="#4CAF50", fg="white", command=self.save_profile).pack(pady=10)

    def save_profile(self):
        self.data["name"] = self.name_var.get()
        self.data["preferred_name"] = self.pref_name_var.get()
        self.data["voice_tone"] = self.tone_var.get()
        self.data["medical_history"] = [x.strip() for x in self.medical_text.get("1.0", "end").strip().split(",")]
        self.data["daily_routine"] = [x.strip() for x in self.routine_text.get("1.0", "end").strip().split(",")]

        family = {}
        for rel_var, name_var in self.family_entries:
            rel, name = rel_var.get(), name_var.get()
            if rel and name:
                family[rel] = name
        self.data["known_family"] = family

        with open(PROFILE_PATH, "w") as f:
            json.dump(self.data, f, indent=2)

        messagebox.showinfo("Saved", "Patient profile updated successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientProfileGUI(root)
    root.mainloop()
