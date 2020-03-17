import json
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.constants import END, LEFT, RIGHT, X, Y
from urllib import parse, request

def translateGoogle(s, fr, to):
    query = s.strip('\n')
    data = parse.urlencode({
        'dt'    : 't'  ,
        'client': 'gtx',
        'sl'    : fr,
        'tl'    : to,
        'dj'    : '1',
        'ie'    : 'utf-8',
        'q'     : query
    })
    URL = 'https://translate.googleapis.com/translate_a/single?' + data
    res = request.urlopen(URL)
    return json.load(res)['sentences'][0]['trans']

translate = translateGoogle
class App:
    '''The application'''
    __name = "PyTransHelper"
    def __init__(self, file):
        self.loadset(file)
        self._initUI()
        self._initLt()
        self._initRt()
        self._ButtonDictInit()
        self._ButtonPlace()

    def _initUI(self):
        self.ui = tk.Tk()
        self.ui.title("PyTransHelper")
        self.ui.geometry("1220x700")
        self.ui.resizable(False,False)

    def _initLt(self):
        self.lable1 = tk.Label(self.ui, text = "Input")
        self.lable1.place(x = 20, y = 20, height = 40, width = 580)
        self._frbar = tk.Scrollbar(self.ui)
        self._frbar.pack(side = LEFT, fill = Y)
        self.fr = tk.Text(self.ui, bg = self.setting['i']['bgcol'], bd = 5,
                          font = self.setting['i']['font'],
                          fg = self.setting['i']['txtcol'],
                          yscrollcommand = self._frbar.set)
        self._frbar.config(command = self.fr.yview)
        self.fr.place(x = 20, y = 70, height = 500,width = 580)

    def _initRt(self):
        self.lable2 = tk.Label(self.ui, text = "Output")
        self.lable2.place(x = 620, y = 20, height = 40, width = 580)
        self._tobar = tk.Scrollbar(self.ui)
        self._tobar.pack(side = RIGHT, fill = Y)
        self.to = tk.Text(self.ui, bg = self.setting['o']['bgcol'], bd = 5,
                          font = self.setting['o']['font'],
                          fg = self.setting['o']['txtcol'],
                          yscrollcommand = self._tobar.set)
        self._tobar.config(command = self.to.yview)
        self.to.place(x = 620, y = 70, height = 500, width = 580)

    def _ButtonDictInit(self):
        self.buttons = {
            'l' : self.crBt("Load", self.loadFromFile),
            'i' : self.crBt("Init", self.initFromInput),
            'n' : self.crBt("Next", self.next),
            'p' : self.crBt("Prev", self.prev),
            'n-': self.crBt("SkipFd", lambda: self.next(False)),
            'p-': self.crBt("SkipBd", lambda: self.prev(False)),
            's' : self.crBt("Save", self.save),
            'e' : self.crBt("Exec", lambda: exec(self.to.get('1.0', END))),
            'a' : self.crBt("Auto\nTrans", self.trans),
            'c' : self.crBt("Copy", self.copy)
        }

    def crBt(self, text, command):
        return tk.Button(self.ui, bd = 8, text = text,
                         font = self.setting['buttonfont'],
                         command = command)

    def _ButtonPlace(self):
        j = 20
        for i in self.setting['buttons']:
            try:
                (b:=self.buttons[i["id"]]).place(x = j, y = 600, height = 70,width = 100)
                j += 120
                if i["key"] != "":
                    self.ui.bind(i["key"], b['command'])
            except KeyError:
                pass

    def initFromInput(self):
        self.text = self.fr.get('1.0', END)
        self.init_text()
        self.fr.delete('1.0', END)

    def init_text(self):
        with open(self.setting['i']['file'], mode = 'w', encoding = "utf-8") as f:
            f.write(self.text)
        f.close()
        self.lfr = self.text.split('\n')
        self.lto = ['' for i in self.lfr]
        with open(self.setting['o']['file'], mode = 'w', encoding = "utf-8") as f:
            f.write('\n'.join(self.lto))
        f.close()
        self.end = len(self.lfr)
        self.it = 0

    def loadFromFile(self, file = None, filetr = None):
        if file   is None:file   = self.setting['i']['file']
        if filetr is None:filetr = self.setting['o']['file']
        try:
            with open(file, encoding = "utf-8") as f:
                self.text = f.read()
            with open(filetr, encoding = "utf-8") as fout:
                tr = fout.read()
        except FileNotFoundError:
            msgbox.showerror(self.__name, "Input and/or output file missing!")
            return -1
        except Exception as e:
            msgbox.showerror(self.__name, f"unknown error raised {repr(e)}")
            return -1
        self.fr.delete('1.0', END)
        f.close()
        self.lfr = self.text.split('\n')
        self.lto = tr.split('\n')
        self.end = len(self.lfr)
        self.it = 0

    def loadset(self, file):
        try:
            with open(file) as f:
                self.setting = json.load(f)
                f.close()
        except Exception as e:
            raise e

    def copy(self):
        self.to.delete('1.0',END)
        self.to.insert(END, self.fr.get('1.0',END))

    def next(self, save = True):
        try:
            if self.it == self.end:
                msgbox.showerror(self.__name, "THAT'S THE END OF UR PASSAGE")
                return -1
        except AttributeError:
            msgbox.showerror(self.__name, "INIT or LOAD FIRST!!!")
            return -1
        self.fr.delete('1.0', END)
        self.fr.insert(END, self.lfr[self.it])
        if save and self.it:
            self.lto[self.it - 1] = self.to.get('1.0', END).rstrip('\n ')
        self.to.delete('1.0', END)
        self.to.insert(END, self.lto[self.it])
        self.it += 1

    def prev(self, save = True):
        try:
            if self.it < 2:
                msgbox.showerror(self.__name, "THAT'S THE BEGINNING OF UR PASSAGE")
                return -1
        except AttributeError:
            msgbox.showerror(self.__name, "INIT or LOAD FIRST!!!")
            return -1
        self.it -= 1
        self.fr.delete('1.0', END)
        self.fr.insert(END, self.lfr[self.it - 1])
        if save:
            self.lto[self.it] = self.to.get('1.0', END).rstrip('\n ')
        self.to.delete('1.0', END)
        self.to.insert(END, self.lto[self.it - 1])

    def save(self, name = None):
        if name is None: name = self.setting['o']['file']
        if self.it and self.it < self.end:
            self.lto[self.it - 1] = self.to.get('1.0', END).rstrip('\n ')
        with open(name, mode = 'w', encoding = "utf-8") as f:
            f.write('\n'.join(self.lto))
        f.close()
        msgbox.showinfo(self.__name, "File Saved")

    def trans(self):
        try:
            self.to.insert(END, translate(self.fr.get('1.0', END),
                                          self.setting['i']['lan'],
                                          self.setting['o']['lan']))
        except Exception as e:
            msgbox.showerror(self.__name, f'Invalid Translation {e}')
        
if __name__ == '__main__':
    app = App('./settings.json')    
    tk.mainloop()
    del X
