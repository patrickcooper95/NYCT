import Queue
import Tkinter as tk


class TrainFrame:

    def __init__(self, master, queue, status_command):
        self.queue = queue
        console = tk.Button(master, text='Close', command=status_command)
        console.pack()

        self.window = tk.Canvas(master, width=1000, height=300)
        self.window.pack()
        self.oval = self.window.create_oval(50, 50, 250, 250, fill="green4")
        self.train_num = self.window.create_text(150, 150, fill='white', font=('Helvetica', 100, 'bold'))
        self.train_dir = self.window.create_text(275, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.train_time = self.window.create_text(700, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.min_type = self.window.create_text(800, 150, anchor='w', font=('Helvetica', 50, 'bold'), text="min")

    def update_text(self):
        while self.queue.qsize():
            try:
                current_train = self.queue.get(0)
                self.window.itemconfigure(self.train_num, text=current_train.loc['Service'])
                self.window.itemconfigure(self.train_dir, text=current_train.loc['Destination'])
                self.window.itemconfigure(self.train_time, text=current_train.loc['ETA'])
            except Queue.Empty:
                pass


root = tk.Tk()
