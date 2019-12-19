import random
import psycopg2
import pyttsx3
import sys
import speech_recognition as sr
from tkinter import *

quesNo = 0

conn = psycopg2.connect(database="<DB_Name>", user="<Your_User>", password="<Your_Password>", host="localhost", port="5432")
#By default user and database are "postgres"
cur = conn.cursor()
engine = pyttsx3.init()
recording = sr.Recognizer()

win = Tk()
win.title("Interview Round")
win.geometry("350x200")

w1 = Label(win, text="Name: ")
w1.config(font=("Courier", 14))
w1.grid(row=2, column=1, padx=(30,0), pady=(30,5))

user = Entry(win, width=30)
user.grid(row=2, column=2, padx=(0,5), pady=(30,5))

while True:
    res = int(input("Press:\n1 For HR interview questions\n2 For casual interview questions\n \t Your resp: "))
    if res==1 or res==2:
        break

q = "SELECT COUNT(*) FROM ";

if res==1:
    ROUND = "HR"
    q = q+ROUND+";"     
  
else:
    ROUND = "casual"
    q = q+ROUND+";"
    cur.execute(q)

cur.execute(q)
c = list(cur.fetchone())[0]
length = c+1
t = list(range(1, length))
random.shuffle(t)

def close():
    global win, user
    name = user.get()
    fin = "Okay Thank you " + str(name)
    engine.say(fin)
    engine.runAndWait()
    win.destroy()
    sys.exit(0)

def nextQues(ROUND, i):
    global c, quesNo
    cur.execute("SELECT question FROM " + ROUND + " WHERE id="+str(i)+";")
    q = list(cur.fetchone())[0]
    engine.say(q)
    engine.runAndWait()
    quesNo+=1
    if quesNo>=c:
        close()

if(quesNo>=len(t)):
    sys.exit(0)
else:
    try:
        nex = Button(win, text="Next", command=lambda: nextQues(ROUND, t[quesNo]))
        nex.grid(row=4, column=2, padx=(10,75), pady=(30,30))
    except Exception as e:
        close()

if(quesNo>=len(t)):
    sys.exit()

win.resizable(0,0)
win.mainloop()

fin = "Okay Thank you"
engine.say(fin)
engine.runAndWait()
