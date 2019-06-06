import Tkinter as tk
import nyctLive
import numpy as np

trains = nyctLive.create_trains()
trains = trains.iloc[:5]
print trains


class TrainFrame:

    def __init__(self, master, trains):
        window = tk.Canvas(master, width=1000, height=300)
        window.pack()
        self.trains = trains
        self.oval = window.create_oval(50, 50, 250, 250, fill="green4")
        self.train_num = window.create_text(150, 150, fill='white', font=('Helvetica', 100, 'bold'))
        self.train_dir = window.create_text(275, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.train_time = window.create_text(700, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.min_type = window.create_text(800, 150, anchor='w', font=('Helvetica', 50, 'bold'), text="min")



    count_of_trains = np.array(trains['Service'])
    count_of_destination = np.array(trains['Destination'])
    count_of_ETA = np.array(trains['ETA'])
    count_of_ETA = count_of_ETA.astype('int')
    go_through_trains = (t for t in count_of_trains)
    go_through_destinations = (t for t in count_of_destination)
    go_through_ETA = (t for t in count_of_ETA)


    def canvas_animation(self):
        try:
            window.itemconfigure(train_num, text=next(go_through_trains))
            window.itemconfigure(train_dir, text=next(go_through_destinations))
            window.itemconfigure(train_time, text=next(go_through_ETA))
            master.after(2000, canvas_animation)
        except StopIteration:
            pass


canvas_animation()
master.mainloop()
