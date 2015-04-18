from tkinter import *


def onresize(event):
    pass

root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


label = Label(root, width=20, height=10, text='bitch', bg='blue')
canvas = Canvas(root, width=20, height=50, bg='black')

label.grid(row=0, column=0, sticky='nswe')
canvas.grid(row=1, column=0, sticky='nswe')

root.bind('<Configure>', onresize)



