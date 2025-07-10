import face_recognition
import cv2
import os
import json
import numpy as np

with open("patient_profile.json") as f:
    data = json.load(f)

photo_folder = "photos_clean"
encoding_folder = "encodings"
os.makedirs(encoding_folder, exist_ok=True)

for relation, name in data["known_family"].items():
    filename = f"{relation.lower()}_{name.lower()}.jpg"
    filepath = os.path.join(photo_folder, filename)

    if not os.path.exists(filepath):
        print(f"❌ Photo missing: {filepath}")
        continue

    image_bgr = cv2.imread(filepath)
    if image_bgr is None:
        print(f"❌ Could not load image: {filename}")
        continue

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    try:
        encodings = face_recognition.face_encodings(image_rgb)
        if encodings:
            out_path = os.path.join(encoding_folder, f"{relation.lower()}_{name.lower()}.npy")
            np.save(out_path, encodings[0])
            print(f"✅ Encoded {relation} ({name})")
        else:
            print(f"⚠️ No face found in {filename}")
    except Exception as e:
        print(f"❌ Failed encoding {filename}: {e}")
