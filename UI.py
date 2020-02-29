import tkinter as tk
from tkinter.constants import *
from urllib import request, parse
import json

def translateGoogle(s, fr, to):
    try:
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
    except Exception as e:
        return repr(e)

translate = translateGoogle
class App:
    '''The application'''
    def __init__(self, file):
        self.loadset(file)
        self.ui = tk.Tk()
        self.ui.geometry("1220x700+300+200")
        self.ui.resizable(False,False)
        self.lable1 = tk.Label(self.ui, text = "Input")
        self.lable1.place(x = 20, y = 20, height = 40, width = 580)
        self.fr = tk.Text(self.ui, bg = self.setting['i']['bgcol'], bd = 5,
                          font = self.setting['i']['font'],
                          fg = self.setting['i']['txtcol'])
        self.fr.place(x = 20, y = 70, height = 500,width = 580)
        self.lable2 = tk.Label(self.ui, text = "Output")
        self.lable2.place(x = 620, y = 20, height = 40, width = 580)
        self.to = tk.Text(self.ui, bg = self.setting['o']['bgcol'], bd = 5,
                          font = self.setting['o']['font'],
                          fg = self.setting['o']['txtcol'])
        self.to.place(x = 620, y = 70, height = 500, width = 580)
        self.buttons = {
            'l' : self.crBt("Load", self.initFromFile),
            'i' : self.crBt("Init", self.init_text),
            'n' : self.crBt("Next", self.next),
            'p' : self.crBt("Prev", self.prev),
            'n-': self.crBt("SkipFd", lambda: self.next(False)),
            'p-': self.crBt("SkipBd", lambda: self.prev(False)),
            's' : self.crBt("Save", self.save),
            'e' : self.crBt("Exec", lambda: exec(self.to.get('1.0', END))),
            'a' : self.crBt("Auto\nTrans", self.trans),
            'c' : self.crBt("Copy", self.copy)
        }
        j = 20
        for i in self.setting['buttonAndKey']:
            try:
                (b:=self.buttons[i]).place(x = j, y = 600, height = 70,width = 100)
                j += 120
                if (e:=self.setting['buttonAndKey'][i]) != "":
                    self.ui.bind(e, b['command'])
            except KeyError:
                pass

    def crBt(self, text, command):
        return tk.Button(self.ui, bd = 8, text = text,
                         font = self.setting['buttonfont'],
                         command = command)

    def init_text(self):
        self.text = self.fr.get('1.0', END)
        with open(self.setting['i']['file'], mode = 'w', encoding = "utf-8") as f:
            f.write(self.text)
        self.fr.delete('1.0', END)
        f.close()
        self.lfr = self.text.split('\n')
        self.lto = ['' for i in self.lfr]
        with open(self.setting['o']['file'], mode = 'w', encoding = "utf-8") as f:
            f.write('\n'.join(self.lto))
        f.close()
        self.end = len(self.lfr)
        self.it = 0

    def initFromFile(self, file = None, filetr = None):
        if file is None:    file = self.setting['i']['file']
        if filetr is None:filetr = self.setting['o']['file']
        try:
            with open(file, encoding = "utf-8") as f:
                self.text = f.read()
            with open(filetr, encoding = "utf-8") as fout:
                tr = fout.read()
        except Exception as e:
            self.to.delete('1.0',END)
            self.to.insert(END, str(e))
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
                self.fr.insert(END, "THAT'S THE END OF UR PASSAGE")
                return -1
        except AttributeError:
            self.fr.insert(END, "INIT or LOAD FIRST!!!")
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
                self.fr.insert(END, "THAT'S THE BEGINNING OF UR PASSAGE")
                return -1
        except AttributeError:
            self.fr.insert(END, "INIT or LOAD FIRST!!!")
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
        with open(name, mode = 'w', encoding = "utf-8") as f:
            f.write('\n'.join(self.lto))
        f.close()
        print("File Saved")

    def trans(self):
        try:
            self.to.insert(END, translate(self.fr.get('1.0', END),
                                          self.setting['i']['lan'],
                                          self.setting['o']['lan']))
        except Exception as e:
            self.to.insert(END, f'Invalid Translation {e}')
        
if __name__ == '__main__':
    app = App('./settings.json')    
    tk.mainloop()
    pass
