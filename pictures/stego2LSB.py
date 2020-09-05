from PIL import Image, ImageDraw

def change_pix(color, num):
    if num == '0':
        if color % 2 == 0:
            return color
        else:
            return color-1
    if num == '1':
        if color % 2 == 1:
            return color
        else:
            return color+1
    #return color #debug

def encode(word):
    hide = ''
    for i in range(len(word)):
        if word[i] == ' ':
            hide += '00100000'
        else:
            hide += bin(ord(word[i])-848)[2::]
    #print(len(hide)) #debug
    image = Image.open('read_bmp.bmp') 
    draw = ImageDraw.Draw(image)  
    width = image.size[0]  
    height = image.size[1]  
    k = 0
    pix = image.load()
    l = bin(len(hide))[2::]
    i = 0
    check = 63 - len(l) #63 ибо 21 пиксель под длину слова
    zero = ''
    for i in range(check):
        zero += '0'
    l = zero + l
    j = 0
    #print(l) #debug
    i = 0
    while i < len(l):
        pos = (j, 0)
        r, g, b = pix[pos][0:3]
        r = change_pix(r, l[i])
        #print(r, i) #debug
        i += 1
        if i != len(l):
            g = change_pix(g, l[i])
            #print(g, i) #debug
            i += 1
            if i != len(l):
                b = change_pix(b, l[i])
                i += 1
        j += 1
        draw.point(pos, (r, g, b))
    #print(len(hide)) #debug
    for i in range(1, height):
        if k >= len(hide):
            break
        for j in range(width):
            pos = (j, i)
            r, g, b = pix[pos][0:3]
            # четный номер пикселя = 0, нечетный = 1
            r = change_pix(r, hide[k])
            #print(r) #debug
            k += 1
            if k < len(hide):
                g = change_pix(g, hide[k])
                k += 1
                if k < len(hide):
                    b = change_pix(b, hide[k])
            draw.point(pos, (r, g, b))
            k += 1
            if k >= len(hide):
                break
    image.save('newimage.bmp', 'bmp')

def color_to_num(color):
    if color % 2 == 0:
        return '0'
    else:
        return '1'
    
def decode():
    decoded = ''
    text = ''
    image = Image.open('newimage.bmp') 
    width = image.size[0] 
    height = image.size[1]
    skip = 0
    pix = image.load()
    length = ''
    for i in range(21):
        pos = (i, 0)
        length += str(pix[pos][0] % 2)
        length += str(pix[pos][1] % 2)
        length += str(pix[pos][2] % 2)
    start = length.find('1')
    length = length[start::]
    length = int(length, 2)
    sym = 0
    #print(length) #debug
    for i in range(1, height):
        if sym >= length:
            break
        for j in range(width):
            pos = (j, i)
            if sym < length:
                r = pix[pos][0]
                decoded += color_to_num(r)
                sym += 1
                if sym < length:
                    g = pix[pos][1]
                    decoded += color_to_num(g)
                    sym += 1
                    if sym < length:
                        b = pix[pos][2]
                        decoded += color_to_num(b)
                        sym += 1 
                    else:
                        break
                else:
                    break
    mas = [decoded[x:x+8] for x in range(0, len(decoded), 8)]
    for i in mas:
        if int(i, 2) == 32:
            text += ' '
        else:
            text += chr(int(i, 2)+848)
    print(text)
    
opt = input('Type 1 for encode and 2 for decode: ')
if opt == '1':
    word = input('Input word: ')
    encode(word)
elif opt == '2':
    decode()