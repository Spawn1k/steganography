import codecs

def symchange(s, word):
    hide = ''
    new = ''
    k = 0
    for i in range(len(word)):
        hide += bin(ord(word[i])-848)[2::]
    #русская о = 1, русская р = 0
    i = 0
    while k < len(hide):
        if s[i] == 'о' and hide[k] == '1':
            new += 'o'
            k += 1
        elif s[i] == 'р' and hide[k] == '0':
            new += 'p'
            k += 1
        else:
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
        if s[i] == 'o':
            code += '1'
        if s[i] == 'p':
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
    symchange(s, word)
elif opt == '2':
    decode()