import codecs
import random

def spec(s, word):
    hide = ''
    new = ''
    for i in range(len(word)):
        hide += bin(ord(word[i])-848)[2::]    
    i = 0
    k = 0
    #longandshort = 1, shortandshort = 0
    while k < len(hide):
        if s[i] == '—' and hide[k] == '1':
            new += '—–'
            k += 1
        elif s[i] == '—' and hide[k] == '0':
            new += '–—'
            k += 1
        elif ord(s[i]) != 13:
            new += s[i]
        i += 1
    new += chr(8195)
    j = i
    for j in range(len(s)):
        if s[j] == '—' and random.getrandbits(1) == 0:
            new += '—–'
        elif s[j] == '—' and random.getrandbits(1) == 1:
            new += '–—'
        else:
            new += s[j]
            
    f = codecs.open('output.txt', 'w', 'utf-8')
    f.write(new)
    f.close()        

def decode():
    f = codecs.open('output.txt', 'r', 'utf-8')
    s = f.read()
    f.close()
    code = ''
    answer = ''
    i = 0
    k = s.find(chr(8195))
    while i < k:
        if s[i] == '—':
            code += '1'
            i += 2
        elif s[i] == '–':
            code += '0'
            i += 2
        else:
            i += 1
    mas = [code[x:x+8] for x in range(0, len(code), 8)]
    for i in mas:
        answer += chr(int(i, 2)+848)
    f = codecs.open('decoded.txt', 'w', 'utf-8')
    f.write(answer)
    f.close()    

f = codecs.open('input.txt', 'r', 'utf-8')
s = f.read()
f.close()
opt = input('Type 1 for encode and 2 for decode: ')
if opt == '1':
    word = input('Input word: ')
    spec(s, word)
elif opt == '2':
    decode()