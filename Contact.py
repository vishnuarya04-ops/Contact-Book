"""
Name: VISHNU SHANKAR
Course: MCA (AI & ML)
Subject: Programming for Problem Solving Using Python
Assignment 02 – Contact Book (CSV + JSON + Exception Handling)
"""

import csv
import json
from datetime import datetime

CSV_FILE = "contacts.csv"
JSON_FILE = "contacts.json"
LOG_FILE = "error_log.txt"

def log_error(msg, op):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] ERROR in {op}: {msg}\n")

def load_contacts():
    try:
        with open(CSV_FILE, "r") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []
    except Exception as e:
        log_error(e, "Load CSV")
        return []

def save_contacts(contacts):
    try:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(contacts)
    except Exception as e:
        log_error(e, "Save CSV")

def add_contact():
    print("\n--- Add Contact ---")
    c = {
        "name": input("Name: ").strip(),
        "phone": input("Phone: ").strip(),
        "email": input("Email: ").strip(),
    }
    if not c["name"]:
        print("Name cannot be empty.")
        return
    contacts = load_contacts()
    contacts.append(c)
    save_contacts(contacts)
    print("✔ Contact added!\n")

def view_contacts():
    print("\n--- Contacts ---")
    contacts = load_contacts()
    if not contacts:
        print("No contacts found.")
        return
    print(f"{'Name':15}{'Phone':15}{'Email'}")
    print("-" * 40)
    for c in contacts:
        print(f"{c['name']:15}{c['phone']:15}{c['email']}")

def search_contact():
    name = input("\nSearch Name: ").lower()
    for c in load_contacts():
        if name in c["name"].lower():
            print(f"Found → {c['name']} | {c['phone']} | {c['email']}")
            return c
    print("No contact found.")
    return None

def update_contact():
    target = search_contact()
    if not target:
        return
    print("--- Update Contact ---")
    target["phone"] = input("New Phone (leave blank to keep): ") or target["phone"]
    target["email"] = input("New Email (leave blank to keep): ") or target["email"]
    contacts = load_contacts()
    for c in contacts:
        if c["name"] == target["name"]:
            c.update(target)
    save_contacts(contacts)
    print("✔ Updated!\n")

def delete_contact():
    target = search_contact()
    if not target:
        return
    contacts = load_contacts()
    contacts = [c for c in contacts if c["name"] != target["name"]]
    save_contacts(contacts)
    print("✔ Deleted!\n")

def export_json():
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(load_contacts(), f, indent=4)
        print("✔ Exported to JSON!\n")
    except Exception as e:
        log_error(e, "Export JSON")

def import_json():
    try:
        with open(JSON_FILE) as f:
            data = json.load(f)
        print("\n--- JSON Contacts ---")
        for c in data:
            print(f"{c['name']} | {c['phone']} | {c['email']}")
    except Exception as e:
        log_error(e, "Import JSON")
        print("JSON file missing or corrupted.")

# ----------------------  Welcome + Menu ---------------------- #
def main():
    print("""
===============================
      CONTACT BOOK - PYTHON PROJECT
 This tool allows you to Add, View, Search,
 Update, Delete contacts with CSV & JSON.
===============================
""")
    while True:
        print("""
1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Export JSON
7. Import JSON
0. Exit
""")
        choice = input("Choose: ")
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "0":
            print("Thank you!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
