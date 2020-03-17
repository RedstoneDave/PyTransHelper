import tkinter as tk
import tkinter.messagebox as msgbox
import io
import sys

class TkOstream(io.IOBase):
    def __init__(self, fl):
        self.fl = fl
        self.q = str()
        self.doflush = False

    def write(self, x):
        x = str(x)
        self.q += x
        print(self.q,end='')

    def flush(self):
        self.q = str()

#sout = TkOstream(lambda x:msgbox.showinfo("Test",x))
#sys.stdout = sout
serr = TkOstream(lambda x:msgbox.showerror("Error",x))
sys.stderr = serr
