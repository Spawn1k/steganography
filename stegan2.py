import codecs

def space(s, word):
    hide = ''
    new = ''
    for i in range(len(word)):
        hide += bin(ord(word[i])-848)[2::]    
    i = 0
    k = 0
    #2 пробела = 1, 1 пробел = 0
    while k < len(hide):
        if ord(s[i]) == 10 and hide[k] == '1':
            new += '  \n'
            k += 1
        elif ord(s[i]) == 10 and hide[k] == '0':
            new += ' \n'
            k += 1
        elif ord(s[i]) != 13:
            new += s[i]
        i += 1
    new += s[i::]   
    f = codecs.open('output.txt', 'w', 'utf-8')
    f.write(new)
    f.close()        

def decode():
    f = codecs.open('output.txt', 'r', 'utf-8')
    s = f.read()
    f.close()
    code = ''
    answer = ''
    for i in range(len(s)):
        if s[i] == '\n':
            if s[i-1] == ' ':
                if s[i-2] == ' ':
                    code += '1'
                else:
                    code += '0'
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
    space(s, word)
elif opt == '2':
    decode()