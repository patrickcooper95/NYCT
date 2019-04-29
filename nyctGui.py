from Tkinter import *


master = Tk()

w = Canvas(master, width=1000, height=300)
w.pack()

w.create_oval(50, 50, 250, 250, fill="green4")

mainloop()