import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from fpdf import FPDF

# ---------------------------------------------------------
# Logic to extract Wi-Fi credentials from Windows
# ---------------------------------------------------------
def get_wifi_credentials():
    credentials = []
    try:
        # Ask Windows for a list of all saved Wi-Fi profiles
        # We decode the outppip install fpdf2ut to standard text, replacing any weird characters
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
        
        # Extract just the profile names from the command output
        profiles = [i.split(":")[1][1:-1] for i in meta_data.split('\n') if "All User Profile" in i]

        # Loop through each profile name to find its password
        for profile in profiles:
            try:
                # Run the netsh command to reveal the clear-text password for this specific profile
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace")
                
                # Extract the password (Key Content)
                passwords = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
                
                # If a password exists, grab it. Otherwise, mark it as "None" (e.g., for open networks)
                password = passwords[0] if passwords else "None"
                
                # Add the pair to our list
                credentials.append((profile, password))
            except subprocess.CalledProcessError:
                # If the system denies access to a specific password, note the error
                credentials.append((profile, "Error reading password (Requires Admin?)"))
                
    except Exception as e:
        messagebox.showerror("System Error", f"Could not retrieve Wi-Fi profiles. Error: {e}")
        
    return credentials

# ---------------------------------------------------------
# Logic to generate and save the PDF
# ---------------------------------------------------------
def save_to_pdf(credentials, filepath):
    # Initialize the PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the title font and text
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Saved Wi-Fi Networks and Passwords", ln=True, align='C')
    
    # Draw a line under the title
    pdf.line(10, 20, 200, 20)
    pdf.ln(10) # Add some vertical spacing
    
    # Set the font for the data
    pdf.set_font("Arial", size=12)
    
    # Write each Wi-Fi name and password to the PDF
    for ssid, password in credentials:
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 8, txt=f"Network (SSID): {ssid}", ln=True)
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"Password: {password}", ln=True)
        
        pdf.ln(4) # Add space between entries
        
    # Save the file to the chosen path
    pdf.output(filepath)

# ---------------------------------------------------------
# GUI Event Handler
# ---------------------------------------------------------
def on_extract_button_click():
    # 1. Get the data
    credentials = get_wifi_credentials()
    
    if not credentials:
        messagebox.showinfo("Info", "No Wi-Fi profiles were found on this system.")
        return
        
    # 2. Ask the user where they want to save the PDF
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf", 
        filetypes=[("PDF files", "*.pdf")],
        title="Save Wi-Fi Passwords As..."
    )
    
    # 3. If the user didn't cancel the save dialog, create the PDF
    if filepath:
        try:
            save_to_pdf(credentials, filepath)
            messagebox.showinfo("Success!", f"Successfully exported {len(credentials)} networks to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")

# ---------------------------------------------------------
# Build the Graphical User Interface (GUI)
# ---------------------------------------------------------
# Create the main window
root = tk.Tk()
root.title("Wi-Fi Password Extractor")
root.geometry("400x200")
root.resizable(False, False)

# Add some padding and a description label
label = tk.Label(root, text="Extract all saved Wi-Fi networks and\npasswords to a PDF file.\n @zacki12", font=("Arial", 12))
label.pack(pady=30)

# Add the main extraction button
extract_btn = tk.Button(root, text="Extract & Save to PDF", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=on_extract_button_click)
extract_btn.pack(pady=10)

# Start the GUI loop
root.mainloop()