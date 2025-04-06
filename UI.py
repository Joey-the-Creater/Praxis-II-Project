from tkinter import *
import tkinter.messagebox as messagebox
import time
import serial
import compare
import threading

root = Tk()
root.geometry("1080x550")
root.title("LESORT Interface")
# Adding a label for the title
title_label = Label(root, text="LESORT Interface", font=("Arial", 20, "bold"))
title_label.pack(pady=10)
# Adding Start and Stop buttons
button_frame = Frame(root)
button_frame.pack(pady=20)

if not hasattr(root, '_status_initialized'):
    with open("Status.txt", "w") as file:
        file.write("Status: Stop\n")
    file.close()
    with open("Image/response.txt", "w") as file:
        file.write("LEGO not detected")
    file.close()
    compare.main(root)
    
    root._status_initialized = True
def check_weight():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            print(line)

            if line and "ALERT: Bin is Full" in line: 
                print("Bin is full! Stopping sorting.")
                stop_sorting()
                bin_full()
def read_bin():
    bins={1:{'Color':None,'Type':'Brick','Size':None}}
    return bins
def read_response(response):
    time.sleep(0.25)
    with open('Image/response.txt', 'r') as f:
        res = f.read().strip()
        if res == "LEGO not detected":
            response.append({1:1})
        else:
            parts = res.split(". ")
            response_data = {}
            for part in parts:
                if ": " in part:
                    key, value = part.split(": ", 1)
                    response_data[key.strip()] = value.strip()
            response.append({
                "Name": response_data.get("Name", ""),
                "Category": response_data.get("Category", ""),
                "Type": response_data.get("Type", "")
            })
            with open('Image/color.txt', 'r') as f:
                color = f.read().strip()
                response[-1]['Color']=color
        f.close() 
    response=response[1:]
    return response
def determine_bin():
    response=[{1:1}]*6
    while True:
        time.sleep(0.25)
        response=read_response(response)
        if response == [{1:1}]*6:
            time.sleep(0.25)
            continue
        bins=read_bin()
        names=[]
        for i in response:
            if i == {1:1}:
                continue
            names.append(i['Name'])
        if len(names) == 0:
            time.sleep(0.25)
            continue
        name_counts = {name: names.count(name) for name in set(names)}
        id=''
        flag=False
        for name,count in name_counts.items():
            if count >= 4:
                id=name
                flag=True
                break
        if not flag:
            continue
        print("Piece Located",id)
        print(response)
        ids={}
        for item in response:
            if item == {1:1}:
                continue
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
            continue

        best_match = 0
        max_similarity = 0

        for bin_id, attributes in bins.items():
            similarity = 0
            if attributes['Size']!= None:
                if attributes['Size'] in name:
                    similarity += 1
            if category==attributes['Type'] or (name in attributes['Type']):
                similarity += 1
            if attributes['Color'] == color:
                similarity += 1

            if similarity > max_similarity:
                max_similarity = similarity
                best_match = bin_id
        print(max_similarity)
        tell_angle(max_similarity)
        time.sleep(1)
        response=[{1:1}]*6
    
def tell_angle(bin):
    top=False
    if bin<19:
        top=True
        if bin == 0:
            angle = 90
        else:
            angle = -90
        print(f"Sending angle {angle} to Arduino")
        ser.write(f"{angle}\n".encode())
    return
# Initialize the serial connection
port = "/dev/cu.usbmodem11301"
ser = serial.Serial(port, 9600, timeout=1)
threading.Thread(target=check_weight, daemon=True).start()
threading.Thread(target=determine_bin, daemon=True).start()

def start_sorting():
    status_label.config(text="Status: Running", fg="green")
    with open("Status.txt", "w") as file:
        file.write("Status: Start\n")
    file.close()

def stop_sorting():
    status_label.config(text="Status: Stop", fg="red")
    with open("Status.txt", "w") as file:
        file.write("Status: Stop\n")
    file.close()

def bin_full():
    status_label.config(text="Status: Bin Full", fg="orange")

start_button = Button(button_frame, text="Start Sorting", font=("Arial", 12), command=start_sorting, bg="green", fg="white")
start_button.pack(side=LEFT, padx=10)

stop_button = Button(button_frame, text="Stop Sorting", font=("Arial", 12), command=stop_sorting, bg="red", fg="white")
stop_button.pack(side=LEFT, padx=10)

status_label = Label(button_frame, text="Status: Stop", font=("Arial", 12), fg="red")
status_label.pack(side=LEFT, padx=10)

# Adding three dropdown menus from left to right
options1 = [i for i in range(1, 19)]  
optionsd1 = [i for i in range(19, 30)]  
options2 = ["Brick", "Technic", "Plate", "Tile", "Slope", "Minifig", "Misc"]
options3 = ['white', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
options4=["1x1", "1x2", "1x3", "1x4", "1x6", "1x8", "2x2", "2x3", "2x4", "2x6", "2x8", "3x3", "3x4", "4x4", "4x6", "4x8", "6x6", "6x8", "8x8"]
# Dictionary to record sorting options for each bin
sorting_options = {}
for i in range(1, 30):
    sorting_options[i] = {
        "Type": "None",
        "Color": "None",
        "Size": "None"
    }


# Function to update the dictionary with sorting options
def update_sorting_options(bin_number, bin_type, bin_color, bin_size,level=None):
    sorting_options[int(bin_number)] = {
        "Type": bin_type,
        "Color": bin_color,
        "Size": bin_size
    }
    # Save the sorting options to a text file
    with open("sorting_options.txt", "w") as file:
        for bin_number, options in sorting_options.items():
            file.write(f"Bin {bin_number}: Type={options['Type']}, Color={options['Color']},Size={options['Size']}\n")
    file.close()


# Top Level Bin
top_label = Label(root, text="Top Level Bin:", font=("Arial", 15, "bold"))
top_label.pack(pady=10)

selected_option1 = StringVar(root)
selected_option1.set(options1[0])  # Default value

selected_option2 = StringVar(root)
selected_option2.set(options2[0])  # Default value

selected_option3 = StringVar(root)
selected_option3.set(options3[0])  # Default value

selected_option4 = StringVar(root)
selected_option4.set(options4[0])  # Default value

frame_top = Frame(root)
frame_top.pack(pady=10)

dropdown1_label = Label(frame_top, text="Bin:", font=("Arial", 12))
dropdown1_label.pack(side=LEFT, pady=10)
dropdown1 = OptionMenu(frame_top, selected_option1, *options1)
dropdown1.pack(side=LEFT, padx=10)

dropdown2_label = Label(frame_top, text="Type:", font=("Arial", 12))
dropdown2_label.pack(side=LEFT, pady=10)
dropdown2 = OptionMenu(frame_top, selected_option2, *options2)
dropdown2.pack(side=LEFT, padx=10)

dropdown3_label = Label(frame_top, text="Color:", font=("Arial", 12))
dropdown3_label.pack(side=LEFT, pady=10)
dropdown3 = OptionMenu(frame_top, selected_option3, *options3)
dropdown3.pack(side=LEFT, padx=10)

dropdown4_label = Label(frame_top, text="Size:", font=("Arial", 12))
dropdown4_label.pack(side=LEFT, pady=10)
dropdown4 = OptionMenu(frame_top, selected_option4, *options4)
dropdown4.pack(side=LEFT, padx=10)

# Set Button to allocate sorting type for Top Level Bin
def set_sorting_top():
    bin_number = selected_option1.get()
    bin_type = selected_option2.get()
    bin_color = selected_option3.get()
    messagebox.showinfo("Set Sorting", f"Top Level Bin {bin_number} set to Type: {bin_type}, Color: {bin_color}")
    update_sorting_options(bin_number, bin_type, bin_color, "Top")

set_button_top = Button(frame_top, text="Set", font=("Arial", 12), command=set_sorting_top, bg="blue", fg="white")
set_button_top.pack(side=LEFT, padx=10)

# Low Level Bin
low_label = Label(root, text="Low Level Bin:", font=("Arial", 15, "bold"))
low_label.pack(pady=10)

selected_option1_low = StringVar(root)
selected_option1_low.set(optionsd1[0])  # Default value

selected_option2_low = StringVar(root)
selected_option2_low.set(options2[0])  # Default value

selected_option3_low = StringVar(root)
selected_option3_low.set(options3[0])  # Default value

frame_low = Frame(root)
frame_low.pack(pady=10)

dropdown1_label_low = Label(frame_low, text="Bin:", font=("Arial", 12))
dropdown1_label_low.pack(side=LEFT, pady=10)
dropdown1_low = OptionMenu(frame_low, selected_option1_low, *optionsd1)
dropdown1_low.pack(side=LEFT, padx=10)

dropdown2_label_low = Label(frame_low, text="Type:", font=("Arial", 12))
dropdown2_label_low.pack(side=LEFT, pady=10)
dropdown2_low = OptionMenu(frame_low, selected_option2_low, *options2)
dropdown2_low.pack(side=LEFT, padx=10)

dropdown3_label_low = Label(frame_low, text="Color:", font=("Arial", 12))
dropdown3_label_low.pack(side=LEFT, pady=10)
dropdown3_low = OptionMenu(frame_low, selected_option3_low, *options3)
dropdown3_low.pack(side=LEFT, padx=10)

selected_option4_low = StringVar(root)
selected_option4_low.set(options4[0])  # Default value

dropdown4_label_low = Label(frame_low, text="Size:", font=("Arial", 12))
dropdown4_label_low.pack(side=LEFT, pady=10)
dropdown4_low = OptionMenu(frame_low, selected_option4_low, *options4)
dropdown4_low.pack(side=LEFT, padx=10)


# Set Button to allocate sorting type for Low Level Bin
def set_sorting_low():
    bin_number = selected_option1_low.get()
    bin_type = selected_option2_low.get()
    bin_color = selected_option3_low.get()
    messagebox.showinfo("Set Sorting", f"Low Level Bin {bin_number} set to Type: {bin_type}, Color: {bin_color}")
    update_sorting_options(bin_number, bin_type, bin_color, "Low")

set_button_low = Button(frame_low, text="Set", font=("Arial", 12), command=set_sorting_low, bg="blue", fg="white")
set_button_low.pack(side=LEFT, padx=10)

# Button to display the sorting table
def display_sorting_table_scrollable():
    table_window = Toplevel(root)
    table_window.title("Sorting Options Table")
    table_window.geometry("700x500")

    # Create a canvas and a scrollbar
    canvas = Canvas(table_window)
    scrollbar = Scrollbar(table_window, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Configure the canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Table headers
    headers = ["Bin Number", "Type", "Color", "Size"]
    for col, header in enumerate(headers):
        header_label = Label(scrollable_frame, text=header, font=("Arial", 12, "bold"), borderwidth=2, relief="solid", width=15)
        header_label.grid(row=0, column=col, padx=5, pady=5)

    # Table content
    for row, (bin_number, options) in enumerate(sorting_options.items(), start=1):
        bin_label = Label(scrollable_frame, text=bin_number, font=("Arial", 12), borderwidth=2, relief="solid", width=15)
        bin_label.grid(row=row, column=0, padx=5, pady=5)

        type_label = Label(scrollable_frame, text=options["Type"], font=("Arial", 12), borderwidth=2, relief="solid", width=15)
        type_label.grid(row=row, column=1, padx=5, pady=5)

        color_label = Label(scrollable_frame, text=options["Color"], font=("Arial", 12), borderwidth=2, relief="solid", width=15)
        color_label.grid(row=row, column=2, padx=5, pady=5)

        size_label = Label(scrollable_frame, text=options["Size"], font=("Arial", 12), borderwidth=2, relief="solid", width=15)
        size_label.grid(row=row, column=3, padx=5, pady=5)

# Button to display the sorting table
table_button = Button(root, text="Show Sorting Table", font=("Arial", 12), command=display_sorting_table_scrollable, bg="purple", fg="white")
table_button.pack(pady=20)


label = Label(root)
label.pack(pady=10)

def auto_detect():
    with open('Image/response.txt', 'r') as f:
        content = f.read().strip()
        label.config(text=f"Detected LEGO: {content}", font=("Helvetica", 9))
    root.after(100, auto_detect)

auto_detect()
root.mainloop()