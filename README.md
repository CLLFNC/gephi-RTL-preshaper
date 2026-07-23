# gephi-RTL-preshaper

 A GUI application to prepare Arabic, Persian (or other RTL script) labels before importing them into Gephi, which does not natively support right-to-left rendering.

 Given a CSV with a text column (e.g. nodes or edges), the tool creates a new column called **Label** containing the reshaped and reordered text, **which will be unreadable bu the human eye, but ready to be used as a label in Gephi** during import.
 
 The interface is available in English, Italian, Arabic, Farsi, selectable from a menu at the top of the app window.

 **To be visualized correctly in Gephi, you need to have the necessary fonts for your target language installed on your system.**

 [![Download Windows](https://img.shields.io/badge/Download-Windows-blue?logo=windows)](https://github.com/CLLFNC/gephi-RTL-preshaper/releases/download/v1.0.0/GephiRTLReshaper-windows.zip)
[![Download macOS](https://img.shields.io/badge/Download-macOS-lightgrey?logo=apple)](https://github.com/CLLFNC/gephi-RTL-preshaper/releases/download/v1.0.0/GephiRTLReshaper-macos.zip)
[![Download Linux](https://img.shields.io/badge/Download-Linux-orange?logo=linux)](https://github.com/CLLFNC/gephi-RTL-preshaper/releases/download/v1.0.0/GephiRTLReshaper-linux.zip)

## How to use it:

- Browse... → select the CSV with nodes or edges
- Select the column to convert (e.g. "Name")
- Process and save
- A filename_gephi.csv file is generated in the same folder as the original file, **with all the original columns plus the new Label column**
- In Gephi, import that CSV and use Label as the label field for nodes or edges

## Installation
The executables are not digitally signed, so operating systems will show a security warning the first time. It just needs to be authorized once.

### Windows
- Extract the GephiRTLReshaper-windows zip (right-click → "Extract All")
- Double-click GephiRTLReshaper.exe
- Windows Defender SmartScreen will show: "Windows protected your PC"
- Click "More info" (small gray link) → then click "Run anyway"
- From then on, the app opens normally with no further warnings

### macOS
- Extract the GephiRTLReshaper-macos zip
- Do not double-click it the first time — instead: right-click (or Ctrl+click) the app → Open
- macOS will show a warning ("unidentified developer") but this time with an "Open" button available
- If the button doesn't appear, go to System Settings → Privacy & Security, scroll to the bottom of the page, and click "Open Anyway" next to the message about GephiRTLReshaper
- After this first manual authorization, the app will always open normally with a double-click

### Linux
Linux does not show a Gatekeeper/SmartScreen-style warning, but the file needs to be marked as "executable" first — most file managers extract zip files without that permission set, and double-clicking may just open a text editor instead of running the program.

#### Using the file manager (e.g. GNOME Files/Nautilus on Ubuntu):

- Extract the GephiRTLReshaper-linux zip
- Right-click the GephiRTLReshaper file → Properties
- Go to the Permissions tab → check "Allow executing file as program" (wording may vary slightly by distro/file manager) → close the dialog
- Double-click the file
- If a dialog pops up asking whether to Run or Display the file, choose Run
- From then on, double-clicking opens the app directly

#### Using the terminal:

- Extract the zip
- Open a terminal in that folder and run:
bash
   chmod +x GephiRTLReshaper
   ./GephiRTLReshaper
  
- The app window opens; this only needs to be done once — after that, ./GephiRTLReshaper (or double-click, per the steps above) works directly
