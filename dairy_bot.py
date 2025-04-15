import os
import shutil
import json
from datetime import datetime

def welcome():
    print("Hi! I'm your Personal Dairy Bot.")
    print("Let's log your day!")

def copy_file_to_media(file_path):
    if file_path.strip() == "":
        return "None"

    if not os.path.exists("media"):
        os.makedirs("media")

    filename = os.path.basename(file_path)
    dest_path = os.path.join("media", filename)

    try:
        shutil.copy(file_path, dest_path)
        print(f"Copied to: {dest_path}")
        return dest_path
    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
        return "Invalid file"

def get_entry():
    entry={}

    date_input=input("Enter the date(YYYY-MM-DD) or press Enter for today: ")
    if date_input.strip()=="":
        entry["date"]=datetime.now().strftime("%Y-%m-%d")
    else:
        entry["date"]=date_input 

    entry["how_was_day"]=input("How was your day? ")
    entry["people_met"]=input("Who did you meet today?(seperated names with commas)")

    cert_path=input("Enter path of certificate image (Leave empty if none)") or "None"
    if cert_path.strip():
        cert_copy_path=copy_file_to_media(cert_path)
    else:
        cert_path="None"

    photo_path=input("Enter path of photo/selfie (Leave empty if none):") or "None"
    if photo_path.strip():
        photo_copy_path=copy_file_to_media(photo_path)
    else:
        photo_copy_path="None"
    
    entry["memories"]={
        "certificates":cert_copy_path,
        "photos":photo_copy_path
    } 