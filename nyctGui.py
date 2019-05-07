from Tkinter import *


master = Tk()

w = Canvas(master, width=1000, height=300)
w.pack()

w.create_oval(50, 50, 250, 250, fill="green4")

w.create_text(150, 150, anchor="center", fill='white', font=("Georgia", 100, 'bold'),
              text="6")

w.create_text(275, 150, anchor="w", font=("Georgia", 70, 'bold'), text="Uptown")

mainloop()
