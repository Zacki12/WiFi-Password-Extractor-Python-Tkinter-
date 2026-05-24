A desktop utility built with Python and Tkinter that retrieves saved WiFi profiles and extracts previously connected network passwords from a Windows system using Command Prompt (netsh) commands. The application provides a simple graphical interface and exports the collected information into a downloadable PDF report.

Features
GUI built with Tkinter
Executes Windows CMD commands automatically
Extracts saved WiFi SSIDs and passwords
Displays results inside the application
Generates and exports results to PDF
Simple and lightweight design
Windows-compatible
Technologies Used
Python
Tkinter
subprocess
netsh (Windows Command Utility)
PDF generation library (such as FPDF or ReportLab)
How It Works

The application uses Windows netsh wlan show profiles commands to:

Retrieve all WiFi profiles stored on the machine
Extract security keys/passwords for each profile
Display the information in a Tkinter GUI
Export the data into a PDF file for offline storage
Requirements
Python 3.x
Windows OS
Administrator privileges may be required for some systems
