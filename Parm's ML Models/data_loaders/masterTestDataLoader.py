"""
MASTER DATA LOADER

- Scans entire dataset
- Parses filename into structured metadata
- Saves everything into metadata.csv

OUTPUT COLUMNS:
image_path, instrument, background, orientation, state,
lights, brightness, camera
"""

import os
import pandas as pd
import csv

def loadAndSaveData(root_dir, csvSave):
    # -------------------------
    # ROOT DIRECTORY
    # -------------------------
    data = []

    # -------------------------
    # PARSE FILENAME FUNCTION
    # -------------------------
    def parse_filename(file):
        name = file.replace(".jpg", "").replace(".png", "")
        parts = name.split("_")

        # -------------------------
        # 1. CAMERA (always last 2)
        # -------------------------
        camera = parts[-2] + "_" + parts[-1]

        # -------------------------
        # 2. LIGHTING (dynamic)
        # -------------------------
        lighting_parts = []
        i = len(parts) - 3  # before camera

        while i >= 0:
            p = parts[i]
            if p.startswith("S") or p.startswith("L") or p.startswith("B") or p.isdigit():
                lighting_parts.insert(0, p)
                i -= 1
            else:
                break

        # Extract lighting components
        lights = []
        brightness = None

        for p in lighting_parts:
            if p.startswith("L") or p.isdigit():
                lights.append(p)
            elif p.startswith("B"):
                brightness = int(p[1:])  # convert B100 → 100

        lights_str = "_".join(lights) if lights else None

        return lights_str, brightness, camera


    # -------------------------
    # WALK THROUGH DATASET
    # -------------------------
    for root, dirs, files in os.walk(root_dir):

        # ONLY KEEP Session_1
        if "Session_1" not in root:
            continue

        for file in files:
            if not file.lower().endswith((".jpg", ".png")):
                continue

            image_path = os.path.join(root, file)

            try:
                # -------------------------
                # EXTRACT FROM PATH (ROBUST FIX)
                # -------------------------
                path_parts = root.split(os.sep)

                # Anchor everything relative to Session_1
                session_idx = path_parts.index("Session_1")

                instrument      = path_parts[session_idx - 2]
                background      = path_parts[session_idx - 1]
                session         = path_parts[session_idx]
                camera_folder   = path_parts[session_idx + 1]
                orientation     = path_parts[session_idx + 2]
                state           = path_parts[session_idx + 3]

                # -------------------------
                # LIGHTING FROM FILENAME
                # -------------------------
                lights, brightness, camera_name = parse_filename(file)

                # -------------------------
                # NORMALIZE STRINGS (CRITICAL FOR FILTERING)
                # -------------------------
                instrument = instrument.strip()
                background = background.strip().lower()
                orientation = orientation.strip().lower()
                state = state.strip().lower()
                camera_folder = camera_folder.strip().lower()

                data.append({
                    "image_path": image_path,
                    "instrument": instrument,
                    "background": background,
                    "orientation": orientation,
                    "state": state,
                    "lights": lights,
                    "brightness": brightness,
                    "camera": camera_folder   # use folder (more reliable than filename)
                })

            except Exception as e:
                print(f"Skipping file (parse error): {file}")
                print(e)

    # -------------------------
    # CREATE DATAFRAME
    # -------------------------
    df = pd.DataFrame(data)

    # -------------------------
    # SAVE CSV
    # -------------------------
    df.to_csv(csvSave, index=False, quoting=csv.QUOTE_ALL)

"""
print("Metadata CSV created!")
print("Total images:", len(df))

# -------------------------
# DEBUG INFO
# -------------------------
print("\n--- Sample Data ---")
print(df.head())

print("\n--- Orientation Distribution ---")
print(df["orientation"].value_counts())

print("\n--- State Distribution ---")
print(df["state"].value_counts())

print("\n--- Lighting (lights) Distribution ---")
print(df["lights"].value_counts().head())

print("\n--- Brightness Distribution ---")
print(df["brightness"].value_counts().head())
"""
