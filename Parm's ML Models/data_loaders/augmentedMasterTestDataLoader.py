"""
MASTER DATA LOADER (AUGMENTED DATASET VERSION)

- Scans dataset directory
- Parses filenames using the NEW format:
    Name_state_[imageID]_aug[backgroundID].jpg

- Extracts structured metadata
- Saves everything into metadata.csv

-----------------------------------------------------
EXPECTED FILENAME FORMAT:

Example:
Needle_Holder_Mayo-Hegar_..._closed_01_aug003.jpg

Breakdown:
    - Instrument: everything before state
    - State: "open" or "closed"
    - image_id: original image index (e.g. 01)
    - aug index: background augmentation ID (aug003 → 3)

-----------------------------------------------------

OUTPUT COLUMNS:
    image_path
    instrument
    state
    image_id
    background_aug
"""

import os
import pandas as pd
import csv

def loadAndSaveData_a(root_dir, csvSave):
    """
    Walks through dataset, parses filenames, and saves structured metadata.

    Args:
        root_dir (str): Root directory of dataset
        csvSave (str): Output CSV file path
    """

    data = []

    # -------------------------------------------------
    # PARSE FILENAME FUNCTION: Name_orientation_state_
    # [2 digit image id out of 50 which augment was
    # derived from]_aug[out of 20 random bg, which is it]
    # -------------------------------------------------
    def parse_filename(file):
        name = file.replace(".jpg", "").replace(".png", "")
        parts = name.split("_")

        # -------------------------
        # SPECIAL CASE:
        # FILENAMES CONTAIN ORIENTATION
        # -------------------------
        has_orientation = (
            "_".join(parts).find("right_side_up") != -1 or
            "_".join(parts).find("left_side_up") != -1 or
            "_".join(parts).find("upside_down") != -1
        )

        if has_orientation:

            # -------------------------
            # DETERMINE ORIENTATION
            # -------------------------
            if "right_side_up" in "_".join(parts):
                orientation = "right side up"
                orientation_len = 3

            elif "left_side_up" in "_".join(parts):
                orientation = "left side up"
                orientation_len = 3

            elif "upside_down" in "_".join(parts):
                orientation = "upside down"
                orientation_len = 2

            # -------------------------
            # AUGMENTED CASE
            # -------------------------
            if parts[-1].startswith("aug"):
                background_aug = int(parts[-1].replace("aug", ""))
                image_id = int(parts[-2])
                state = parts[-3]

                instrument_parts = parts[:-(3 + orientation_len)]

            # -------------------------
            # ORIGINAL IMAGE (NO AUG)
            # -------------------------
            else:
                background_aug = None
                image_id = int(parts[-1])
                state = parts[-2]

                instrument_parts = parts[:-(2 + orientation_len)]

        else:

            # -------------------------
            # DEFAULT CASE
            # (EXISTING PARSER)
            # -------------------------
            orientation = None

            # -------------------------
            # 1. CHECK IF AUGMENTED
            # -------------------------
            if parts[-1].startswith("aug"):
                # -------------------------
                # AUGMENTED CASE
                # -------------------------
                background_aug = int(parts[-1].replace("aug", ""))
                image_id = int(parts[-2])
                state = parts[-3]

                instrument_parts = parts[:-3]

            else:
                # -------------------------
                # ORIGINAL IMAGE (NO AUG)
                # -------------------------
                background_aug = None
                image_id = int(parts[-1])
                state = parts[-2]

                instrument_parts = parts[:-2]

        # -------------------------
        # VALIDATION
        # -------------------------
        if state not in ["open", "closed"]:
            raise ValueError("Invalid state value")

        if len(instrument_parts) == 0:
            raise ValueError("Instrument name missing")

        # -------------------------
        # INSTRUMENT NAME
        # -------------------------
        instrument = " ".join(instrument_parts)

        # -------------------------
        # RETURN STRUCTURED DATA
        # -------------------------
        return {
            "instrument": instrument,
            "orientation": orientation,
            "state": state,
            "image_id": image_id,
            "background_aug": background_aug
        }

    # -------------------------------------------------
    # WALK THROUGH DATASET
    # -------------------------------------------------
    for root, dirs, files in os.walk(root_dir):
        for file in files:

            # Only process images
            if not file.lower().endswith((".jpg", ".png")):
                continue

            image_path = os.path.join(root, file)

            try:
                parsed = parse_filename(file)

                data.append({
                    "image_path": image_path,
                    "instrument": parsed["instrument"],
                    "orientation": parsed["orientation"],
                    "state": parsed["state"],
                    "image_id": parsed["image_id"],
                    "background_aug": parsed["background_aug"]
                })

            except Exception as e:
                print(f"Skipping file (parse error): {file}")
                print(e)

    # -------------------------------------------------
    # CREATE DATAFRAME
    # -------------------------------------------------
    df = pd.DataFrame(data)

    # -------------------------------------------------
    # SAVE CSV
    # -------------------------------------------------
    df.to_csv(csvSave, index=False, quoting=csv.QUOTE_ALL)