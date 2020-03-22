import json
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.constants import END, LEFT, RIGHT, X, Y, TOP, W
from urllib import parse, request
import indexsys as index

def translateGoogle(s, fr, to):
    query = s.strip('\n')
    data = parse.urlencode({
        'dt'    : 't',
        'client': 'gtx',
        'sl'    : fr,
        'tl'    : to,
        'dj'    : '1',
        'ie'    : 'utf-8',
        'q'     : query
    })
    URL = 'https://translate.googleapis.com/translate_a/single?' + data
    res = request.urlopen(URL)
    js = json.load(res)
    sentences = js['sentences']
    ret = ''.join(i['trans'] for i in sentences)
    return ret

translate = translateGoogle
class App:
    '''The application'''
    __name = "PyTransHelper"
    def __init__(self, file):
        self.loadset(file)
        self._initUI()
        self._initLt()
        self._initRt()
        self._initBar()
        self._ButtonDictInit()
        self._ButtonPlace()

    def _initUI(self):
        self.ui = tk.Tk()
        self.ui.title("PyTransHelper")
        self.ui.geometry(f"{self.scrset['w']}x{self.scrset['h']}")
        self.ui.resizable(False,False)

    def _initBar(self):
        self.bar = tk.Label(
            self.ui, justify = LEFT,
            anchor = W,
            font = self.setting["barfont"]
        )
        self.bar.pack(side = TOP, fill = X)

    def _initLt(self):
        self.lable1 = tk.Label(self.ui, text = "Source")
        self.lable1.place(x = 0, y = 0, height = self.scrset['ptop'], width = self.scrset['w']/2)
        self._frbar = tk.Scrollbar(self.ui)
        self._frbar.pack(side = LEFT, fill = Y)
        self.fr = tk.Text(
            self.ui, bg = self.setting['i']['bgcol'], bd = 5,
            font = self.setting['i']['font'],
            fg = self.setting['i']['txtcol'],
            yscrollcommand = self._frbar.set
        )
        self._frbar.config(command = self.fr.yview)
        self.fr.place(
            x = self.scrset['pside'],
            y = self.scrset['ptop'],
            height = self.scrset['txth'],
            width = self.txtwid
        )

    def _initRt(self):
        self.lable2 = tk.Label(self.ui, text = "Result")
        self.lable2.place(x = self.scrset['w']/2, y = 0, height = self.scrset['ptop'], width = self.scrset['w']/2)
        self._tobar = tk.Scrollbar(self.ui)
        self._tobar.pack(side = RIGHT, fill = Y)
        self.to = tk.Text(
            self.ui, bg = self.setting['o']['bgcol'], bd = 5,
            font = self.setting['o']['font'],
            fg = self.setting['o']['txtcol'],
            yscrollcommand = self._tobar.set
        )
        self._tobar.config(command = self.to.yview)
        self.to.place(
            x = self.scrset['pside'] + self.scrset['pmid'] + self.txtwid,
            y = self.scrset['ptop'],
            height = self.scrset['txth'],
            width = self.txtwid
        )

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
            'a' : self.crBt("AutoTrans", self.trans),
            'c' : self.crBt("Copy", self.copy),
            'j' : self.crBt("Jump", self.jump)
        }

    def crBt(self, text, command):
        return tk.Button(
            self.ui, bd = 8, text = text,
            font = self.setting['buttonfont'],
            command = command
        )

    def _ButtonPlace(self):
        j = self.scrset['pside']
        h = self.scrset['buttonY']
        for i in self.setting['buttons']:
            try:
                (b:=self.buttons[i["id"]]).place(
                    x = j,
                    y = h,
                    height = self.scrset['buttonH'],
                    width = self.btnwid
                )
                j += self.btnwid + self.scrset['pmid']
                if j >= self.scrset['w'] - self.scrset['pside']:
                    if h + self.scrset['buttonH'] > self.scrset['h']:
                        msgbox.showwarning(self.__name, "The button may be out of the UI")
                    j = self.scrset['pside']
                    h += self.scrset['pbtn'] + self.scrset['buttonH']
                if i["key"] != "":
                    self.ui.bind(i["key"], b['command'])
            except KeyError as e:
                msgbox.showerror(self.__name, f"KeyError raised: {e}, maybe you wrote an invalid button id in settings.json")
            except Exception as e:
                msgbox.showerror(self.__name, f"Unknown Exception raised when placing the buttons: {e}")

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
        self.it = -1
        self.index = index.IndexList(self.lfr)
        self.index.save(self.setting["indexfile"])

    def require4str(self, title, prompt):
        tmp = tk.Tk()
        tmp.geometry("300x300")
        tmp.resizable(False,False)
        tlable = tk.Label(tmp, text = prompt)
        tlable.pack()
        retvar = tk.StringVar(tmp)
        tentry = tk.Entry(tmp, textvariable = retvar)
        tentry.pack()
        def f4btn():
            tmp.quit()
            tmp.destroy()
        tmpbtn = tk.Button(tmp, text = "Confirm", command = f4btn)
        tmpbtn.pack()
        tmp.mainloop()
        return retvar.get()

    def require4int(self, title, prompt):
        s = self.require4str(title, prompt)
        try:
            return int(s)
        except ValueError:
            msgbox.showerror("You are not inputing an integer!")
            return -1

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
            msgbox.showerror(self.__name, f"unknown Exception raised: {e}")
            return -1
        self.fr.delete('1.0', END)
        f.close()
        self.lfr = self.text.split('\n')
        self.lto = tr.split('\n')
        self.end = len(self.lfr)
        self.it = -1
        try:
            self.index = index.IndexList.load(self.setting["indexfile"])
        except FileNotFoundError:
            msgbox.showerror(self.__name, "Index file missing!")

    def loadset(self, file):
        try:
            with open(file) as f:
                self.setting = json.load(f)
                f.close()
            self.scrset = self.setting['screen']
            rawwid = self.scrset['w'] - 2*self.scrset['pside']
            self.txtwid = (rawwid - self.scrset['pmid'])/2
            self.btnwid = (rawwid + self.scrset['pmid'])/self.scrset['buttonpline'] - self.scrset['pmid']
        except FileNotFoundError as e:
            msgbox.showerror(self.__name, "Settings.json Missing!")
        except Exception as e:
            msgbox.showerror(self.__name, f"Unknown Exception raised when loading the settings: {e}")

    def copy(self):
        self.to.delete('1.0',END)
        self.to.insert(END, self.fr.get('1.0',END))

    def moveto(self, index, save = True):
        try:
            if index >= self.end:
                msgbox.showerror(self.__name, "That's the end of your passage!")
                return -1
            elif index < 0:
                msgbox.showerror(self.__name, "That's the begining of your passage!")
                return -1
        except AttributeError:
            msgbox.showerror(self.__name, "Init or load first!")
            return -1
        self.fr.delete('1.0',END)
        self.fr.insert(END, self.lfr[index])
        if save and self.it >= 0:
            self.lto[self.it] = self.to.get('1.0', END).rstrip('\n ')
        self.to.delete('1.0', END)
        self.to.insert(END, self.lto[index])
        self.it = index
        self.bar["text"] = f"{self.it} | {self.index.generate(self.it)}"

    def jump(self, save = True):
        i = self.require4int(self.__name, "Input the line that\nyou want to jump to")
        if i < 0 or i >= self.end:
            msgbox.showerror(self.__name, "Index out of range!")
            return -1
        self.moveto(i)

    def next(self, save = True):
        self.moveto(self.it + 1, save)

    def prev(self, save = True):
        self.moveto(self.it - 1, save)

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
            self.to.insert(END, translate(
                self.fr.get('1.0', END),
                self.setting['i']['lan'],
                self.setting['o']['lan']
            ))
        except Exception as e:
            msgbox.showerror(self.__name, f'Invalid Translation: {e}')

if __name__ == '__main__':
    app = App('./settings.json')    
    tk.mainloop()
