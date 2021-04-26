#!/usr/bin/env python
# coding: utf-8

# Init the needed display libraries.

# In[1]:


import sympy as sym
from IPython.display import display, Math


# In[2]:


from sympy.abc import x,y,z,a,b,c,d
from sympy import evaluate
from sympy.parsing.sympy_parser import parse_expr


# In[3]:


def showTEX(text):
    text = text.replace("^","**")
    temp = parse_expr(text, evaluate=False)
    display(Math(sym.latex(temp)))


# In[4]:


def isNumber(text):
    try:
        temp = float(text)
        return True
    except ValueError as n:
        return False


# In[5]:


var = ['a', 'b', 'c', 'd', 'x', 'y', 'z']


# In[6]:


def cleanInput(text):
    list=[]
    var = ['a','b','c','d','x','y','z']
    list[:0]=text
    l = 0
    while l < len(list):
        temp = list[l]
        if l==0 or temp=='*':
            l+=1
            continue
        if list[l-1]!='(' and list[l-1]!='-' and list[l-1]!='^' and list[l-1]!='*' and list[l-1]!='/':
            if (temp == '(' or temp == '-' or temp in var) or (isNumber(temp) and not isNumber(list[l-1])):
                list.insert(l, '*')
                l+=2
            else:
                l+=1
        else:
            l+=1
    result = ""
    return result.join(list)
            


# In[7]:


def distribute(base, exponent):
    done = False
    i = 0
    start = 0
    exitflag = False
    while not done:
        if i == len(base) or base[i] == '*' or base[i] == '/':
            if i == len(base):
                exitflag = True
            exp = len(exponent)
            temp = []
            if '^' in base[start:i]:
                list = []
                temp = base[start:i]
                cut = temp.index('^')
                expo = temp[cut + 1:]
                strTemp = ""
                strTemp = strTemp.join(expo)
                flTemp = parse_expr(strTemp)
                strTemp = strTemp.join(exponent)
                flTemp2 = parse_expr(strTemp)
                resTemp = flTemp * flTemp2
                strTemp = '%.2f' % resTemp.evalf()
                list[:0] = strTemp
                temp = temp[:cut + 1] + list
                leng = len(list)
                orleng = len(expo)
                exp += leng - orleng
                base = base[:start] + temp + base[i:]
            else:
                temp.append('^')
                exp += 1
                if '/' in exponent or '*' in exponent:
                    temp.append('(')
                    exp += 1
                for j in exponent:
                    temp.append(j)
                if '/' in exponent or '*' in exponent:
                    temp.append(')')
                    exp += 1
                base[i:i] = temp
            if exitflag:
                done = True
            i += exp + 1
            start = i
        else:
            i += 1

    return base


# In[8]:


def computeExponents(text):
    list = []
    list[:0] = text
    done = False
    compute = False
    i = 0
    temp = ""
    result = ""
    while not done:
        if i == len(list) - 1:
            done = True
        if compute:
            if list[i] == ")":
                fl = parse_expr(temp)
                temp = '%.2f' % fl.evalf()
                result += temp
                temp = ""
                compute = False
            else:
                temp += list[i]
        else:
            if list[i] == "^" and i + 1 < len(list):
                result += list[i]
                if list[i + 1] == "(":
                    compute = True
                    i += 1
            else:
                if not compute:
                    result += list[i]
        i += 1
    return result


# In[9]:


def replaceOperations(list):
    list = ['@' if x == '*' else x for x in list]
    list = ['*' if x == '/' else x for x in list]
    list = ['/' if x == '@' else x for x in list]
    return list


# In[10]:


def cleanP(text):
    openers = []
    result = ""
    list = []
    list[:0] = text
    curr = 0
    while curr < len(list):
        if list[curr] == '(':
            openers.append(curr)
        elif list[curr] == ')':
            i = 1
            appendable = []
            # conseguir base y ver si es numerico
            numeric = True
            base = list[openers[-1] + 1:curr]
            baseStr = ""
            baseStr = baseStr.join(base)
            if any(item in base for item in var):
                numeric = False
            else:
                temp = parse_expr(baseStr)
                baseStr = '%.2f' % temp.evalf()
                base.clear()
                base[:0] = baseStr
            # ver si hay potencia
            if curr != len(list) - 1 and list[curr + 1] == '^':
                # si hay potencia conseguir exponente y ver si es simple o fraccion
                exponent = ""
                i = 2
                done = False
                while not done:
                    if not curr + i >= len(list) and (
                            isNumber(list[curr + i]) or list[curr + i] == '-' or list[curr + i] == '/'):
                        exponent = exponent + list[curr + i]
                        i += 1
                    else:
                        done = True
                        temp = parse_expr(exponent)
                        exponent = '%.2f' % temp.evalf()
                # si es simple hacer la multiplicacion de base exc
                if numeric:
                    try:
                        exp = float(exponent)
                        result = '%.2f' % temp ** exp
                    except ValueError as n:
                        print("exponent not numeric")
                        result = 0

                else:
                    expo = []
                    expo.append(exponent)
                    result = distribute(list[openers[-1] + 1:curr], expo)
            elif curr != len(list) - 1 and list[curr + 1] == '/':
                # replace all the * yo / and / to *
                reptemp = list[curr+2:]
                reptemp = replaceOperations(reptemp)
                list[curr+2:] = reptemp
                result = baseStr
            else:
                result = baseStr
            # eliminar expresion anterior empezando de ( a )
            del list[openers[-1]:curr + i]
            # devolver el cursor al principio de (
            if len(openers) != 0:
                curr = openers.pop(-1)
            # agregar el resultado y adelantar el cursor al final del resultado
            res = []
            res[:0] = result
            leng = len(res)-1
            list[curr:curr] = res
            curr += leng
        curr += 1
    return list


# In[11]:


def exponent(curr):
    temp = parse_expr(curr[0])
    temp2 = parse_expr(curr[1])
    mult = temp ** temp2
    curr[0] = '%.2f' % mult.evalf()
    curr[1] = "1"
    return curr


# In[12]:


def factor(text):
    factors = []
    i = 0
    curr = ["", "1", '*']
    for element in text:
        if element == '^':
            i = 1
            curr[1] = ""
        elif element == '*' or element == '/':
            i = 0
            if isNumber(curr[0]):
                curr = exponent(curr)
            if curr[1] == "":
                curr[1] = "1"
            factors.append(curr)
            curr = ["", "1", element]
        else:
            curr[i] += str(element)
    if isNumber(curr[0]):
        curr = exponent(curr)
    if curr[1] == "":
        curr[1] = "1"
    factors.append(curr)
    return factors


# In[13]:


def show(factors):
    final = ""
    for i in factors:
        final += i[0]+"^"+i[1]+i[2]

    final = final[:-1]
    showTEX(final)


# In[14]:


def search(factors, element):
    i = 0
    for x in factors:
        if x[0] == element or '-'+x[0] == element or x[0] == '-'+element:
            return i
        elif isNumber(x[0]) and isNumber(element):
            return i
        i+=1
    return -1


# In[15]:


def simplify(text):
    print("Parte 1 (Calcular exponentes)")
    text = computeExponents(text)
    showTEX(text)
    list = cleanP(text)
    print("Parte 2 (Eliminar parentesis)")
    temp = ""
    temp = temp.join(list)
    showTEX(temp)
    factors = factor(list)
    result = []
    print("Parte 3 (Pasar factores)")
    for f in factors:
        i = search(result, f[0])
        if i != -1:
            curr = result[i]
            if isNumber(curr[0]):
                temp1 = float(curr[0])
                temp2 = float(f[0])
                if f[2] == "*":
                    temp1 *= temp2
                else:
                    temp1 /= temp2
                curr[0] = '%.2f' % temp1
            else:
                neg1 = '-' in curr[0]
                neg2 = '-' in f[0]
                if neg1 and neg2:
                    curr[0] = curr[0].replace("-","")
                elif neg2:
                    curr[0] = '-' + curr[0]
                    
                temp1 = float(curr[1])
                temp2 = float(f[1])
                if f[2] == "*":
                    temp1 += temp2
                else:
                    temp1 -= temp2
                curr[1] = '%.2f' % temp1
            result[i] = curr
        else:
            result.append(f)
        show(result)
    print("Resultado")
    show(result)


# In[16]:


print("Solo utilizar las variables x,y,z,a,b,c,d")
userInput = input("Ingrese la expression de modo a^2*5*(4*b)^4:" )
res = cleanInput(userInput)
print("Ingresaste:")
showTEX(res)
simplify(res)

