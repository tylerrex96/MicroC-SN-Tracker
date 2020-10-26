import tkinter as tk
from datetime import datetime
from time import sleep
import RPI.GPIO as io
io.setmode(io.BCM)
io.setup(4,io.OUT)



def read_file():  #delete old text entry, read the file and post the up to date list
    serials_file.delete("1.0", tk.END)
    with open("Serials.txt", "r") as f:
        a = f.read()
        f.close()
    serials_file.insert(tk.END, a)
    invalid.config(text="Waiting for input.")


def save_serial():
    serial_number = serial_entry.get()
    if serial_number[0] == "S" and len(serial_number) == 13:   #validate the S/N
        now = datetime.now()   #store file in memory, write new line at top, restore rest of file. PITA way to prepend
        with open("Serials.txt","r+") as f:
            a = f.read()
            with open("Serials.txt", "w+") as f:
                f.write("Serial number: " + serial_number + now.strftime(" %m/%d/%Y, %H:%M:%S \n" + a))   #save S/N with time and date
        read_file()
        invalid.config(text="Success!")
    else:
        invalid.config(text="**Error! Invalid S/N.")
        io.output(4,1)
        sleep(1)
        io.output(4,0)


io.output(4,0)
window = tk.Tk()
window.title("Serial Number Logging")


#defining and drawing basic frames
submitframe = tk.Frame(window)
invalid = tk.Label(submitframe, text="Waiting for input.", font=("Helvetica", "15", "bold"))
listframe = tk.Frame(window)
serial_entry = tk.Entry(submitframe, width=15, font=("Helvetica", "15"))
btn_submit = tk.Button(submitframe, text="Submit", command=save_serial, relief=tk.RAISED)
window.bind("<Return>", lambda event=None: btn_submit.invoke())  #i dont even know what this is some guy on the internet said it worked and it does
btn_refresh = tk.Button(listframe, text="Refresh List", command=read_file, relief=tk.RAISED)
serials_file = tk.Text(listframe, width=45, height=50, font=("Helvetica"))


read_file()  #auto-populating the readout


submitframe.pack(side="top", pady=25, padx=25, fill="both")
listframe.pack(side="top", pady=25, padx=25, fill="y")
invalid.pack(side="bottom", pady=10)
btn_submit.pack(side="bottom", pady=10)
serial_entry.pack(side="top")
btn_refresh.pack(side="bottom", pady=10)
serials_file.pack(side="bottom", fill="both")


window.mainloop()