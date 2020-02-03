import config
import csv
import tkinter as tk
from tkinter import filedialog

def ReadData():
    root = tk.Tk()
    staticport_list = []
    reader = dict()
    while True:
        print("Please select file (.csv) ....")
        filedata = filedialog.askopenfilename()
        root.update()
        root.withdraw()
        print("File: " + filedata + "\n================================")
        if filedata != "":
            reader = csv.DictReader(open(filedata))
            break
        else:
            print(Back.RED + "You are not choose any file.")
            print(Style.RESET_ALL)

    for line in reader:
        staticport_list.append(line)

    root.destroy()
    return (staticport_list)

def ReadEPG():
    epg_detail = []
    fileEPG = config.epg_detail
    reader = csv.DictReader(open(fileEPG))
    for line in reader:
        epg_detail.append(line)
    
    return (epg_detail)