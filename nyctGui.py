from Tkinter import *
import nyctLive

trains = nyctLive.create_trains()
train_time = int(trains.iloc[0][4])
train_time_str = str(train_time) + " min"
print train_time_str


master = Tk()

w = Canvas(master, width=1000, height=300)
w.pack()

w.create_oval(50, 50, 250, 250, fill="green4")

w.create_text(150, 150, anchor="center", fill='white', font=("Georgia", 100, 'bold'),
              text=trains.iloc[1][0])

w.create_text(275, 150, anchor="w", font=("Georgia", 50, 'bold'), text=trains.iloc[0][1])

w.create_text(700, 150, anchor="w", font=("Georgia", 50, 'bold'), text=train_time_str)

mainloop()
