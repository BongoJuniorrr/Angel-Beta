from customtkinter import *
from PIL import Image,ImageTk

app = CTk()
app.title("Angel Asistant")
app.geometry("800x600")
set_appearance_mode("dark")

my_img = CTkImage(light_image=Image.open('angel2.jpg'),size=(300,100))
name=CTkLabel(master=app, text="Angel", font=("000GosmickSansTB",70) , text_color = "#343434",image=my_img)


textbox = CTkTextbox(master = app, width=650,height=400, scrollbar_button_color = "#FFCC70", corner_radius=16, border_color="#FFCC70", border_width=5,font=("000GosmickSansTB",20))
name.place(relx=0.5, rely=0.1, anchor="center")
textbox.place(relx=0.5, rely=0.55, anchor="center")



app.mainloop()