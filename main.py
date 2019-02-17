from tkinter import Tk, Label, Button, filedialog
from tkinter import *
import os
from src import recognizer


req = recognizer.Recognizer(True)


def getProofVideo():
    filename = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                          filetypes=(("jpeg files", "*.mp4"), ("all files", "*.*")))
    if filename == ():
        pass
    else:
        req.uploadVideo(filename)
        videoButton.set(os.path.basename(filename))


def getPhoto():
    fileDir = filedialog.askdirectory()
    if fileDir == ():
        pass
    else:
        req.createProfile("Verified Face", fileDir)
        photoButton.set(os.path.basename(fileDir))


def varify():
    # data = {"percent": .90, "frame_percentages": [1,2,3,4,5,5], "frames_total": 45}

    data = req.verify(showPreview=popup)

    faceInFramePercent = str(data["percent"] * 100)

    message = ( u"\u2713" + "Accuracy of video: {}%\nPercentage of frames with a face {} = {} ".format(faceInFramePercent
        , (str(len(data["frames_percentages"])) + "/" + str(data["frames_total"])),
        '{0:.3g}'.format((len(data["frames_percentages"]) / data["frames_total"]) * 100)))

    messageBox.set(message)

popup = False
window = Tk()
window.configure(bg="#f58625")
window.geometry("543x300")
window.title("Face Verifier")
videoButton = StringVar(value="Select Video")
photoButton = StringVar(value="Select Photo Directory of format png or jpg")
messageBox = StringVar()
welcomeText = ("Please select a 'proof of life' video, and a historical photo \n"
               "that will be used to test if the two are similar\n"
               "For best performance, use high resolution photos")
Label(window, text=welcomeText, font=("ubuntu", 15), justify=CENTER, bg="#17365d", fg="white").grid(row=0, sticky=EW, columnspan=1, pady=(0, 5))
Button(window, textvariable=videoButton, command=getProofVideo).grid(row=1, column=0, pady=3)
Button(window, textvariable=photoButton, command=getPhoto).grid(row=2, column=0, pady=3)
Button(window, command=varify, text="Compute accuracy of video").grid(row=3, pady=3)
Checkbutton(window, text="Show Popup Preview of the magic", variable=popup, bg="#f58625").grid(row=4, pady=3)
Label(window, textvariable=messageBox, wraplength=450, font=("ubuntu", 12), bg="#f58625").grid(row=5, pady=3)
window.mainloop()
