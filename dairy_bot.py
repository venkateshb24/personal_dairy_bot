import json
import os
from datetime import datetime
import shutil

DATA_FILE = "entries.json"
MEDIA_FOLDER = "media"

if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)

def copy_file_to_media(path):
    if not os.path.exists(path):
        return "File not found"
    filename = os.path.basename(path)
    dest = os.path.join(MEDIA_FOLDER, filename)
    shutil.copy(path, dest)
    return dest

def log_entry():
    entry = {}

    date_input = input("Enter the date (YYYY-MM-DD) or press Enter for today: ")
    entry["date"] = date_input.strip() if date_input.strip() else datetime.now().strftime("%Y-%m-%d")

    entry["how_was_day"] = input("How was your day? ")
    
    people = input("Who did you meet today? (separate names with commas): ")
    entry["people_met"] = [p.strip() for p in people.split(",") if p.strip()]

    activities = input("What did you do today? (separate with commas): ")
    entry["activities"] = [a.strip() for a in activities.split(",") if a.strip()]

    cert_path = input("Enter path of certificate image (Leave empty if none): ").strip()
    cert_copy_path = copy_file_to_media(cert_path) if cert_path else None

    photo_path = input("Enter path of photo/selfie (Leave empty if none): ").strip()
    photo_copy_path = copy_file_to_media(photo_path) if photo_path else None

    entry["memories"] = {
        "certificates": cert_copy_path,
        "photos": photo_copy_path
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(entry)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print(f"\nEntry for {entry['date']} saved successfully!\n")

def search_entries(search_term):
    if not os.path.exists(DATA_FILE):
        print("No entries found.")
        return

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    found = False
    for entry in data:
        if (
            search_term.lower() in entry["date"].lower()
            or search_term.lower() in entry["how_was_day"].lower()
            or any(search_term.lower() in person.lower() for person in entry["people_met"])
            or any(search_term.lower() in activity.lower() for activity in entry["activities"])
        ):
            print("\n--- Entry Found ---")
            print(json.dumps(entry, indent=4))
            found = True

    if not found:
        print("No matching entry found.")

def main_menu():
    while True:
        print("\n==== Personal Diary Bot ====")
        print("1. Log Today’s Entry")
        print("2. Search Past Entries")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            log_entry()
        elif choice == "2":
            keyword = input("Enter a keyword or date to search: ")
            search_entries(keyword)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()