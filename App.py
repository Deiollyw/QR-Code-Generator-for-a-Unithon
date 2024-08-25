import segno
import os
import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
import random


qr_code_window = None
qr_id = None

global CurrentSpots

#Current amount of spots left
CurrentSpots = 5

#Directories
Data_PATH = r"DATA.text"
QR_ID_PATH = r"QR_ID.png"

# Open the file and write the CurrentSpost value
with open(Data_PATH, "w") as file:
    # Write text to the file
    file.write(str(CurrentSpots))

qr_usage_count = {}

# Generate a unique ID for QR code
def generate_unique_id():
    return random.randint(1000, 9999)

# Generate a QR code with a unique ID
def generate_qr_code():
    global qr_id
    # Generate unique ID
    qr_id = generate_unique_id()

    # Generate QR code
    qr = segno.make_qr(str(qr_id))

    # Save QR code image
    qr.save(QR_ID_PATH, scale=10)

    # Display success message
    status_label.config(text=f"QR code {qr_id} generated successfully.", fg="green", font=("Arial", 20, "bold"))

    # Open a window to show the QR code image
    display_qr_code()

# Display QR code in a window
def display_qr_code():
    global qr_code_window
    if qr_code_window:
        qr_code_window.destroy()

    qr_code_window = tk.Toplevel(root)
    qr_code_window.title("QR Code")
    qr_code_window.geometry("300x300")

    qr_image = Image.open(QR_ID_PATH)
    qr_photo = ImageTk.PhotoImage(qr_image)

    qr_label = tk.Label(qr_code_window, image=qr_photo)
    qr_label.image = qr_photo
    qr_label.pack()

# Function to use a QR code
def use_qr_code():
    global qr_code_window
    global qr_id
    global qr_usage_count

    if qr_id:
        # Increment usage count
        qr_usage_count[qr_id] = qr_usage_count.get(qr_id, 0) + 1
        with open(Data_PATH, "w") as file:
            file.write(str(CurrentSpots - 1))

        # Check if QR code has been used twice
        if qr_usage_count[qr_id] == 2:
            # Delete the QR code
            os.remove(QR_ID_PATH)
            status_label.config(text=f"QR code {qr_id} used twice.", fg="green", font=("Arial", 20, "bold"))
            with open(Data_PATH, "w") as file:
                CurrentSpots + 1
                file.write(str(CurrentSpots))
            qr_id = None
            if qr_code_window:
                qr_code_window.destroy()
        elif qr_usage_count[qr_id] > 2:
            status_label.config(text=f"You no longer have a QR code. Create a new QR code first by hitting the 'Generate Code' button.", fg="green", font=("Arial", 15, "bold"))
            qr_id = None
            if qr_code_window:
                qr_code_window.destroy()
        else:
            status_label.config(text=f"QR code {qr_id} used once.", fg="green", font=("Arial", 20, "bold"))

root = tk.Tk()
root.title("Parking Counter")
root.geometry("600x800")

# ico = PhotoImage(file=r"QR background.png")
# root.iconphoto(False, ico)

center_frame = tk.Frame(root)
center_frame.pack(expand=True, fill="none", padx=10, pady=10)

# Igenerate = PhotoImage(file=r"Generate buttom.png")
# Iscan = PhotoImage(file=r"Scan code.png")

generate_button = ttk.Button(center_frame, text="Generate QR Code", command=generate_qr_code, padding=0)
generate_button.pack(pady=20)

use_button = ttk.Button(center_frame, text="Scan QR Code (test)", command=use_qr_code, padding=1)
use_button.pack(pady=2)

status_label = tk.Label(center_frame, text="", fg="black")
status_label.pack(pady=10)

root.mainloop()