
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

    def generate(self):
        i = self.par
        s = self.title
        while i is not None:
            s = f"{i.title}>{s}"
            i = i.par
        return s

    def __repr__(self):
        return f"IndexItem({self.lv}, \"{self.title}\", {self.par}, {self.line})"

class IndexList:
    def __init__(self, passage, name = "Root"):
        self.list = []
        prstList = []
        self.root = IndexItem(0, name, None, -1)
        self.list.append(self.root)
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
        self.len = len(self.list)

    def __getitem__(self, i):
        assert isinstance(i, int), "Invalid argument"
        lt = 0
        rt = self.len
        mid = (lt + rt + 1) >> 1
        while lt < mid:
            if self.list[mid].line > i:
                rt = mid - 1
            elif self.list[mid].line == i:
                return self.list[mid]
            else:
                lt = mid
            mid = (lt + rt + 1) >> 1
        return self.list[mid]

    def generate(self, i):
        return self[i].generate()

    def save(self, file):
        with open(file, "w", encoding = "utf-8") as f:
            for i in self.list: f.write(f"{i.line} {i.lv} {i.title}\n")
        f.close()

    @classmethod
    def load(cls, file):
        inst = cls([])
        inst.list = []
        prstList = []
        f = open(file,encoding = "utf-8")
        line = f.readline()
        while line != '':
            a,b,s = line.split(' ',2)
            a,b = int(a),int(b)
            s = s[:-1]
            if b == 0:
                inst.root = IndexItem(0, s, None, a)
                inst.list.append(inst.root)
                prstList.append(inst.root)
                line = f.readline()
                continue
            else:
                while b <= prstList[-1].lv: prstList.pop()
            newitem = IndexItem(b, s, prstList[-1], a)
            prstList.append(newitem)
            inst.list.append(newitem)
            line = f.readline()
        f.close()
        inst.len = len(inst.list)
        return inst

    def __repr__(self):
        return repr(self.list)
