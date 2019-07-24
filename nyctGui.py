import nyctLive
import Queue
import threading
import time
import TrainFrame as tf
import sys


class UpdateThread:
    """UpdateThread manages asynchronous threads to queue new Train data for the GUI application

    By starting a new thread, the GUI thread (run through the Tkinter master object) is uninterrupted by
    the worker thread, which periodically requests updates from the MTA API.

    Attributes:
        master: Tkinter root thread object.
        queue: a Queue object used to store and push new trains to the GUI thread.
        gui: instance of the TrainFrame class containing the TKinter Canvas on which train data is displayed.
        running: an Integer controlling execution. If the "Close" button on the GUI is pressed, this will switch to 0
        and execution will cease.
        io_thread: an instance of the Thread class used to create the thread on which the background data is updated
        using the MTA API.
        periodic_call(): runs the update_text() function from the TrainFrame class every 2 seconds, until self.running
        is no longer equal to 1
        data_thread(): by calling the create_trains() function of the nyctLive class, creates a new pandas DataFrame
        of index 5, prints to the console for debugging, puts to the queue for the GUI, and sleeps for 3 seconds to
        allow some time for the trains to be displayed on the GUI before the DataFrame updates and more are added to
        the queue.
        end_application(): this function is called by the command attribute of the Tkinter button class. When "Close"
        is pressed, the function is run and self.running = 0, therefore stopping execution.
    """
    def __init__(self, master):
        self.master = master
        self.queue = Queue.Queue()

        # Create thread to handle I/O
        self.running = 1
        self.cv = threading.Condition()
        self.io_thread = threading.Thread(target=self.data_thread)
        self.io_thread.start()
        self.gui = tf.TrainFrame(master, self.queue, self.end_application, self.io_thread, self.cv)
        self.periodic_call()

    def periodic_call(self):
        self.gui.update_text()
        if not self.running:
            sys.exit(1)
        self.master.after(2000, self.periodic_call)

    def data_thread(self):
        while self.running:
            # Import train data from nyctLive py file
            # Trim the results to 5 trains and delete the object containing the function return
            self.cv.acquire()
            trains = nyctLive.train_main()
            new_trains = trains.iloc[:5]
            self.cv.notify()
            self.cv.release()
            del trains

            new_trains = new_trains.astype({'ETA': int})
            print new_trains
            for index, row in new_trains.iterrows():
                self.queue.put(row)
                time.sleep(3)
            del new_trains

    def end_application(self):
        self.running = 0


if __name__ == "__main__":
    root = tf.root
    client = UpdateThread(root)
    root.mainloop()
