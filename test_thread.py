from tkinter import *
import time,threading,random
from queue import Queue

class winApp:
    def __init__(self, thread):
        self.tread = thread
        self.root = Tk()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww = 500
        wh = 100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.__running_text = True
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
        self.text_threading = threading.Thread(target=self.write_text)
        self.text_threading.start()
        self.tread.start()
        print("start!")

    def pause(self):
        self.tread.pause()
        print("pause!")

    def resume(self):
        self.tread.resume()
        print("resume!")

    def stop(self):
        self.tread.stop()
        self.__running_text = False
        print("stop!")

    def write_text(self):
        while self.__running_text:
            if not self.tread.queue.empty():
                self.text.delete(0, END)
                self.text.insert(0, self.tread.queue.get())

    def shutdown(self):
        self.tread.stop()
        self.__running_text = False
        self.root.destroy()

class myThread(threading.Thread):
    def __init__(self,ThreadID, name, counter):
        super(myThread, self).__init__()
        self.ThreadID = ThreadID
        self.name = name
        self.queue = Queue(100)
        self.counter = counter
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        print("开始线程：" + self.name)
        self.jishu = 1
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.queue.put(print_time(self.name, self.counter, self.jishu))
            self.jishu += 1

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False

def print_time(threadName, delay, counter):
    time.sleep(delay)
    string = "%s: %s  %d" % (threadName, time.ctime(time.time()), counter)
    print(string)
    return string

if __name__ == '__main__':
    mythread = myThread(1, "Thread-1", 1)
    app = winApp(mythread)
    app.root.mainloop()