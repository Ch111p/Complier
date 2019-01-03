from left_recursion import grammer
import itertools
import re

class ll1:
    
    def __init__(self,inputGram=list):
        self.gram = grammer(inputGram).indirectRec()
        self.first = {}
        self.follow = {}
        self.select = {}
        self.goTable = {}
        self.follow[self.gram.start] = set('$')
        self.symbols = [i.split('::')[0] for i in self.gram.grams]
        for i in self.symbols:
            for j in self.gram.end:
                if i in self.goTable:
                    self.goTable[i].update({j:''})
                else:
                    self.goTable.update({i:{j:''}})
        print(self.goTable)
        for i in self.gram.end:
            self.first[i] = set()
            self.first[i].add(i)
        flag = 1
        self.reList = ['(',')','*','+']
        while(flag):
            flag = 0
            for i in self.symbols:
                if i not in self.first.keys():
                    flag = 1
                    self.first[i] = set()
                for j in self.gram.map[i]:
                    if j == '#':
                        self.first[i].add('#')
                        continue
                    listA = re.split('(' + ''.join('\\' + _ + '|' if _ in self.reList else _ + '|' for _ in self.gram.end + self.symbols[::-1])[:-1] + ')',j)
                    while(1):
                        if '' in listA:
                            listA.remove('')
                        else:
                            break
                    for k in listA:
                        if k in self.first.keys():
                            lengthA = len(self.first[i])
                            self.first[i].update(self.first[k] - set('#'))
                            lengthB = len(self.first[i])
                            if lengthA != lengthB:
                                flag = 1
                        else:
                            flag = 1
                        if k in self.gram.end or '#' not in self.gram.map[k]:
                            break
        flag = 1
        while(flag):
            flag = 0
            for i in self.symbols:
                if i not in self.follow.keys():
                    flag = 1
                    self.follow[i] = set()
                for j in self.gram.map[i]:
                    listA = re.split('(' + ''.join('\\' + _ + '|' if _ in self.reList else _ + '|' for _ in self.gram.end + self.symbols[::-1])[:-1] + ')',j)
                    while(1):
                        if '' in listA:
                            listA.remove('')
                        else:
                            break
                    for index, k in enumerate(listA):
                        if k in self.symbols:
                            if k not in self.follow.keys():
                                flag = 1
                                break
                            if index == len(listA) - 1:
                                self.follow[k].update(self.follow[i])
                            for z in listA[index + 1:]:
                                lengthA = len(self.follow[k])
                                self.follow[k].update(self.first[z] - set('#'))
                                if '#' in self.first[z]:
                                    self.follow[k].update(self.follow[i])
                                lengthB = len(self.follow[k])
                                if lengthA != lengthB:
                                    flag = 1
        for i in self.gram.map:
            for j in self.gram.map[i]:
                listA = re.split('(' + ''.join('\\' + _ + '|' if _ in self.reList else _ + '|' for _ in self.gram.end + self.symbols[::-1])[:-1] + ')',j)
                while(1):
                    if '' in listA:
                        listA.remove('')
                    else:
                        break
                if listA[0] == '#':
                    for k in self.follow[i]:
                        self.goTable[i][k] = j
                    continue
                for k in self.first[listA[0]]:
                    if k != '#':
                        self.goTable[i][k] = j

    def analyse(self,Input=str):
        inputList = re.split('(' + ''.join('\\' + _ + '|' if _ in self.reList else _ + '|' for _ in self.gram.end)[:-1] + ')',Input)
        for i in inputList:
            if '' in inputList:
                inputList.remove('')
            else:
                break
        analyseStack = ['$']
        analyseStack.append(self.gram.start)
        top = 1
        while(analyseStack[top] != '$'):
            if analyseStack[top] == '#':
                analyseStack.pop()
                top -= 1
                continue
            if analyseStack[top] == inputList[0]:
                inputList = inputList[1:]
                analyseStack.pop()
                top -= 1
            elif analyseStack[top] in self.gram.end:
                print('error')
                exit()
            elif self.goTable[analyseStack[top]][inputList[0]] != '':
                newStatus = re.split('(' + ''.join('\\' + _ + '|' if _ in self.reList else _ + '|' for _ in self.gram.end + self.symbols[::-1])[:-1] + ')',self.goTable[analyseStack[top]][inputList[0]])[::-1]
                for i in newStatus:
                    if '' in newStatus:
                        newStatus.remove('')
                    else:
                        break
                analyseStack.pop()
                top -= 1
                analyseStack += newStatus
                print(inputList)
                print(analyseStack)
                top += len(newStatus)
            else:
                print('error')
        print('success')
        return

fp = open('grammer.txt')
subList = fp.readlines()
ll = ll1(subList)
print(ll.first)   
print(ll.follow)
print(ll.goTable)
ll.analyse('id+id*id$')