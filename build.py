import PyInstaller.__main__
import os
import shutil
import customtkinter

# Get CustomTkinter path for data inclusion
ctk_path = os.path.dirname(customtkinter.__file__)

# Define PyInstaller arguments
args = [
    'main.py',                               # Entry point
    '--name=QRMint',                         # Name of the executable
    '--noconfirm',                           # Overwrite output directory without asking
    '--onefile',                             # Package into a single executable
    '--windowed',                            # No console window
    '--clean',                               # Clean cache
    f'--add-data={ctk_path};customtkinter/', # Include CTK assets
    '--add-data=media;media/',               # Include local media folder (if exists, or empty)
    # Hidden imports often missed by PyInstaller analysis
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=reportlab',
    '--hidden-import=reportlab.pdfgen',
    '--hidden-import=reportlab.lib.pagesizes',
]

# Ensure media directory exists locally (or create valid empty one for build)
if not os.path.exists("media"):
    os.makedirs("media")

print("Building QRMint.exe... This make take a minute.")
PyInstaller.__main__.run(args)
print("Build Complete! Check the 'dist' folder.")
