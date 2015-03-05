__author__ = 'tieh'

import tkinter as tk

GIFSTART = \
    'R0lGODlhIAAgAPQAAP9rAP9rAf9xCv9yDP90EP92E/93Fv94Fv+BJv+IM/+ZT/+aUf+gW/+vdv+xeP+0fv+3hP+4hP+5hv+7if/F'\
    'm//Rr//dxP/dxf/exv/v5P/27//28P/48v/7+P/+/QAAACH5BAEAAB8ALAAAAAAgACAAAAWr4CeOZGmeaKqqldO8cCzPslN9D6Dv'\
    'fO//ukcBICgYj8ikMikADAGTlXQ04UWn0uruilVpddwu6gsVe60pTGSDJYdLC8CB4smiUYpdArNyp/I7AQwZKX54PgMRHSeGJ4A+'\
    'CBwmjSZxP5GTd46IioyaJo86g4WfJY97faUkcQV0dltpEGxTlGYltbZUqrkfuLy+uVpDRUvFxgVNBTlAzM1BHy000tMvNrzX2CIh'\
    'ADs='

GIFSTOP = \
    'R0lGODlhIAAgAPIAAP9rAP+CJ/+DKv/EmQAAAAAAAAAAAAAAACH5BAEAAAQALAAAAAAgACAAAANiSLrc/jDKSau9OOsNhwhgKI6B'\
    'MFACoK5suwpU4M5tENM4YE9yPu+Snq92GxJ5xmMwyQJGhEwnBJqUPqhGqwM71Da4Pi8DnBMvyDizAk1TE9g/FPNF8ZDuIRNnz+/7'\
    '/4CBEgkAOw=='

def showgif():
    root = tk.Tk()
    p = tk.PhotoImage(data=GIF)
    l = tk.Label(image=p)
    l.pack()
    root.mainloop()


def b64gif():
    import base64
    with open(r'e:\mat\icon\iconsplace\aqua-view-details-32.gif', 'rb') as f:
        sb64 = base64.b64encode(f.read()).decode()
        for i in range(0, len(sb64), 100):
            print("    '%s'\\" % sb64[i:i+100])


class ImgBtton(tk.Button):
    def __init__(self, master=None, *args, **kw):
        tk.Button.__init__(self, master, *args, **kw)
        self.config(relief=tk.FLAT)
        self.config(cursor='hand2')
        self.config(compound='left')
        self.bind('<Enter>', self.onenter)
        self.bind('<Leave>', self.onleave)
        self.oldbg = self.cget('bg')

    def onenter(self, event):
        self.config(bg='#3385FF')

    def onleave(self, event):
        self.config(bg=self.oldbg)


def showbutton():
    root = tk.Tk()
    p = tk.PhotoImage(data=GIFSTOP)
    btn = ImgBtton(root, text='Start', image=p)
    btn.pack()
    root.mainloop()


if __name__ == '__main__':
    #showgif()
    b64gif()
    #showbutton()