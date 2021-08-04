import tkinter as tk
import nyctLive
import queue
import threading
import time
import random


class TrainFrame:

    def __init__(self, master, queue, status_command):
        self.queue = queue
        console = tk.Button(master, text='Close', command=status_command)
        console.pack()
        master.title('Subway Countdown Clock')

        self.window = tk.Canvas(master, width=1000, height=300)
        self.window.pack()
        self.oval = self.window.create_oval(50, 50, 250, 250, fill="green4")
        self.train_num = self.window.create_text(150, 150, fill='white', font=('Helvetica', 100, 'bold'))
        self.train_dir = self.window.create_text(275, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.train_time = self.window.create_text(700, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.min_type = self.window.create_text(790, 150, anchor='w', font=('Helvetica', 50, 'bold'), text="min")

    def update_text(self):
        while self.queue.qsize():
            try:
                current_train = self.queue.get(0)
                self.window.itemconfigure(self.train_num, text=current_train.loc['Service'])
                self.window.itemconfigure(self.train_dir, text=current_train.loc['Destination'])
                self.window.itemconfigure(self.train_time, text=current_train.loc['ETA'])
            except queue.Empty:
                pass


class UpdateThread:

    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()
        self.gui = TrainFrame(master, self.queue, self.end_application)

        # Create thread to handle I/O
        self.running = 1
        self.thread1 = threading.Thread(target=self.worker_thread1)
        self.thread1.start()

        self.periodic_call()

    def periodic_call(self):
        self.gui.update_text()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(1000, self.periodic_call)

    def worker_thread1(self):
        while self.running:
            # Import train data from nyctLive py file
            # Trim the results to 5 trains and delete the object containing the function return
            trains = nyctLive.create_trains()
            new_trains = trains.iloc[:5]
            del trains

            new_trains = new_trains.astype({'ETA': int})
            # print new_trains
            for index, row in new_trains.iterrows():
                self.queue.put(row)
                time.sleep(3)
            del new_trains

    def end_application(self):
        self.running = 0


rand = random.Random()
root = tk.Tk()
client = UpdateThread(root)
root.mainloop()
