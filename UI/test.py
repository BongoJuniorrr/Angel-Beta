from customtkinter import *
from PIL import Image,ImageTk
import time

def wait_there():
    var = IntVar()
    app.after(3000, var.set, 1)
    app.wait_variable(var)



app = CTk()
app.title("Angel Asistant")
app.geometry("800x600")
set_appearance_mode("dark")

#intro

    

#load hinh angel
my_img = CTkImage(light_image=Image.open('angel2.jpg'),size=(300,100))
guest = CTkImage(light_image =Image.open('guest2.jpg'),size=(300,100))
#tieude
global name
name=CTkLabel(master=app, text="Angel", font=("000GosmickSansTB",70) , text_color = "#343434",image=my_img)
#boxchat
textbox = CTkTextbox(master = app, width=650,height=400, scrollbar_button_color = "#FFCC70", corner_radius=16, border_color="#FFCC70", border_width=5,font=("000GosmickSansTB",20))
#dat vitri
name.place(relx=0.5, rely=0.1, anchor="center")
textbox.place(relx=0.5, rely=0.55, anchor="center")


intro = CTkImage(light_image=Image.open('intro.png'), size=(800,600))
lab = CTkLabel(master=app, text="", image=intro)
lab.place(relx=0,rely=0)

def xoaten():
    name.destroy()
def doi1():
    xoaten()
    global name
    name=CTkLabel(master=app, text="Angel", font=("000GosmickSansTB",70) , text_color = "#343434",image =guest)
    name.place(relx=0.5, rely=0.1, anchor="center")
def doi2():
    xoaten()
    global name
    name=CTkLabel(master=app, text="Angel", font=("000GosmickSansTB",70) , text_color = "#343434",image=my_img)
    name.place(relx=0.5, rely=0.1, anchor="center")
def send_message():
    # Lấy tin nhắn từ hộp nhập liệu
    #ham message lay tu voice
    doi1()
    message = "adfsfds"
    # Thêm tin nhắn vào hộp thoại
    textbox.insert("end", f"[Bạn]: {message}\n")
    
def reply_message():
    doi2()
    reply = "thuaa"  #Angle reply
    textbox.insert("end", f"[ANGLE]: {reply}\n")
    textbox.see('end')

    

def on_enter(event):
    # Nếu phím enter được nhấn, thì gọi hàm send_message()
    if event.keysym == "Return":
        lab.destroy()
        send_message()
        wait_there()
        reply_message()
        

app.bind("<Return>", on_enter)

app.mainloop()

