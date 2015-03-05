import sys
import time
import datetime
import signal
import subprocess
import threading
import queue
import tkinter as tk
import tkinter.font as tkfont
import idlelib.WidgetRedirector


__author__ = 'Tie Hu'
__email__ = "feht@163.com"
__version__ = "0.1.0-20141201"

'''base64-encoded gif image for logo'''
LOGO = \
    'R0lGODlhIAAgAPYAAP8AAP8BAf8CAv8DA/8EBP8FBf8HB/8ICP8JCf8KCv8LC/8ODv8REf8WFv8YGP8bG/8gIP8iIv8jI/8oKP8p'\
    'Kf8wMP8zM/87O/9AQP9BQf9ERP9ISP9MTP9NTf9OTv9PT/9QUP9RUf9UVP9XV/9YWP9eXv9gYP9mZv9paf9wcP9xcf9zc/91df92'\
    'dv95ef96ev97e/99ff+Bgf+Cgv+Dg/+Fhf+Hh/+Li/+Ojv+Skv+Xl/+YmP+hof+iov+kpP+mpv+np/+oqP+urv+wsP+ysv+zs/+1'\
    'tf+5uf+7u//AwP/Gxv/IyP/Kyv/Ozv/Q0P/S0v/T0//V1f/b2//d3f/j4//k5P/m5v/n5//o6P/p6f/q6v/r6//u7v/v7//w8P/x'\
    '8f/09P/19f/29v/5+f/7+//8/P/9/QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'\
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAGcALAAAAAAgACAAAAf+gGdaLBgjSWeIiYqLjItaEACRAECNZ15GMygnMEFalWcs'\
    'kpENZYtKIwSikQQjT40YqgBTiVYhsaoEMaWKJLheiEUMt7cdYYpJqiaIO8PNHbuIQA0ABCbGPM3ZMItlU79nTwjZ2a6VF+PZIZVI'\
    '6NkEVo297c08jGXC88MsjTP5wyWV+vlLxkjLmDMCB0batqhJh4MJBwZh5AXAQ4QKAXhiRMEixIEbKoXyiDEfkkpAJF2MmE3DJyOi'\
    'VqJDIOUTs5gfs1GqZEVCLJnDbnyKAolYTlEEcnwqsiAb0EgVllQqMyOVqAc4hPBQAWklgg5FoC0K0yGWg1mKtCiBd0ZsoxIjsRBI'\
    '/UQ3UYVYO+vWxaFKhd6/Y2xFwnDwr94yNSiE4GJYbyAAOw=='\

'''base64-encoded gif image for 'Start' button'''
GIFSTART = \
    'R0lGODlhIAAgAMQAAP9rAP9rAf9xCv9yDP90EP92E/93Fv94Fv+BJv+IM/+ZT/+aUf+gW/+vdv+xeP+0fv+3hP+4hP+5hv+7if/F'\
    'm//Rr//dxP/dxf/exv/v5P/27//28P/48v/7+P/+/QAAACH5BAEAAB8ALAAAAAAgACAAAAVj4CeOZGmeaKqqQOu+cCy332zfeK6/'\
    'az/GPh8wuBoSU8bjKVlyBZkkWA/6k7KsSxkSa7pleShcl9v0lsFf7Ri9JkfdVXaaFpbPAVu8EK4UUfs1fH1/g4JKO4iJilKLOYCP'\
    'kCUhADs='\

'''base64-encoded gif image for 'Stop' button'''
GIFSTOP = \
    'R0lGODlhIAAgAMQAAP9rAP9rAf9xCv9yDP90EP92E/93Fv94Fv+BJv+IM/+ZT/+aUf+gW/+vdv+xeP+0fv+3hP+4hP+5hv+7if/F'\
    'm//Rr//dxP/dxf/exv/v5P/27//28P/48v/7+P/+/QAAACH5BAEAAB8ALAAAAAAgACAAAAVf4CeOZGmeaKqqQOu+cCy332zfeK6/'\
    'az/GPh8wuBoSU8bjKaksMX+3JUyKMz1rOetUW3VuvV3SVcd1UaNgc9m2BpzZaVpb1kaFxd9m3K2v9/d/gIFQO4WGh2aIWYOMSiEA'\
    'Ow=='

'''base64-encoded gif image for 'Statistics' button'''
GIFSUMMARY = \
    'R0lGODlhIAAgAPQAAAD//wf//yf//yr//zv//z3//0///1f//2L//3T//4n//53//6z//7v//8P//8T//83//9b//9v//+z//+//'\
    '//L///P//wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABcALAAAAAAgACAAAAXp4GUdAWCeaKqewWFdV7LONJrABTAo'\
    'fO//wN4AUIARAAaYcslsLg0AghHprFqh0ssxae0+o1Ou14sNj8dlLRXmWDBgjYV8Tl84lOmtEgEQwKA1CHhgamJ8fheANIJ/hHow'\
    'FhQUkBMTFJaVmBQvjVmPZ1eOa6BVeaMSDxAwEQ+trq8PEoOeo4eNgbNmMLaJNQCMvbRiqKoXrLCwsp26pE6mYs1Mz0qRkyKZl5eV'\
    'l5zBzLyKM8DTu323i7mFSm1vF3F1dXfL6tFN5PVfwvjSotD79/u8XcixI4hBg0OKxPDFMMUNESQa+mrxIgQAOw=='

'''base64-encoded gif image for 'Clear All' button'''
GIFCLEAR = \
    'R0lGODlhIAAgAPUAAP/OAP/OAf/OBP/PB//QDv/REv/SFf/SGP/TGv/UI//VJP/VJ//XMP/ZO//bRP/dTv/dT//dUf/hYv/kdv/m'\
    'fP/mff/mf//oif/oi//pj//rlv/snf/vqv/vq//wsP/wsf/yvf/0xP/0yf/20f/31v/32P/54P/65P/65f/77P/88f/++P/++f/+'\
    '+//+/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAC8ALAAAAAAgACAAAAb+'\
    'wJdwSHyRIAOAEjCAkIrQ6HBUWFoBhZF0O2woI5QwJaJscLcnpQQqUZ7OwlVqngIpNXS6RgnKr6ImVVeDhEsFJlAfhYuEH0UcDoyS'\
    'Sw4cRBOTmQATRBgLC0oHn6MJBwgIBwmjnwdKnxhQKUobcEQbSilSsgC0tUK3ALlRu7QnEBAiRhARTyLHb8DCsbMvJUqOIUohL4oA'\
    'JS/RutTWANja3Erf4cPj1y/ZANvd6rjivNXu8PLp4PXs9+TMxUPnrV8we7QCvjs3z6C0IsTwlVs4sOG6aQDzMeR3EWK7ifoI0jv4'\
    'L6HGihz9YTQJcmPBjkQiKgxpUaXHjC1RvrQZ86M7wH07Sa584WLOHzkpjs5x4VCKCiUZfAnJoETFFlAGKGDYyrVrVwoGACzgwkHT'\
    'IEtcPjBIkmkAA0dFggAAOw=='

'''base64-encoded gif image for 'Toggle Console' button'''
GIFWIN = \
    'R0lGODlhIAAgAPUAAAAAAAEBAQMDAwQEBAgICA8PDxMTEx0dHR4eHicnJysrKy0tLTY2Njs7Ozw8PE9PT1FRUVRUVFhYWFlZWV9f'\
    'X2BgYGJiYmZmZn19fX5+foODg4mJiY+Pj5SUlJmZmaSkpLCwsLa2trm5ubu7u9TU1ODg4Orq6uzs7PHx8fb29v39/QAAAAAAAAAA'\
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACsALAAAAAAgACAAAAbM'\
    'wNWIMQAYj8ik8jhgjITFpXTKHAIKmI12y+16t5gCgAjArM7otHqtxgCiG7Z8ft4g4/R82n7E6/V8Rn5/dIEAg4RyhoiJa4uNhXeQ'\
    'c4+TbJWWapiZaJucK56coZmGGp9pGkgHHyCtrq+wsa4fB1S2SwMDBkdit74jKhJXFL6+JCtuFCYKxbYKFQQKJispHhbX1xUV1wlK'\
    'Cdnb2BceKX8PShCnKxxKHeorKCfyJyiWJBEP+fr7/A8QT3kcNDuyQA+FBggTKlyYUMK7P0EAADs='

'''Maximum lines of log show in view'''
MAX_LINES = 9999


def toggleconsole():
    """
    Hide or show the console window
    :return:
    """
    import win32console
    import win32gui
    hd = win32console.GetConsoleWindow()
    if win32gui.IsWindowVisible(hd):
        win32gui.ShowWindow(hd, 0)
    else:
        win32gui.ShowWindow(hd, 5)


def askoverwrite(path):
    """
    Check whether the file is exists and ask for overwrite
    :param path: False if exists and choose do not overwrite
    :return:
    """
    import os
    import tkinter.messagebox as tkmsgbox
    if os.path.exists(path) and not tkmsgbox.askyesno('覆盖', path + ' 已存在。\n是否覆盖?'):
        return False
    return True


def req_statistics(subproc):
    if subproc:
        subproc.poll()
        if subproc.returncode is None:
            subproc.send_signal(signal.CTRL_BREAK_EVENT)


def req_stop(subproc):
    if subproc:
        subproc.poll()
        if subproc.returncode is None:
            subproc.send_signal(signal.CTRL_BREAK_EVENT)
            subproc.send_signal(signal.SIGTERM)
            subproc.wait()  # must wait subprocess exit or log.write in read_thread_func will throw ValueError


def period_thread_func(subproc):
    while True:
        time.sleep(60)
        req_statistics(subproc)


def read_thread_func(subproc, log, view):
    while True:
        for line in subproc.stdout:
            d = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f] ')
            l = d + line.replace(b'\r', b' ').decode(sys.getfilesystemencoding())

            # save to log file
            if log:
                try:
                    log.write(l)
                    log.flush()
                except ValueError:
                    print('Write error: ' + l)
                    log.close()
                    log = None

            # show in log view
            if view is not None:
                view.write(l)


def pinglog(ip, log, view):
    if log is None:
        log = sys.stdout

    # 创建 ping 进程
    cmd = ["ping", "-t", ip]
    p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, stdout=subprocess.PIPE)
    
    # 创建周期进程，周期发统计请求
    t = threading.Thread(target=period_thread_func, name='PeriodStat', args=(p, ), daemon=True)
    t.start()

    # 创建读进程
    t = threading.Thread(target=read_thread_func, name='Read', args=(p, log, view), daemon=True)
    t.start()
    
    return p


class ImgButton(tk.Button):
    def __init__(self, master=None, *args, **kw):
        tk.Button.__init__(self, master, *args, **kw)
        self.myfont = tkfont.Font(family='Helvetica', size=10, weight='bold')
        self.config(font=self.myfont)
        self.config(relief=tk.FLAT)
        self.config(cursor='hand2')
        self.config(compound='left')
        self.bind('<Enter>', self.onenter)
        self.bind('<Leave>', self.onleave)
        self.oldbg = self.cget('bg')

    def onenter(self, event):
        self.config(bg='#87CEFA')

    def onleave(self, event):
        self.config(bg=self.oldbg)


class ROText(tk.Text):
    def __init__(self, *args, **kw):
        tk.Text.__init__(self, *args, **kw)
        self.redirector = idlelib.WidgetRedirector.WidgetRedirector(self)
        self.insert = self.redirector.register("insert", lambda *args2, **kw2: "break")
        self.delete = self.redirector.register("delete", lambda *args2, **kw2: "break")


class ThreadSafeROText(ROText):
    def __init__(self, master, **options):
        ROText.__init__(self, master, **options)
        self.queue = queue.Queue()
        self.update_me()

    def write(self, line):
        self.queue.put(line)

    def clear(self):
        self.queue.put(None)

    def update_me(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, tk.END)
                else:
                    # truncate if more than 9999 line
                    try:
                        nline = int(self.index(tk.END).split('.')[0])
                        if nline > MAX_LINES:
                            self.delete('1.0', tk.END)
                    except ValueError:
                        print('Failed to get number of lines!')
                    self.insert(tk.END, str(line))
                self.see(tk.END)
                self.update_idletasks()
        except queue.Empty:
            pass
        self.after(100, self.update_me)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Tk Ping')
        p = tk.PhotoImage(data=LOGO)
        self.wm_iconphoto(True, p)
        self.resizable(0, 0)  # disable resize/maximize
        self.myfont = tkfont.Font(family='Helvetica', size=10)
        self.mybfont = tkfont.Font(family='Helvetica', size=10, weight='bold')

        self.ip = tk.StringVar()
        self.ip.set('192.168.1.1')
        self.needLog = tk.IntVar()
        self.needLog.set(1)
        self.logPath = tk.StringVar()
        self.logPath.set('ping.log')
        self.editLogPath = None
        self.logView = None
        self.btnPing = None

        self.flog = None
        self.subproc = None
        self.pinging = False

        self.gifstart = tk.PhotoImage(data=GIFSTART)
        self.gifstop = tk.PhotoImage(data=GIFSTOP)
        self.gifsummary = tk.PhotoImage(data=GIFSUMMARY)
        self.gifclear = tk.PhotoImage(data=GIFCLEAR)
        self.gifwin = tk.PhotoImage(data=GIFWIN)

        self.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.exit_ping)  # stop ping before exit by click X

    def create_widgets(self):
        # Create button frame
        btnframe = tk.Frame(self)
        self.btnPing = ImgButton(btnframe, text=" Start Ping", command=self.toggle_ping, image=self.gifstart)
        btn_stat = ImgButton(btnframe, text=" Statistics", command=self.stat_ping, image=self.gifsummary)
        btn_clear = ImgButton(btnframe, text=" Clear All", command=self.clear_log_view, image=self.gifclear)
        btn_show = ImgButton(btnframe, text=" Toggle Console", command=toggleconsole, image=self.gifwin)

        # Create input frame
        inframe = tk.Frame(self)
        lip = tk.Label(inframe, text="IP: ", font=self.mybfont)
        eip = tk.Entry(inframe, textvariable=self.ip, width='50', font=self.myfont)
        cklog = tk.Checkbutton(inframe, variable=self.needLog, text="Log Path: ",
                               command=self.toggle_log, font=self.mybfont)
        self.editLogPath = tk.Entry(inframe, textvariable=self.logPath, width='50', font=self.myfont)

        # Create outout frame
        logframe = tk.Frame(self)
        self.logView = ThreadSafeROText(logframe)
        scrollbar = tk.Scrollbar(logframe, command=self.logView.yview)
        self.logView.config(yscrollcommand=scrollbar.set)

        # Layout main
        self.columnconfigure(1, weight=1)
        btnframe.grid(row=0, sticky=tk.W, pady=5)
        inframe.grid(row=1, sticky=tk.W, padx=5)
        logframe.grid(row=2)

        # Layout button frame
        self.btnPing.grid(row=0, column=0, padx=5)
        btn_stat.grid(row=0, column=1)
        btn_clear.grid(row=0, column=2, padx=5)
        btn_show.grid(row=0, column=3)

        # Layout input frame
        lip.grid(row=0, column=0, sticky=tk.W, padx=5)
        eip.grid(row=0, column=1, sticky=tk.W)
        cklog.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.editLogPath.grid(row=1, column=1, sticky=tk.W)

        # Layout outout frame
        self.logView.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

    def toggle_log(self):
        if self.needLog.get():
            self.editLogPath.config(state=tk.NORMAL)
        else:
            self.editLogPath.config(state=tk.DISABLED)
    
    def toggle_ping(self):
        if self.pinging:
            self.stop_ping()
        else:
            self.start_ping()

    def start_ping(self):
        ip = self.ip.get()
        needlog = self.needLog.get()
        logpath = self.logPath.get()

        if needlog and logpath:
            if askoverwrite(logpath):
                self.flog = open(logpath, 'w')
            else:
                self.editLogPath.selection_range(0, tk.END)
                self.editLogPath.icursor(tk.END)
                self.editLogPath.focus_set()
                return
        else:
            self.flog = None
        self.subproc = pinglog(ip, self.flog, self.logView)
        self.pinging = True
        self.btnPing.config(image=self.gifstop)
        self.btnPing.config(text=' Stop Ping')
        
    def stop_ping(self):
        req_stop(self.subproc)
        if self.flog:
            self.flog.close()
        self.pinging = False
        self.btnPing.config(image=self.gifstart)
        self.btnPing.config(text=' Start Ping')

    def exit_ping(self, event=None):
        self.stop_ping()
        self.destroy()

    def stat_ping(self):
        req_statistics(self.subproc)
        
    def clear_log_view(self):
        self.logView.clear()


def guiping():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    toggleconsole()
    guiping()
