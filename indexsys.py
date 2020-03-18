
class IndexItem:
    def __init__(self, level, title, par, line):
        self.lv = level
        self.title = title
        self.children = []
        self.chcnt = 0
        self.par = par
        if self.par:
            self.par.children.append(self)
            self.par.chcnt += 1
            self.id = self.par.chcnt
        else: self.id = -1
        self.line = line

    def __repr__(self):
        return f"{self.title}\n{self.children}\n"

class IndexList:
    def __init__(self, passage):
        self.list = []
        prstList = []
        self.root = IndexItem(0, "Root", None, -1)
        prstList.append(self.root)
        for it in range(len(passage)):
            i = passage[it]
            cnt = 0
            halflen = len(i)
            while cnt < halflen:
                if i[cnt] != '=' or i[~cnt] != '=':
                    break
                cnt += 1
            if not cnt:
                continue
            while prstList[-1].lv >= cnt:
                prstList.pop()
            newitem = IndexItem(cnt, i[cnt:-cnt], prstList[-1], it)
            self.list.append(newitem)
            prstList.append(newitem)

    def __repr__(self):
        return repr(self.root)
