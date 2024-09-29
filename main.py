import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
from datetime import datetime, timedelta

# Define the XML template without any keys
xml_template = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PrintLetterBarcodeData {attributes}/>
"""

# Function to generate the QR code
def generate_qr_code(data):
    # Remove empty fields and format the attributes for the XML template
    attributes = ' '.join(f'{key}="{value}"' for key, value in data.items() if value)
    
    # Substitute the attributes into the XML template
    xml_data = xml_template.format(attributes=attributes)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(xml_data)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image with the user's name
    filename = f"QRs/{data['name']}_qrcode.png"
    img.save(filename)
    messagebox.showinfo("Success", f"QR code for {data['name']} has been generated and saved as {filename}")
    
    # Display the QR code in the UI
    img = Image.open(filename)
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    qr_code_label.config(image=img)
    qr_code_label.image = img

# Function to collect data and call the QR code generator
def on_generate():
    data = {
        'uid': uid_entry.get(),
        'name': name_entry.get(),
        'careOf': careOf_entry.get(),
        'building': building_entry.get(),
        'street': street_entry.get(),
        'landmark': landmark_entry.get(),
        'vtcName': vtcName_entry.get(),
        'districtName': districtName_entry.get(),
        'stateName': stateName_entry.get(),
        'pincode': pincode_entry.get(),
    }
    
    dob_str = dob_entry.get()
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, "%d/%m/%Y")
            current_year = datetime.now().year
            if (current_year - dob.year) < 21:
                dob = dob.replace(year=current_year - 22)
                print(f'new dob is :{dob}')
            data['dob'] = dob.strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid DOB format. Please use DD/MM/YYYY.")
            return

    # Check for required fields
    required_fields = ['uid', 'name', 'districtName', 'stateName']
    missing_fields = [field for field in required_fields if not data[field]]
    
    if missing_fields:
        messagebox.showerror("Error", f"The following fields are required: {', '.join(missing_fields)}")
        return
    
    generate_qr_code(data)

# Create the main window
root = tk.Tk()
root.title("QR Code Generator")

# Create and place the input fields and labels in a grid
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

labels = ["UID", "Name", "DOB (DD/MM/YYYY)", "Care Of", "Building", "Street", "Landmark", "VTC Name", "District Name", "State Name", "Pincode"]
entries = []

for i, label in enumerate(labels):
    lbl = ttk.Label(main_frame, text=label)
    lbl.grid(column=0, row=i, sticky=tk.W, pady=5)
    entry = ttk.Entry(main_frame, width=40)
    entry.grid(column=1, row=i, sticky=(tk.W, tk.E), pady=5)
    entries.append(entry)

(uid_entry, name_entry, dob_entry, careOf_entry, building_entry, street_entry, landmark_entry, vtcName_entry, districtName_entry, stateName_entry, pincode_entry) = entries

# Create the Generate QR Code button
generate_button = ttk.Button(main_frame, text="Generate QR Code", command=on_generate)
generate_button.grid(column=1, row=len(labels), pady=10)

# Label to display the QR code
qr_code_label = ttk.Label(main_frame)
qr_code_label.grid(column=1, row=len(labels) + 1, pady=10)

# Configure column weights
for i in range(2):
    main_frame.columnconfigure(i, weight=1)

# Start the main loop
root.mainloop()
