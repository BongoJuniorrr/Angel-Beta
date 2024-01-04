import pyttsx3
import speech_recognition
from datetime  import datetime
import chatbot
import ObjectDetection as YOLO
import cv2
import requests, json 
import time
import asyncio
import numpy as np
import customtkinter
from customtkinter import *
from PIL import Image,ImageTk
import time
import textscanning as scanner
from llama_cpp import Llama
import cv2
import numpy as np
import pickle
import sqlite3
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

#Captioning Model
import captioning as Caption
def predict_capture(cam_port):
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    res, frame = cam.read()
    
    if res:
        cv2.imwrite("./Images/CAP.png", frame)
    else:
        print("Cannot capture image")
        exit()
    

#Answering Model
monglanghehon = "./mistral-7b-openorca.Q4_K_M.gguf"
model = Llama(
            model_path=monglanghehon,
            n_gpu_layers=1,
            n_ctx=4096
            )
global template
template = f"""
<|im_start|>system
Angel
<|im_end|>
"""

def Make_Chatbot_Faster_Again():
    chatbot.reply("hello")
    inp = "Wish you a good day, Angel!"
    template1 = f"""
<|im_start|>user
{inp}
<|im_end|>
"""
    query = ""
    query+=template1
    output = model.create_completion(template+'\n'+query+'\n'+"<|im_start|>assistant", max_tokens=1000,  stop=["<|im_end|>"], stream=True)
    res = ""
    for token in output:
        print(token["choices"][0]["text"], end='', flush=True)
        res+=token["choices"][0]["text"]
    template2 = f"""
<|im_start|>assistant
{res}
<|im_end|>
"""

Make_Chatbot_Faster_Again()

# Khởi tạo bộ phát hiện khuôn mặt
faceDetect=cv2.CascadeClassifier('./face_recognizer/haarcascade_frontalface_default.xml');

# Khởi tạo bộ nhận diện khuôn mặt
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./face_recognizer/recognizer/trainner.yml')

id=0
#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)

# Hàm lấy thông tin người dùng qua ID
def getProfile(id):
    conn=sqlite3.connect("./face_recognizer/FaceBaseNew.db")
    cursor=conn.execute("SELECT * FROM People WHERE ID="+str(id))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

# Load a model
capture = cv2.VideoCapture(0)


#Assistant named ANGEL

#Initialize
robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()
voices = robot_mouth.getProperty('voices')
robot_mouth.setProperty('voice', voices[1].id)
robot_brain = ""
you = ""

#Initialize the Object Detection function
Detector = YOLO.Object_Detection("0")

#Capture function
def capture_image(cam_port):
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    res, frame = cam.read()
    
    if res:
        cv2.imwrite("./Images/IMG.png", frame)
    else:
        print("Cannot capture image")
        exit()
        
def capture_text(cam_port):
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    res, frame = cam.read()
    
    if res:
        cv2.imwrite("./Images/TEXT.png", frame)
        
    else:
        print("Cannot capture image")
        exit()

# Image
# capture_image(0)
img = "./Images/IMG.png"

#Init UI Controller
app = CTk()
app.title("Angel Asistant")
app.geometry("800x600")
set_appearance_mode("dark")

#Face detection UI
fmy_img = CTkImage(light_image=Image.open('./UI/angel2.jpg'),size=(300,100))
fname=CTkLabel(master=app, text="Angel", font=("000GosmickSansTB",70) , text_color = "#343434",image=fmy_img)
fname.place(relx=0.5, rely=0.1, anchor="center")
#UI Controller
def wait_there():
    var = IntVar()
    app.after(1000, var.set, 1)
    app.wait_variable(var)
def img_wait():
    var = IntVar()
    app.after(100, var.set, 1)
    app.wait_variable(var)

#intro
#load hinh angel
my_img = CTkImage(light_image=Image.open('./UI/angel2.jpg'),size=(300,100))
guest = CTkImage(light_image =Image.open('./UI/guest2.jpg'),size=(300,100))
#tieude
global name
name=CTkLabel(master=app, text="Angel", font=("000GosmickSansTB",70) , text_color = "#343434",image=my_img)
#boxchat
global textbox
textbox = CTkTextbox(master = app, width=650,height=400, scrollbar_button_color = "#FFCC70", corner_radius=16, border_color="#FFCC70", border_width=5,font=("000GosmickSansTB",20))
textbox.place(relx=0.5, rely=0.55, anchor="center")
#dat vitri
name.place(relx=0.5, rely=0.1, anchor="center")

intro = CTkImage(light_image=Image.open('./UI/intro.png'), size=(800,600))
global lab
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
def send_message(message):
    # Lấy tin nhắn từ hộp nhập liệu
    #ham message lay tu voice
    doi1()
    wait_there()
    # Thêm tin nhắn vào hộp thoại
    textbox.insert("end", f"[Bạn]: {message}\n")
    wait_there()
    
def reply_message(reply):
    doi2()
    wait_there()
    textbox.insert("end", f"[ANGEL]: {reply}\n")
    textbox.see('end')
    wait_there()
    
def Mistral_update(reply):
    img_wait()
    textbox.insert("end",f"{reply}")
    textbox.see('end')
    img_wait()

def image_update(img,check):
    your_image = customtkinter.CTkImage(light_image=img, size=(650, 400))
    ftextbox = CTkLabel(master=app, image=your_image, text='')
    ftextbox.place(relx=0.5, rely=0.55, anchor="center")
    img_wait()
    ftextbox.destroy()
    if (check):
        print("Destroyed!")
        wait_there()

def FaceDetector():
    cam=cv2.VideoCapture(0)
    username = ""
    while(True):

        # Đọc ảnh từ camera
        ret,img=cam.read()
        color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        pil_image = Image.fromarray(color_coverted) 
        image_update(pil_image,False)
        # Lật ảnh cho đỡ bị ngược
        img = cv2.flip(img, 1)

        # Vẽ khung chữ nhật để định vị vùng người dùng đưa mặt vào
        centerH = img.shape[0] // 2
        centerW = img.shape[1] // 2
        sizeboxW = 650
        sizeboxH = 400
        check = False
        cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                    (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

        # Chuyển ảnh về xám
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Phát hiện các khuôn mặt trong ảnh camera
        faces=faceDetect.detectMultiScale(gray,1.3,5)

        # Lặp qua các khuôn mặt nhận được để hiện thông tin
        for(x,y,w,h) in faces:
            # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và dist (độ sai khác)
            id,dist=recognizer.predict(gray[y:y+h,x:x+w])

            profile=None

            # Nếu độ sai khác < 75% thì lấy profile
            if (dist<=75):
                profile=getProfile(id)

            # Hiển thị thông tin tên người hoặc Unknown nếu không tìm thấy
            if(profile!=None):
                #cv2.putText(img, "Name: " + str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor ,2)
                check = True
                username = str(profile[1])
            else:
                pass
                #cv2.putText(img, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor1, 2)
        if check==True:
            image_update(pil_image,True)
            break
    cam.release()
    return username

def UI_out(reply):
    str = reply
    reply_message(str)

def on_enter(event):
    # Nếu phím enter được nhấn, thì gọi hàm send_message()
    lab.destroy()
    wait_there()
    username = FaceDetector()
    Program.robot_brain = f"Hello {username}!"
    UI_out(Program.robot_brain)
    Program.Say()
    Program.run()
    
def loop():
    wait_there()
    username = FaceDetector()
    Program.robot_brain = f"Hello {username}!"
    UI_out(Program.robot_brain)
    Program.Say()
    Program.run()
#Assistant Class
class Assistant:
    
    #Initialize
    def __init__(self, ear, mouth, brain, you = "", isExit = False):
        self.robot_ear = ear
        self.robot_mouth = mouth
        self.robot_brain = brain
        self.you = ""
        self.isExit = isExit
        self.talker_name =  ""
        self.playlist_count = 0
        self.tester_mode = False
        self.todoList = []
        self.reminders = []
        self.results = None
        self.timedOut = 0
        self.preans1 = "-1"
        self.preans2 = "-1"
        self.query = f"""
"""
    
    def tester_listen(self):
        self.you = input("You: ")
        self.you = self.you.lower()
    
    def tester_say(self):
        UI_out(self.robot_brain)
    
    def get_current_day(self, day):
        ans = str(day)
        day = int(day)
        if (day%10 == 1):
            ans = ans + "st"
        elif (day%10 == 2):
            ans = ans + "nd"
        elif (day%10 == 3):
            ans = ans + "rd"
        else:
            ans = ans + "th"
        return ans
    
    def get_current_month(self,month):
        ans = ""
        month = int(month)
        if (month == 1):
            ans = "January"
        elif (month == 2):
            ans = "February"
        elif (month == 3):
            ans = "March"
        elif (month == 4):
            ans = "April"
        elif (month == 5):
            ans = "May"
        elif (month == 6):
            ans = "June"
        elif (month == 7):
            ans = "July"
        elif (month == 8):
            ans = "August"
        elif (month == 9):
            ans = "September"
        elif (month == 10):
            ans = "October"
        elif (month == 11):
            ans = "November"
        else:
            ans = "December"
        return ans
    
    def process_answer(self,answer):
        answer = answer.replace("bing","Angel")
        answer = answer.replace("Bing","Angel")
        answer = answer.replace("chatgpt","")
        answer = answer.replace("gpt-3","")
        answer = answer.replace("gpt-4","")
        answer = answer.replace("gpt","")
        answer = answer.replace("openai","")
        answer = answer.replace("chatbot","")
        answer = answer.replace("bot","")
        return answer
         
    def get_current_name(self,you):
        name = ""
        you = " " + you
        i = len(you) - 1
        while you[i] != ' ':
            name=you[i] + name
            i-=1
        return name
    
    def get_current_a(self,name):
        pattern = ['a', 'i', 'e', 'o', 'u']
        if (len(name) == 0):
            return "Nothing!"
        if (name[0] in pattern):
            return "an"
        else:
            return "a"
    
    def get_object_list(self,DATA):
        ans = "I will list from the left to the right! \n"
        cnt = 0
        for data in DATA:
            ans= ans + data + ','
            cnt += 1
        if (cnt==0):
            ans="Nothing!"
        return ans
    
    def get_current_city(self,city,country):
        city.replace("city","")
        city = city.lower()
        country = country.lower()
        path = open('country_code.json')
        data = json.load(path)
        for i in data:
            if (i["Name"].lower() == country):
                country = i["Code"]
                break
        if ("vietnam" in country):
            country = "VN"
        path.close()
        return "{}, {}".format(city,country)
    
    def clean_search_info(self,info):
        ans = "Please tell me information about " + info + " shortly"
        return ans
    
    def clean_remind_request(self,request):
        request = request.replace("remind me to","")
        request = request.replace("remind me","")
        request = request.replace("remind to","")
        request = request.replace("remind","")
        request = request.replace("at","-")
        job = ""
        time = ""
        for i in request:
            if i=='-':
                break
            else:
                job+=i
        check=False
        for i in request:
            if i=='-':
                check=True
            if check and i!='-':
                time+=i
        for i in job:
            if i==' ':
                i=''
        for i in time:
            if i==' ':
                i=''
        return job,time
    
    def save_to_do_list(self):
        f = open("./logs/to-do-list.txt","w")
        for task in self.todoList:
            f.write(task+'-')
        f.close()
        
    def load_to_do_list(self):
        f = open("./logs/to-do-list.txt","r")
        task = ""
        for st in f:
            for i in st:
                if i!='-':
                    task+=i
                else:
                    self.todoList.append(task)
                    task=""
        f.close()
        
    def format_time(self,time_str):
        try:
            time_str = time_str.replace(".","")
            # Remove leading and trailing whitespace from the input time string
            time_str = time_str.strip()

            # Define the format for parsing the input time string
            if 'a.m' in time_str.lower() or 'am' in time_str.lower():
                time_format = "%I:%M %p"
            elif 'p.m' in time_str.lower() or 'pm' in time_str.lower():
                time_format = "%I:%M %p"
            else:
                raise ValueError("Invalid time string format")

            # Parse the input time string and format it to 24-hour format
            time_obj = datetime.strptime(time_str, time_format)

            # Extract hour and minute from the time object
            hour = int(time_obj.strftime("%H"))
            minute = int(time_obj.strftime("%M"))

            return "Passed",hour, minute
        except:
            return "Failed","",""
    
    def add_reminder(self, hour, minute, reminder_message):
        self.reminders.append((hour, minute, reminder_message))

    def check_reminders(self):
        DATA = []
        current_time = time.strftime('%H:%M')
        current_hour, current_minute = map(int, current_time.split(':'))

        for hour, minute, reminder_message in self.reminders:
            if current_hour == hour and current_minute == minute:
                DATA.append(reminder_message)
                UI_out(f"Reminder: {reminder_message}")
        return DATA

    def save_to_log(self, log_filename="./logs/remind.txt"):
        with open(log_filename, 'w') as file:
            for hour, minute, reminder_message in self.reminders:
                file.write(f"{hour}:{minute} {reminder_message}\n")

    def load_from_log(self, log_filename="./logs/remind.txt"):
        with open(log_filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(' ')
                time_parts = parts[0].split(':')
                hour, minute = map(int, time_parts)
                reminder_message = ' '.join(parts[1:])
                self.add_reminder(hour, minute, reminder_message)
                
    
    def Mistral(self,inp):
        template1 = f"""
<|im_start|>user
{inp}
<|im_end|>
"""
        self.query+=template1
        global template
        output = model.create_completion(template+'\n'+self.query+'\n'+"<|im_start|>assistant", max_tokens=1000,  stop=["<|im_end|>"], stream=True)
        res = ""
        textbox.insert("end", f"[ANGEL]: ")
        check = False
        for token in output:
            if "gpt" in token["choices"][0]["text"]:
                token["choices"][0]["text"]=""
            if token["choices"][0]["text"]=='\n':
                check = True
            if check == True:
                Mistral_update(token["choices"][0]["text"])
                res+=token["choices"][0]["text"]
        template2 = f"""
<|im_start|>assistant
{res}
<|im_end|>
"""     
        textbox.insert("end", f"\n")
        textbox.see('end')
        self.query+=template2
        return res
    
    def Listen(self): 
        self.you = ""
        if self.tester_mode == True:
            self.tester_listen()
            return
        UI_out("...")
        with speech_recognition.Microphone() as source:
            #self.robot_ear.adjust_for_ambient_noise(source, 1)
            audio = self.robot_ear.listen(source,phrase_time_limit = 10)
        try:
            self.you = self.robot_ear.recognize_google(audio)
        except:
            self.you = ""
        
        try:
            self.you = self.you.lower()
        except:
            self.you = ""
        send_message(self.you)
    
    def Brain(self):
        
        if (self.isExit):
            return
        
        check = False
        self.isSay = True
        you = self.you
        
        try:
            response = chatbot.reply(you)
        except:
            response = ""
        
        if you=="":
            self.robot_brain = "Nah..."
            self.timedOut+=1
    
        elif you=="thanks" or you=="thank you":
            self.robot_brain = "You're welcome!"
        
        elif "who are you" in you:
            self.robot_brain = "I'm Angel. I'll be your eyes!"
        
        elif "time" in you:
            curr = datetime.now()
            time = "{} hours, {} minutes, {} seconds".format(curr.hour, curr.minute, curr.second)
            self.robot_brain = time
        
        elif "date" in response or "date" in you:
            today = datetime.now()
            day = self.get_current_day(today.day)
            month = self.get_current_month(today.month)
            year = today.year
            ans = "{}, {}, {}".format(day, month, year)
            self.robot_brain = ans
          
        elif "weather" in response or "weather" in you:
            api_key = "fe8d8c65cf345889139d8e545f57819a" #generate your own api key from open weather
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            country = "Vietnam"
            city = "Nha Trang"
            city_name = self.get_current_city(city, country)
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure= y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                r = ("Temperature is " +
                    str(int(current_temperature)) + " degree celsius . " +
                    "Atmospheric pressure " + str(current_pressure) + " hpa unit . " +
                    "Humidity is " + str(current_humidiy) + " percent . "
                    "And " + str(weather_description))
                self.robot_brain = r
            else:
                self.robot_brain = "City not found!"  
            
        elif "to-do list" in you or "to do list" in you:
            if "create" in you or "add" in you:
                self.robot_brain = "Ok! I will add to the list until you say stop!"
                self.Say()
                self.Listen()
                while True:
                    if self.you == "stop":
                        self.robot_brain = "Saved!"
                        self.save_to_do_list()
                        break
                    else:
                        self.todoList.append(self.you)
                        self.robot_brain = "Added!"
                        self.Say()
                        self.Listen()
            elif "remove" in you or "clear" in you:
                self.robot_brain = "Ok! I will remove the list!"
                self.todoList = []
            else:
                self.robot_brain = "Here is your to do list:"
                self.Say()
                for task in self.todoList:
                    self.robot_brain = task
                    self.Say()
                self.robot_brain = ""
            
        elif "remind me" in you:
            you = self.you
            job,time = self.clean_remind_request(you)
            answer = "Ok, I will remind you to " + job + " at " + time
            isOk,hour,minute = self.format_time(time)
            if (isOk == "Passed"):
                self.add_reminder(hour,minute,job)
                self.robot_brain = answer
            else:
                self.robot_brain = "Time format error"
        
        elif response == "object_detection" or "what is it" in you or "what is this" in you:
            #List objects (sorted by xmin, ymin)
            capture_image(0)
            Detector.list_objects(img)
            fi = open("./logs/objects_res.txt", "r")
            DATA = []
            cnt = 0

            # Correct the while loop condition
            while True:
                obj = fi.readline().strip()  # Read one line from the file
                if not obj:
                    break  # Exit the loop if there are no more lines
                DATA.append(obj)
                cnt += 1

            fi.close()  # Close the file after reading

            if cnt == 0:
                self.robot_brain = "Nothing!"
            elif cnt == 1:
                self.robot_brain = "There is {} {} in front of you!".format(self.get_current_a(DATA[0]), DATA[0])
            else:
                self.robot_brain = "There are {} objects in front of you.".format(len(DATA))
                for obj in DATA:
                    self.robot_brain += " {} {} , ".format(self.get_current_a(obj), obj)

        elif "caption" in you:
            #Image Captioning
            predict_capture(0)
            self.robot_brain = Caption.predict_step("./Images/CAP.png")
        
        elif response == "text_scanning":
            #Scanning documents
            
            #Capture
            capture_text(0)
            scanner.run()
            fi = open("./logs/text_log.txt","r")
            self.robot_brain = fi.read()
            
        elif "bye" in you or "see you" in you or "see ya" in you or "turn off" in you:
            self.robot_brain = response
            self.isExit = True
        
        else:
            #self.robot_brain = response
            check = True
            self.robot_brain = self.Mistral(self.you)
        
        if self.timedOut>=3 and self.preans1=="" and self.preans2=="" and self.you=="":
            self.isExit = True
            self.timedOut = 0
            self.robot_brain = "Restarting..."
        
        if (self.isSay and not self.tester_mode and not check):
            UI_out(self.robot_brain)
            
        self.preans1 = self.preans2
        self.preans2 = self.you
    
    def Say(self):
        if self.tester_mode == True:
            self.tester_say()
            return
        brain = self.robot_brain
        mouth = self.robot_mouth
        mouth.say(brain)
        self.robot_mouth.runAndWait()
    
    def run(self):
        #Running loop
        # self.load_to_do_list()
        # self.load_from_log()
        while True:
            if (self.isExit):
                # UI_out("Angel: Have a nice day!")
                # self.robot_mouth.say("Have a nice day!")
                self.robot_mouth.runAndWait()
                #self.save_to_do_list()
                break
            #DATA = self.check_reminders()
            # for task in DATA:
            #     self.robot_brain = "It's time to " + task
            #     self.Say()
            self.Listen()
            self.Brain()
            self.Say()
        # self.save_to_do_list()
        # self.save_to_log()
        if self.you == "turn off":
            print("Finished...")
            exit(0)
        self.isExit = False
        self.timedOut = 3
        self.preans1 = "-1"
        self.preans2 = "-1"
        loop()
            
    def tester(self):
        #Test Mode
        self.load_to_do_list()
        self.tester_mode = True
        while True:
            if (self.isExit):
                # UI_out("Angel: Have a nice day!")
                # self.robot_mouth.say("Have a nice day!")
                self.robot_mouth.runAndWait()
                self.save_to_do_list()
                break
            self.Listen()
            self.Brain()
            self.Say()

print("Running...")       
Program = Assistant(robot_ear, robot_mouth, robot_brain)
app.bind("<Return>",on_enter)
app.mainloop()
print("Finished...")