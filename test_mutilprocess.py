from tkinter import *
import time,threading,random
from multiprocessing import Process,Queue,Event

class winApp:
    def __init__(self, q, process1, process2):
        self.queue = q
        self.process1 = process1
        self.process2 = process2
        self.root = Tk()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww = 500
        wh = 100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.__running_text = Event()
        self.__running_text.set()
        self.root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

        self.frm_text = Frame(self.root, width=10, height=10)
        self.lable = Label(self.frm_text, text='线程计数：')
        self.text = Entry(self.frm_text, text='',width=100)
        self.frm_text.pack(side=TOP, padx=10, pady=1)
        self.lable.pack(side=LEFT, padx=10, pady=1)
        self.text.pack(side=LEFT, padx=10, pady=1)

        self.frm = Frame(self.root, width=10, height=10)
        self.butn_start = Button(self.frm, text='start',width=10, height=10,command= self.start)
        self.butn_pasue = Button(self.frm, text='pause',width=10, height=10,command= self.pause)
        self.butn_resume = Button(self.frm, text='resume',width=10, height=10,command= self.resume)
        self.butn_stop = Button(self.frm, text='stop',width=10, height=10,command= self.stop)
        self.frm.pack(side=TOP, padx=10, pady=1)
        self.butn_start.pack(side=LEFT, padx=10, pady=1)
        self.butn_pasue.pack(side=LEFT, padx=10, pady=1)
        self.butn_resume.pack(side=LEFT, padx=10, pady=1)
        self.butn_stop.pack(side=LEFT, padx=10, pady=1)

        self.root.bind('<Escape>', lambda e: self.shutdown())
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)


    def start(self):
        # self.process1 = myProcess(self.queue, 'ProcessID-1', 2, 3)
        # self.process2 = myProcess(self.queue, 'ProcessID-2', 2, 3)

        if not self.process1.is_alive():
            self.process1.start()
            print(self.process1.pid)
        if not self.process2.is_alive():
            self.process2.start()
            print(self.process2.pid)

        self.text_threading = threading.Thread(target=self.write_text)
        self.text_threading.start()
        print("start!")

    def pause(self):
        self.process1.pause()
        self.process2.pause()
        self.__running_text.clear()
        print("pause!")

    def resume(self):
        self.__running_text.set()
        self.process1.resume()
        self.process2.resume()
        print("resume!")

    def stop(self):
        self.process1.stop()
        self.process2.stop()
        self.__running_text.clear()
        print("stop!")

    def write_text(self):
        while self.__running_text.wait():
            if not self.queue.empty():
                self.text.delete(0, END)
                self.string = self.queue.get() + '+' +str(self.queue.qsize())
                self.text.insert(0, self.string)

    def shutdown(self):
        self.process1.stop()
        self.process2.stop()
        self.process1.terminate()
        self.process2.terminate()
        self.__running_text = False
        self.root.destroy()

class myProcess(Process):
    def __init__(self, q, ProcessorID, name, delay):
        super(myProcess, self).__init__()
        self.ProcessorID = ProcessorID
        self.name = name
        self.delay = delay
        self.queue = q
        self.__running = Event()
        self.__running.set()
        self.__flag = Event()
        self.__flag.set()
    def run(self):
        print("开始线程：" + self.name)
        self.counter = 1
        while self.__running.is_set():
            self.__flag.wait()
            s = print_time(self.queue, self.name, self.delay, self.counter)
            self.queue.put(s)
            self.counter += 1

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()


def print_time(q, ProcessName, delay, counter):
    time.sleep(delay)
    string = "%s: %s  %d" % (ProcessName, time.ctime(time.time()), counter)
    s = string + '++++' + str(q.qsize())
    print(s)
    return s



if __name__ == '__main__':
    q = Queue()
    pr1 = myProcess(q, 1, 'ProcessID-1', 2)
    pr2 = myProcess(q, 2, 'ProcessID-2', 2)
    app = winApp(q, pr1, pr2)
    app.root.mainloop()
