from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from tkinter import ttk
import sys

def read_data(file_to_read,pos,grab):
    with open(file_to_read,"rb") as opened_file:
        opened_file.seek(pos,0)
        grabed_data=opened_file.read(grab)
    return grabed_data

def to_dec(var):
    var1=int.from_bytes(var,"big")
    return var1

def tobytes(import_var):
    import_var1=(import_var).to_bytes(2,byteorder="big")
    return import_var1

def save_changes():
    if root.filename=="":
        messagebox.showerror(title=app_name, message="Select a PES5/WE9/LE.exe")
    else:
        if backup_check.get():
            with open(root.filename,"rb") as rf_exe:
                chunk_size=4096
                with open(Path(root.filename).stem+".bak","wb") as wf_exe:
                    rf_exe_chunk = rf_exe.read(chunk_size)
                    while len(rf_exe_chunk) >0:
                        wf_exe.write(rf_exe_chunk)
                        rf_exe_chunk = rf_exe.read(chunk_size)
        try:
            with open(root.filename,"r+b") as opened_file:
                offset=0x6E2A77
                if Path(root.filename).stat().st_size ==22793412:
                    offset=0x6E07AF
                for i in range(0,64):
                    opened_file.seek(offset+(i*0x10),0)
                    opened_file.write(tobytes(int(getattr(sys.modules[__name__], f"mycmb_{i}").get())))
                    opened_file.seek(offset+(i*0x10)+2,0)
                    opened_file.write(tobytes(int(getattr(sys.modules[__name__], f"mycmb_{i}").get())))
            messagebox.showinfo(title=app_name, message="Ok!")
            #now we update the flags with the exe to check if there is a error in my programming
            get_flags_ids()
            update_label_name()
        except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=app_name, message="Error while saving PES5/WE9/LE.exe\nplease run as administrator")

def update_cmb(lstf):
    for i in range(0,64):
        getattr(sys.modules[__name__], f"mycmb_{i}").current(lstf[i])

def get_flags_ids():
    count=0
    offset=0x6E2A77
    if Path(root.filename).stat().st_size ==22793412:
        offset=0x6E07AF
    flglst=[]
    for count in range (64):
        x=to_dec(read_data(root.filename,offset+(count*0x10),0X2))
        flglst.append(x)
    if flglst!=[]:
        update_cmb(flglst)

def update_label_name():
    offset=0x6E2A70
    baseaddress=4194304
    if Path(root.filename).stat().st_size ==22793412:
        offset=0x6E07A8
        baseaddress=4200960
    for x in range(0,64):
        nameoffset=int.from_bytes(read_data(root.filename,offset+(x*16),0x4),"little")-baseaddress
        with open(root.filename,"rb") as opened_file:
            opened_file.seek(nameoffset,0)
            name=b''
            ''' #otra forma de leer los nombres en el archivo pero con variables inutiles de todas formas sirve
            for i in range(0,100):
                grabed_data=opened_file.read(1)
                if grabed_data!=b'\x00':
                    name+=grabed_data
                else:
                    break
            '''
            grabed_data=opened_file.read(1)
            while grabed_data!=b'\x00':
                name+=grabed_data
                grabed_data=opened_file.read(1)
        #print(name.decode('utf-8'))
        name=name.decode('utf-8')
        getattr(sys.modules[__name__], f"mylbl_{x}").config(text=name)

def search_exe():
    global my_label
    my_label.destroy()
    root.filename=filedialog.askopenfilename(initialdir=".",title="Select PES5/WE9/LE Executable", filetypes=[("PES5/WE9/LE Executable", "*.exe")])
    if root.filename!='':
        #print(Path(root.filename).stat().st_size)
        my_label= Label(root, text=root.filename)
        my_label.place(x=5,y=480)
        get_flags_ids()
        update_label_name()
    else: # parent of IOError, OSError *and* WindowsError where available
        messagebox.showerror(title=app_name, message="Select a PES5/WE9/LE.exe")

def close():
    root.destroy()

app_name="PES5/WE9/LE National Teams Flag Relink"
root = Tk()
root.title(app_name)
#root.geometry("700x500")
#con el codigo de abajo definimos el tamaño del formulario y tambien hacemos que se posicione en el centro de la pantalla

w = 700 # width for the Tk root
h = 500 # height for the Tk root
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.filename=""

my_btn= Button(root, text="Select a \nPES5/WE9/LE.exe",command=search_exe)
my_btn1= Button(root, text="Save changes",command=save_changes)
my_btn2= Button(root, text="Exit",command=close,width=11)
my_label= Label(root)
backup_check=IntVar()
checkbox_backup=Checkbutton(root, text="Make backup",variable=backup_check)

lst=list(range(288))

#headers labels

mylbl_h1 = Label(root,text="Team name")
mylbl_h2 = Label(root,text="Flag id")
mylbl_h3 = Label(root,text="Team name")
mylbl_h4 = Label(root,text="Flag id")
mylbl_h5 = Label(root,text="Team name")
mylbl_h6 = Label(root,text="Flag id")
mylbl_h7 = Label(root,text="Team name")
mylbl_h8 = Label(root,text="Flag id")

#64 fucking labels


mylbl_0 = Label(root,text="0")
mylbl_1 = Label(root,text="1")
mylbl_2 = Label(root,text="2")
mylbl_3 = Label(root,text="3")
mylbl_4 = Label(root,text="4")
mylbl_5 = Label(root,text="5")
mylbl_6 = Label(root,text="6")
mylbl_7 = Label(root,text="7")
mylbl_8 = Label(root,text="8")
mylbl_9 = Label(root,text="9")
mylbl_10 = Label(root,text="10")
mylbl_11 = Label(root,text="11")
mylbl_12 = Label(root,text="12")
mylbl_13 = Label(root,text="13")
mylbl_14 = Label(root,text="14")
mylbl_15 = Label(root,text="15")
mylbl_16 = Label(root,text="16")
mylbl_17 = Label(root,text="17")
mylbl_18 = Label(root,text="18")
mylbl_19 = Label(root,text="19")
mylbl_20 = Label(root,text="20")
mylbl_21 = Label(root,text="21")
mylbl_22 = Label(root,text="22")
mylbl_23 = Label(root,text="23")
mylbl_24 = Label(root,text="24")
mylbl_25 = Label(root,text="25")
mylbl_26 = Label(root,text="26")
mylbl_27 = Label(root,text="27")
mylbl_28 = Label(root,text="28")
mylbl_29 = Label(root,text="29")
mylbl_30 = Label(root,text="30")
mylbl_31 = Label(root,text="31")
mylbl_32 = Label(root,text="32")
mylbl_33 = Label(root,text="33")
mylbl_34 = Label(root,text="34")
mylbl_35 = Label(root,text="35")
mylbl_36 = Label(root,text="36")
mylbl_37 = Label(root,text="37")
mylbl_38 = Label(root,text="38")
mylbl_39 = Label(root,text="39")
mylbl_40 = Label(root,text="40")
mylbl_41 = Label(root,text="41")
mylbl_42 = Label(root,text="42")
mylbl_43 = Label(root,text="43")
mylbl_44 = Label(root,text="44")
mylbl_45 = Label(root,text="45")
mylbl_46 = Label(root,text="46")
mylbl_47 = Label(root,text="47")
mylbl_48 = Label(root,text="48")
mylbl_49 = Label(root,text="49")
mylbl_50 = Label(root,text="50")
mylbl_51 = Label(root,text="51")
mylbl_52 = Label(root,text="52")
mylbl_53 = Label(root,text="53")
mylbl_54 = Label(root,text="54")
mylbl_55 = Label(root,text="55")
mylbl_56 = Label(root,text="56")
mylbl_57 = Label(root,text="57")
mylbl_58 = Label(root,text="58")
mylbl_59 = Label(root,text="59")
mylbl_60 = Label(root,text="60")
mylbl_61 = Label(root,text="61")
mylbl_62 = Label(root,text="62")
mylbl_63 = Label(root,text="63")

#64 fucking comboboxes

mycmb_0 = ttk.Combobox(root, value=lst,width=3)
mycmb_1 = ttk.Combobox(root, value=lst,width=3)
mycmb_2 = ttk.Combobox(root, value=lst,width=3)
mycmb_3 = ttk.Combobox(root, value=lst,width=3)
mycmb_4 = ttk.Combobox(root, value=lst,width=3)
mycmb_5 = ttk.Combobox(root, value=lst,width=3)
mycmb_6 = ttk.Combobox(root, value=lst,width=3)
mycmb_7 = ttk.Combobox(root, value=lst,width=3)
mycmb_8 = ttk.Combobox(root, value=lst,width=3)
mycmb_9 = ttk.Combobox(root, value=lst,width=3)
mycmb_10 = ttk.Combobox(root, value=lst,width=3)
mycmb_11 = ttk.Combobox(root, value=lst,width=3)
mycmb_12 = ttk.Combobox(root, value=lst,width=3)
mycmb_13 = ttk.Combobox(root, value=lst,width=3)
mycmb_14 = ttk.Combobox(root, value=lst,width=3)
mycmb_15 = ttk.Combobox(root, value=lst,width=3)
mycmb_16 = ttk.Combobox(root, value=lst,width=3)
mycmb_17 = ttk.Combobox(root, value=lst,width=3)
mycmb_18 = ttk.Combobox(root, value=lst,width=3)
mycmb_19 = ttk.Combobox(root, value=lst,width=3)
mycmb_20 = ttk.Combobox(root, value=lst,width=3)
mycmb_21 = ttk.Combobox(root, value=lst,width=3)
mycmb_22 = ttk.Combobox(root, value=lst,width=3)
mycmb_23 = ttk.Combobox(root, value=lst,width=3)
mycmb_24 = ttk.Combobox(root, value=lst,width=3)
mycmb_25 = ttk.Combobox(root, value=lst,width=3)
mycmb_26 = ttk.Combobox(root, value=lst,width=3)
mycmb_27 = ttk.Combobox(root, value=lst,width=3)
mycmb_28 = ttk.Combobox(root, value=lst,width=3)
mycmb_29 = ttk.Combobox(root, value=lst,width=3)
mycmb_30 = ttk.Combobox(root, value=lst,width=3)
mycmb_31 = ttk.Combobox(root, value=lst,width=3)
mycmb_32 = ttk.Combobox(root, value=lst,width=3)
mycmb_33 = ttk.Combobox(root, value=lst,width=3)
mycmb_34 = ttk.Combobox(root, value=lst,width=3)
mycmb_35 = ttk.Combobox(root, value=lst,width=3)
mycmb_36 = ttk.Combobox(root, value=lst,width=3)
mycmb_37 = ttk.Combobox(root, value=lst,width=3)
mycmb_38 = ttk.Combobox(root, value=lst,width=3)
mycmb_39 = ttk.Combobox(root, value=lst,width=3)
mycmb_40 = ttk.Combobox(root, value=lst,width=3)
mycmb_41 = ttk.Combobox(root, value=lst,width=3)
mycmb_42 = ttk.Combobox(root, value=lst,width=3)
mycmb_43 = ttk.Combobox(root, value=lst,width=3)
mycmb_44 = ttk.Combobox(root, value=lst,width=3)
mycmb_45 = ttk.Combobox(root, value=lst,width=3)
mycmb_46 = ttk.Combobox(root, value=lst,width=3)
mycmb_47 = ttk.Combobox(root, value=lst,width=3)
mycmb_48 = ttk.Combobox(root, value=lst,width=3)
mycmb_49 = ttk.Combobox(root, value=lst,width=3)
mycmb_50 = ttk.Combobox(root, value=lst,width=3)
mycmb_51 = ttk.Combobox(root, value=lst,width=3)
mycmb_52 = ttk.Combobox(root, value=lst,width=3)
mycmb_53 = ttk.Combobox(root, value=lst,width=3)
mycmb_54 = ttk.Combobox(root, value=lst,width=3)
mycmb_55 = ttk.Combobox(root, value=lst,width=3)
mycmb_56 = ttk.Combobox(root, value=lst,width=3)
mycmb_57 = ttk.Combobox(root, value=lst,width=3)
mycmb_58 = ttk.Combobox(root, value=lst,width=3)
mycmb_59 = ttk.Combobox(root, value=lst,width=3)
mycmb_60 = ttk.Combobox(root, value=lst,width=3)
mycmb_61 = ttk.Combobox(root, value=lst,width=3)
mycmb_62 = ttk.Combobox(root, value=lst,width=3)
mycmb_63 = ttk.Combobox(root, value=lst,width=3)

#Here comes the positioning of the things in the frame

my_btn.place(x=250,y=380)
checkbox_backup.place(x=400,y=390)
my_btn1.place(x=190,y=440)
my_btn2.place(x=350,y=440)
#headers

for i in range(1,9):
    getattr(sys.modules[__name__], f"mylbl_h{i}").grid(row=0,column=i-1)
'''
mylbl_h1.grid(row=0,column=0)
mylbl_h2.grid(row=0,column=1)
mylbl_h3.grid(row=0,column=2)
mylbl_h4.grid(row=0,column=3)
mylbl_h5.grid(row=0,column=4)
mylbl_h6.grid(row=0,column=5)
mylbl_h7.grid(row=0,column=6)
mylbl_h8.grid(row=0,column=7)
'''
#team ids labels


mylbl_0.grid(row=1,column=0)
mylbl_1.grid(row=2,column=0)
mylbl_2.grid(row=3,column=0)
mylbl_3.grid(row=4,column=0)
mylbl_4.grid(row=5,column=0)
mylbl_5.grid(row=6,column=0)
mylbl_6.grid(row=7,column=0)
mylbl_7.grid(row=8,column=0)
mylbl_8.grid(row=9,column=0)
mylbl_9.grid(row=10,column=0)
mylbl_10.grid(row=11,column=0)
mylbl_11.grid(row=12,column=0)
mylbl_12.grid(row=13,column=0)
mylbl_13.grid(row=14,column=0)
mylbl_14.grid(row=15,column=0)
mylbl_15.grid(row=16,column=0)
mylbl_16.grid(row=1,column=2)
mylbl_17.grid(row=2,column=2)
mylbl_18.grid(row=3,column=2)
mylbl_19.grid(row=4,column=2)
mylbl_20.grid(row=5,column=2)
mylbl_21.grid(row=6,column=2)
mylbl_22.grid(row=7,column=2)
mylbl_23.grid(row=8,column=2)
mylbl_24.grid(row=9,column=2)
mylbl_25.grid(row=10,column=2)
mylbl_26.grid(row=11,column=2)
mylbl_27.grid(row=12,column=2)
mylbl_28.grid(row=13,column=2)
mylbl_29.grid(row=14,column=2)
mylbl_30.grid(row=15,column=2)
mylbl_31.grid(row=16,column=2)
mylbl_32.grid(row=1,column=4)
mylbl_33.grid(row=2,column=4)
mylbl_34.grid(row=3,column=4)
mylbl_35.grid(row=4,column=4)
mylbl_36.grid(row=5,column=4)
mylbl_37.grid(row=6,column=4)
mylbl_38.grid(row=7,column=4)
mylbl_39.grid(row=8,column=4)
mylbl_40.grid(row=9,column=4)
mylbl_41.grid(row=10,column=4)
mylbl_42.grid(row=11,column=4)
mylbl_43.grid(row=12,column=4)
mylbl_44.grid(row=13,column=4)
mylbl_45.grid(row=14,column=4)
mylbl_46.grid(row=15,column=4)
mylbl_47.grid(row=16,column=4)
mylbl_48.grid(row=1,column=6)
mylbl_49.grid(row=2,column=6)
mylbl_50.grid(row=3,column=6)
mylbl_51.grid(row=4,column=6)
mylbl_52.grid(row=5,column=6)
mylbl_53.grid(row=6,column=6)
mylbl_54.grid(row=7,column=6)
mylbl_55.grid(row=8,column=6)
mylbl_56.grid(row=9,column=6)
mylbl_57.grid(row=10,column=6)
mylbl_58.grid(row=11,column=6)
mylbl_59.grid(row=12,column=6)
mylbl_60.grid(row=13,column=6)
mylbl_61.grid(row=14,column=6)
mylbl_62.grid(row=15,column=6)
mylbl_63.grid(row=16,column=6)

#combos for flags ids

mycmb_0.grid(row=1,column=1)
mycmb_1.grid(row=2,column=1)
mycmb_2.grid(row=3,column=1)
mycmb_3.grid(row=4,column=1)
mycmb_4.grid(row=5,column=1)
mycmb_5.grid(row=6,column=1)
mycmb_6.grid(row=7,column=1)
mycmb_7.grid(row=8,column=1)
mycmb_8.grid(row=9,column=1)
mycmb_9.grid(row=10,column=1)
mycmb_10.grid(row=11,column=1)
mycmb_11.grid(row=12,column=1)
mycmb_12.grid(row=13,column=1)
mycmb_13.grid(row=14,column=1)
mycmb_14.grid(row=15,column=1)
mycmb_15.grid(row=16,column=1)
mycmb_16.grid(row=1,column=3)
mycmb_17.grid(row=2,column=3)
mycmb_18.grid(row=3,column=3)
mycmb_19.grid(row=4,column=3)
mycmb_20.grid(row=5,column=3)
mycmb_21.grid(row=6,column=3)
mycmb_22.grid(row=7,column=3)
mycmb_23.grid(row=8,column=3)
mycmb_24.grid(row=9,column=3)
mycmb_25.grid(row=10,column=3)
mycmb_26.grid(row=11,column=3)
mycmb_27.grid(row=12,column=3)
mycmb_28.grid(row=13,column=3)
mycmb_29.grid(row=14,column=3)
mycmb_30.grid(row=15,column=3)
mycmb_31.grid(row=16,column=3)
mycmb_32.grid(row=1,column=5)
mycmb_33.grid(row=2,column=5)
mycmb_34.grid(row=3,column=5)
mycmb_35.grid(row=4,column=5)
mycmb_36.grid(row=5,column=5)
mycmb_37.grid(row=6,column=5)
mycmb_38.grid(row=7,column=5)
mycmb_39.grid(row=8,column=5)
mycmb_40.grid(row=9,column=5)
mycmb_41.grid(row=10,column=5)
mycmb_42.grid(row=11,column=5)
mycmb_43.grid(row=12,column=5)
mycmb_44.grid(row=13,column=5)
mycmb_45.grid(row=14,column=5)
mycmb_46.grid(row=15,column=5)
mycmb_47.grid(row=16,column=5)
mycmb_48.grid(row=1,column=7)
mycmb_49.grid(row=2,column=7)
mycmb_50.grid(row=3,column=7)
mycmb_51.grid(row=4,column=7)
mycmb_52.grid(row=5,column=7)
mycmb_53.grid(row=6,column=7)
mycmb_54.grid(row=7,column=7)
mycmb_55.grid(row=8,column=7)
mycmb_56.grid(row=9,column=7)
mycmb_57.grid(row=10,column=7)
mycmb_58.grid(row=11,column=7)
mycmb_59.grid(row=12,column=7)
mycmb_60.grid(row=13,column=7)
mycmb_61.grid(row=14,column=7)
mycmb_62.grid(row=15,column=7)
mycmb_63.grid(row=16,column=7)

root.resizable(False, False)
root.mainloop()