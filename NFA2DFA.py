import string
import itertools

class DFA:

    def __init__(self,graph=list):
        self.changeTable = {}
        self.accList = []
        self.num = int(graph[0])
        self.startSta = '0'
        subDict = {}
        num = 0
        for i in graph[1:-1]:
            subList = i.split()
            if subList[0] not in subDict:
                subDict[subList[0]] = str(num)
                num += 1
            if subList[2] not in subDict:
                subDict[subList[2]] = str(num)
                num += 1
        for value in graph[1:-1]:
            subList = value.split()
            if subDict[subList[0]] not in self.changeTable:
                self.changeTable[subDict[subList[0]]] = {}
            if subDict[subList[2]] not in self.changeTable:
                self.changeTable[subDict[subList[2]]] = {}
            if subList[1] in self.changeTable[subDict[subList[0]]] and subDict[subList[2]] not in self.changeTable[subDict[subList[0]]][subList[1]]:
                self.changeTable[subDict[subList[0]]][subList[1]].append(subDict[subList[2]])
            else:
                self.changeTable[subDict[subList[0]]].update({subList[1]:[subDict[subList[2]]]})
        for i in graph[-1].split(' '):
            self.accList.append(subDict[i])

    def judgeDorN(self):
        for i in self.changeTable:
            for j in self.changeTable[i]:
                if len(self.changeTable[i][j]) > 1:
                    return False
        return True

    def closure(self, situation=set):
        eSet = situation.copy()
        for i in situation:
            for index, value in enumerate(self.changeTable[i]):
                if '-1' in value:
                    for k in self.changeTable[i]['-1']:
                        eSet.update(self.closure(set(k)))
        return eSet

    def move(self, states=list, situation=str):
        mSet = []
        for i in states:
            for index, value in enumerate(self.changeTable[i]):
                if situation in value:
                    mSet += self.changeTable[i][value]
        subSet = set()
        for i in mSet:
            subSet.add(i)
        return subSet

    def changeNtoD(self):
        if(self.judgeDorN()):
            return self
        else:
            initTable = []
            Dstates = list(self.closure(set(self.startSta)))
            Dstates.sort(key=lambda d:int(d))
            subKey = ''.join(i + '|' for i in Dstates)[:-1]
            Dstates.clear()
            Dstates.append(subKey)
            subList = []
            end = []
            for i in Dstates:
                inputSet = []
                movList = i.split('|')
                for j in movList:
                    inputSet += self.changeTable[j].keys()
                inputSet = set(inputSet)
                print(inputSet)
                for j in inputSet:
                    subKey = ''
                    subList = list(self.closure(self.move(movList,j)))  
                    subList.sort(key=lambda d:int(d))
                    for k in subList:
                        subKey += k + '|'
                    subKey = subKey[:-1]
                    for k in self.accList:
                        if k in subKey:
                            end.append(subKey)
                    if subKey not in Dstates:
                        for index, k in enumerate(Dstates):
                            if set(subKey.split('|')).issubset(set(k.split('|'))):
                                initTable.append(k + ' ' + j + ' ' + k)
                                break
                            if index == (len(Dstates) - 1):
                                Dstates.append(subKey)
                                initTable.append(i + ' ' + j + ' ' + subKey)
                                break
                    else:
                        initTable.append(i + ' ' + j + ' ' + subKey)
            initTable.insert(0,str(len(Dstates)))
            end = set(end)
            initTable += end
            print(initTable)
        return DFA(initTable)
    
    def minDFA(self):
        initTable = []
        subList = [self.accList,[i for i in (set(self.changeTable.keys()) - set(self.accList))]]
        subSets = []
        lengthA = len(subSets)
        while(1):
            subDict = {}
            for index, i in enumerate(subList):
                for j in i:
                    subDict[j] = index
            for i in subList:
                if(len(i) > 1):
                    for j in itertools.combinations(i,2):
                        eflag = 0
                        if len(self.changeTable[j[0]].keys() - self.changeTable[j[1]].keys()) != 0:
                            eflag = 1
                        else:
                            for index, k in enumerate(self.changeTable[j[0]]):
                                if subDict[self.changeTable[j[0]][k][0]] != subDict[self.changeTable[j[1]][k][0]]:
                                    eflag = 1
                                    break
                                if index == len(self.changeTable[j[0]]) - 1:
                                    if len(subSets) == 0:
                                        subSets.append(set([j[0],j[1]]))
                                    else:
                                        for index1, k in enumerate(subSets):
                                            if j[0] in k:
                                                subSets[index1].add(j[1])
                                                break
                                            elif j[1] in k:
                                                subSets[index1].add(j[0])
                                                break
                                            if index1 == len(subSets) - 1:
                                                subSets.append(set([j[0],j[1]]))
                        if eflag:
                            flag = 0
                            for index, e in enumerate(subSets):
                                if j[0] in e:
                                    flag |= 1
                                    subSets[index].add(j[0])
                                elif j[1] in e:
                                    flag |= 0b10
                                    subSets[index].add(j[1])
                            if flag == 0:
                                subSets.append(set(j[0]))
                                subSets.append(set(j[1]))
                            elif flag == 1:
                                subSets.append(set(j[1]))
                            elif flag == 2:
                                subSets.append(set(j[0]))
                            continue
                else:
                    subSets.append(set(i[0]))
            lengthB = len(subSets)
            if lengthB == lengthA:
                break
            lengthA = lengthB
            subList.clear()
            for i in subSets:
                subList.append(list(i))
            subSets.clear()

        accAddr = {}
        
        for index, i in enumerate(subSets):
            for j in i:
                accAddr[j] = index
        for index, i in enumerate(subSets):
            if self.startSta in i:
                subChar = str(i.pop())
                for index, j in enumerate(self.changeTable[self.startSta]):
                    initTable.insert(index,str(accAddr[subChar]) + ' ' + j + ' ' + str(accAddr[self.changeTable[self.startSta][j][0]]))
            else:
                subChar = str(i.pop())
                for j in self.changeTable[subChar]:
                    initTable.append(str(accAddr[subChar]) + ' ' + j + ' ' + str(accAddr[self.changeTable[subChar][j][0]]))
        accSet = set()
        for i in accAddr:
            if i in self.accList:
                accSet.add(accAddr[i])
        accStr = ''.join(str(i) + ' ' for i in accSet)[:-1]
        initTable.append(accStr)
        initTable.insert(0,str(len(subSets)))
        return DFA(initTable)


fp = open('graph.txt','r')
listA = fp.readlines()
for index, value in enumerate(listA):
    listA[index] = listA[index].strip()
a = DFA(listA)
print(a.changeTable)
b = a.changeNtoD()
print(b.changeTable)
print(b.minDFA().changeTable)