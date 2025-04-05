import Brickoganize, os, sys
import cv2
import numpy as np
import threading
import time
import tkinter as tk
import serial
type=["Brick", "Technic", "Plate", "Tile", "Slope", "Minifig", "Misc"]
color=['white', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
size=["1x1", "1x2", "1x3", "1x4", "1x6", "1x8", "2x2", "2x3", "2x4", "2x6", "2x8", "3x3", "3x4", "4x4", "4x6", "4x8", "6x6", "6x8", "8x8"]
def check_weight():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            print(line)

            if line and "ALERT: Bin is Full" in line: 
                print("Bin is full! Stopping sorting.")
                UI.stop_sorting()
                UI.bin_full()
def read_bin():
    bins={1:{'Color':None,'Type':'Brick','Size':None}}
    return bins
def read_response():
    global response
    with open('Image/response.txt', 'r') as f:
        res = f.read().strip()
        if res == "LEGO not detected":
            response.append(None)
        else:
            name, category, type_ = res.split(", ")
            response.append({
                "Name": name.split(": ")[1],
                "Category": category.split(": ")[1],
                "Type": type_.split(": ")[1]
            })
            with open('Image/color.txt', 'r') as f:
                color = f.read().strip()
                response[-1]['Color']=color
        f.close() 
    response=response[1:]
    print(response[-1])
def determine_bin():
    global response
    read_response()
    bins=read_bin()
    names = [item['Name'] for item in response if item is not None]
    name_counts = {name: names.count(name) for name in set(names)}
    id=''
    flag=False
    for name,count in name_counts.items():
        if count >= 4:
            id=name
            flag=True
            break
    if not flag:
        return
    ids={}
    for item in response:
        if item and item['Name'] == id:
            ids = item
            break
    if 'Name' in ids:
        name = ids['Name']
        category = ids['Category']
        typ = ids['Type']
        color = ids['Color']
    else:
        print("Error: 'Name' key not found in ids")
        return

    best_match = 0
    max_similarity = 0

    for bin_id, attributes in bins.items():
        similarity = 0
        if attributes['Size']!= None:
            if attributes['Size'] in name:
                similarity += 1
        if category==attributes['Type']:
            similarity += 1
        if attributes['Color'] == color:
            similarity += 1

        if similarity > max_similarity:
            max_similarity = similarity
            best_match = bin_id
    print(max_similarity)
    time.sleep(1)
    response=[None]*6
    
def tell_angle(bin):
    top=False
    if bin<19:
        top=True

    return
if __name__ == '__main__':
    with open("Status.txt", "w") as file:
        file.write("Status: Stop\n")
    file.close()
    #with open("Image/response.txt", "w") as file:
    #    file.write("LEGO not detected")
    #file.close()
    import UI
    response=[None]*6
    # Initialize the serial connection
    #port = '/dev/cu.usbmodem11301'
    #ser = serial.Serial(port, 9600, timeout=1)
    #threading.Thread(target=check_weight, daemon=True).start()
    while True:
        determine_bin()
        time.sleep(0.25)
