from tkinter import Tk, Label, Button, filedialog
from tkinter import *
import os
# from src import recognizer




def getProofVideo():
    filename = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                          filetypes=(("jpeg files", "*.mp4"), ("all files", "*.*")))
    if filename == ():
        pass
    else:
        #recognizer.uploadVideo(filename)
        videoButton.set(os.path.basename(filename))

def getPhoto():
    filename = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    if filename == ():
        pass
    else:
        photoButton.set(os.path.basename(filename))


window = Tk()
window.geometry("740x500")
window.title("Title")
videoButton = StringVar(value="Select Video")
photoButton = StringVar(value="Select Photo Directory of format png or jpg")
# Label(window, , font=("Ubuntu", 24), justify='center').pack()
welcomeText = ("Please select a 'proof of life' video, and a historical photo \n"
               "that will be used to test if the two are simular\n"
               "For best performance, use a high resolution photo")
Label(window, text=welcomeText, font=("ubuntu", 20), anchor=W, justify=CENTER).grid(row=0)
Button(window, textvariable=videoButton, command=getProofVideo).grid(row=1, column=0)
Button(window, textvariable=photoButton, command=getPhoto).grid(row=2, column=0)

window.mainloop()