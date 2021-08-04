import io
import json
import os
import tkinter as tk
import tkinter.messagebox as msgbox

import index


class Project:
    '''A class to hold a translating project'''

    def __init__(self, source, result, idx):
        self.source = source
        self.result = result
        self.index = idx

    @classmethod
    def load(cls, prjfile):
        f = open(prjfile)
        d = json.load(f)
        root = os.path.split(prjfile)[0]
        inst = cls(d["source"], d["result"], index.IndexList.load(d["index"]))
        return inst

    @classmethod
    def new(cls):
        pass
