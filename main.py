
import re
from tkinter import *
from itertools import groupby
import threading
import random
import string
import os
import sys
keyboard_patterns = [
    "qwerty", "qwertyuiop",
    "azerty", "azertyuiop",
    "zxcvbn", "asdfgh",
    "123456", "12345678",
    "abcdef", "abcdefgh"
]
common_passwords = set()
def get_data_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
filepath = get_data_path("rockyou.txt")

def load_passwords():
    global common_passwords
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        common_passwords = set(line.strip() for line in f)
    print("passwords loaded!")
    button.config(state=NORMAL)


def upper_lower(s):
    T=re.findall(r'[A-Z]',s)
    S=len(T)
    T=re.findall(r'[a-z]',s)
    R=len(T)
    if R>0:
        return S/R
    return S



def special(s):
    S=re.findall(r'[^A-Za-z0-9]',s)
    R=len(S)
    if len(s)>0:
        return R/len(s)



def numbers(s):
    T=re.findall(r'[0-9]',s)
    S=len(T)
    if len(s)>0:
        return S/len(s)



def string_in_file(s):
    if s in common_passwords:
                    return True
    else:
        return False




def check_repetition(s):
    for key, group in groupby(s):
        if len(list(group)) >= 3:
            return True
    return False


def check_pattern(s):
    s_lower = s.lower()
    for pattern in keyboard_patterns:
        if pattern in s_lower:
            return True
    return False


def check_word_year(s):
    if re.search(r'[A-Za-z]+[0-9]{4}', s):
        return True
    return False


def randomize():
    entry.delete(0, END)
    length=random.randint(12, 20)
    chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()_+-=[]{}"),
    ]
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}"
    chars += [random.choice(all_chars) for _ in range(length - 4)]
    random.shuffle(chars)
    entry.insert(0, "".join(chars))
    return 0
def check():
    button.config(state=DISABLED)
    s=entry.get()
    point = 0
    tips = []
    S=len(s)
    if S==0:
        result.config(text="Do not enter a empty password", foreground="red")
        button.config(state=NORMAL)
        return 0
    if S>12:
        point+=1
    elif S>10:
        point+=0.5
        tips.append("Try a Password longer than 12 Letters")
    elif S<8:
        result.config(text="Enter a Password longer than 8 characters", foreground="red")
        button.config(state=NORMAL)
        return 0
    if " " in s:
        result.config(text="No spaces allowed!", foreground="red")
        button.config(state=NORMAL)
        return

    S=upper_lower(s)
    if S>0.3:
        point+=1
    elif S!=0:
        point+=0.5
    else:
        tips.append("Do a Mix Between Upper and Lower Cases")


    S = special(s)
    if S>0.2:
        point+=1.5
    elif S!=0:
        point+=1
    else:
        tips.append("Try Using a Special Characters")


    S=string_in_file(s)
    if S:
        tips.append( "This Password is Very Common")
    else:
        point+=1


    S = numbers(s)
    if S>=0.2:
        point+=1
    elif S!=0:
        point+=0.5
    else:
        tips.append("Try Adding Numbers")


    S=check_repetition(s)
    if S==False:
        point+=1
    else:
        tips.append("Avoid Repeating The Letters ")


    S=check_pattern(s)
    if S==False:
        point+=1
    else:
        tips.append("Avoid keyboard patterns like qwerty or azerty")


    S=check_word_year(s)
    if S:
        tips.append("Avoid Password like Hello2024")
    else:
        point+=1

    tips_text = "\n".join(f"• {tip}" for tip in tips)
    tipss.config(text="Tips :\n"+tips_text, justify="left",font=("sans-serif",13,"bold"),fg="brown")
    if point>=6.5:
        result.config(text="This Password is Strong ! ",foreground="green")
        button.config(state=NORMAL)
        return 0
    elif point>=5:
        result.config(text="This Password is med ! ",foreground="yellow")
        button.config(state=NORMAL)
        return 0
    else:
        result.config(text="This Password is Weak ! ",foreground="red")
        button.config(state=NORMAL)
        return 0
window=Tk()
window.geometry("720x500")
window.title("Password Checker")
icon = PhotoImage(file=resource_path("icon.png"))
window.iconphoto(True,icon)
window.config(background="#d1bcae")
window.resizable(False, False)
icon = icon.subsample(15, 15)
label=Label(window,text="Test Your Code :",font=('serif',30,'bold'),fg="black",bg="#d1bcae",image=icon,compound="left")
label.pack()
entry=Entry(window)
entry.config(font=("sans-serif",17,"bold"))
entry.config(width=16)
entry.place(x=300,y=150)
pas=Label(window,text="Enter Your Password ->",font=("sans-serif",13,"bold"),bg="#d1bcae")
pas.place(x=80,y=155)
tipss=Label(window,text="",bg="#d1bcae")
tipss.place(x=50,y=300)
button=Button(window,text="   🔍   ",bg="#0e4003",fg="white",activebackground="#9c8900",font=("sans-serif",13,"bold"))
button.config(command=check)
button.place(x=550,y=150)
button.config(state=DISABLED)
threading.Thread(target=load_passwords, daemon=True).start()
result=Label(window,text="",bg="#d1bcae",font=("sans-serif",13,"bold"))
result.place(x=310,y=200)
thanks=Label(window,text="Thanks for testing my app \nplease don't forget to leave a comment or suggestion ❤️",font=("sans-serif",13,"bold"),bg="#d1bcae")
thanks.place(x=120,y=420)
ran=Label(window,text="Pick Random Password ->",bg="#d1bcae",font=("sans-serif",13,"bold"))
ran.place(x=80,y=250)
randomm=Button(window,text="   🎲   ",command=randomize,fg="white",activebackground="#5c11f2",font=("sans-serif",13,"bold"),bg="#2b0082")
randomm.place(x=350,y=240)
window.mainloop()