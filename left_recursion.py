import string
import re

class grammer:

    def __init__(self,gram=list):
        self.end = ['id','*','+','(',')','$']
        self.grams = gram[:]
        self.start = gram[0].split('::')[0][0]
        self.map = {}
        self.input = ''
        for i in gram:
            subList = i.strip().split('::')
            purposeList = subList[1].split('|')
            if subList[0] in self.map.keys():
                self.map[subList[0]] += purposeList
            else:
                self.map[subList[0]] = purposeList
    
    def hasDircRec(self,key):
        for i in self.map[key]:
            if key in i and i.index(key) == 0:
                return True
        return False

    def getListStr(self,left,listA):
        return left + '::' + ''.join(_ + "|" for _ in listA)[:-1]

    def directRec(self,subList):
        if type(subList) == list:
            subGram = grammer(subList)
        else:
            for i in self.grams:
                if subList in i and i.index(subList) == 0:
                    subGram = grammer([i])
                    break
        subKey = set(subGram.map.keys()).pop()
        initTable = []
        left = []
        if subGram.hasDircRec(subKey):
            for i in subGram.map[subKey]:
                if subKey in i and i.index(subKey) == 0:
                    left.append(i)
            right = list(set(subGram.map[subKey]) - set(left))
            initTable.append(subKey + "::" + ''.join(_ + subKey + "'|" for _ in right)[:-1])
            initTable.append(subKey + "'::" + ''.join(_.strip(subKey) + subKey + "'|" for _ in left)[:-1] + '|#')
        else:
            initTable.append(subGram.getListStr(subKey,subGram.map[subKey]))
        return initTable
    
    def indirectRec(self):
        initTable = []
        Unstoped = [i.split('::')[0] for i in self.grams]
        for indexI, i in enumerate(Unstoped):
            subTable = []
            for indexJ, j in enumerate(Unstoped[:indexI]):
                subList = []
                for k in self.map[i]:
                    if j in k and k.index(j) == 0:
                        for z in self.map[j]:
                            subList.append(k.replace(j,z))
                        subTable.append(self.getListStr(i,subList))
                    else:
                        subList.append(k)
            if len(subTable) > 0:
                initTable += self.directRec(subTable)
            else:
                initTable += self.directRec(i)
        return grammer(initTable)

    def judgeGram(self,rawInput=str,status=None):
        if status == None:
            status = self.start
        if status == '#':
            return rawInput
        reList = ['(',')','*','+']
        for i in self.map[status]:
            subStr = rawInput
            keys = list(self.map.keys())
            listA = re.split('(' + ''.join('\\' + _ + '|' if _ in reList else _ + '|' for _ in self.end + keys[::-1])[:-1] + ')',i)
            while(1):
                if '' in listA:
                    listA.remove('')
                else:
                    break
            for index, j in enumerate(listA):
                print(i,j,rawInput)
                if j in self.end:
                    if rawInput[0] == j:
                        if len(rawInput) == 1:
                            if index == len(listA) - 1:
                                print('success')
                                return
                            else:
                                rawInput = subStr                             
                                break
                        else:
                            rawInput = rawInput[1:]
                    else:
                        rawInput = subStr
                        break
                else:
                    rawInput = self.judgeGram(rawInput,j)
        if status == self.start:
            print('Failed')
        return rawInput

if __name__ == '__main__':               
    fp = open('grammer.txt')
    listA = fp.readlines()
    print(listA)
    Gram = grammer(listA)
    print(Gram.map)
    b = Gram.indirectRec()
    print(b.map)
    print(b.grams)
    b.judgeGram('id+id*id')