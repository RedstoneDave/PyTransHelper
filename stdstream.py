import tkinter as tk
import tkinter.messagebox as msgbox
import io
import sys

class TkOstream(io.IOBase):
    def __init__(self, out):
        self.out = out
        self.q = str()
        self.doflush = False

    def write(self, x):
        assert isinstance(x, str)
        self.q += x
        print(f"Writing {repr(x)}")
        self.out(x)
        return len(x)

    def flush(self):
        self.q = str()
        print("Flushing")

#sout = TkOstream(lambda x:msgbox.showinfo("Test",x))
#sys.stdout = sout
serr = TkOstream(lambda x: msgbox.showerror("Error",x))
originalStdErr = sys.stderr
sys.stderr = serr
