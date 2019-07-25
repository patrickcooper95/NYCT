import Queue
import Tkinter as tk

WIDTH = 1000
HEIGHT = 300


class TrainFrame:

    def __init__(self, master, queue, status_command, train_thread, train_condition):
        self.queue = queue
        console = tk.Button(master, text='Close', command=status_command)
        console.pack()

        self.io_thread = train_thread
        self.cv = train_condition
        self.window = tk.Canvas(master, width=WIDTH, height=HEIGHT)
        self.window.pack()
        self.oval = self.window.create_oval(50, 50, 250, 250, fill="green4")
        self.train_num = self.window.create_text(150, 150, fill='white', font=('Helvetica', 100, 'bold'))
        self.train_dir = self.window.create_text(275, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.train_time = self.window.create_text(700, 150, anchor='w', font=('Helvetica', 50, 'bold'))
        self.min_type = self.window.create_text(800, 150, anchor='w', font=('Helvetica', 50, 'bold'), text="min")

    def update_text(self):
        self.cv.acquire()
        while self.queue.empty():
            self.cv.wait()
        current_train = self.queue.get(0)
        self.window.itemconfigure(self.train_num, text=current_train.loc['Service'])
        self.window.itemconfigure(self.train_dir, text=current_train.loc['Destination'])
        self.window.itemconfigure(self.train_time, text=current_train.loc['ETA'])
        self.cv.release()


root = tk.Tk()
