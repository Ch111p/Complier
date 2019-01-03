import string

keyword = {
'int':'kw_int',
'char':'kw_char',
'void':'kw_void',
'if':'kw_if',
'else':'kw_else',
'switch':'kw_switch',
'case':'kw_case',
'default':'kw_default',
'while':'kw_while',
'do':'kw_do',
'for':'kw_for',
'break':'kw_break',
'continue':'kw_continue',
'return':'kw_return'
}

operator = {
'++':'inc',
'--':'dec',
'&&':'and',
'||':'or',
'>=':'ge',
'<=':'le',
'==':'equ',
'!=':'neqe',
'-':'sub',
'*':'mul',
'/':'div',
'%':'mod',
'+':'add',
'!':'not',
'=':'assign',
'>':'gt',
'<':'lt',
}

delimiter = {
',':'comma',
':':'colon',
';':'simcon',
'(':'lparen',
')':'rparen',
'{':'lbrac',
'}':'rbrac'
}

def judgeId(subStr):
    if subStr[0] in string.digits or subStr in keyword:
        return False
    for i in subStr:
        if i not in (string.digits + string.ascii_letters + '_'):
            return False
    return True

def splitOperator(subStr=str):
    if subStr == '':
        return []
    for i in dict(operator, **delimiter):
        if i == subStr or len(set(list(string.ascii_letters + string.digits + subStr + '"' + "'"))) == 64:
            return [subStr]
        else:
            try:
                if i in subStr:
                    return splitOperator(subStr[:subStr.index(i)]) + [i] + splitOperator(subStr[subStr.index(i) + len(i):])
                else:
                    continue
            except TypeError:
                print('invalid operator!')
                return []

def run(code=str):
    result = []
    subList = code.split(' ')
    codeList = []
    for i in subList:
        codeList += splitOperator(i)
    print(codeList)
    for index, i in enumerate(codeList):
        if i in keyword:
            result.append({i:keyword[i]})
        elif i in operator:
            result.append({i:operator[i]})
        elif i in delimiter:
            result.append({i:delimiter[i]})
        else:
            if "'" in i:
                result.append({i:'char'})
            elif '"' in i:
                result.append({i:'str'})
            elif i.isdigit():
                result.append({i:'num'})
            else:
                if(judgeId(i)):
                    result.append({i:'ID'})
                else:
                    print('invalid ID:%d %s'%(index,i))
                
    print(result)

if __name__ == '__main__':
    while(1):
        try: 
            code = input()
            run(code)
        except EOFError:
            break