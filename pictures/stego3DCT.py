import cv2
import sys
import numpy as np
from math import log10, sqrt
from PIL import Image

quantization_table = np.array([[16,11,10,16,24,40,51,61],      
                    [12,12,14,19,26,58,60,55],    
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

def PSNR(image,secret_image):
    image = cv2.imread(image)
    secret_image = cv2.imread(secret_image)
    MSE = np.mean((image - secret_image) ** 2)
    if MSE == 0:
        print('PSNR: infinity\n')
    else:
        PSNR = 10 * log10(255 ** 2 / MSE)
        print('PSNR:', PSNR, '\nRMSE:', sqrt(MSE), '\n')
					
def dct2(block):
    return np.round(cv2.dct(block.astype(np.float32) - 128) / quantization_table)

def idct2(block):
    return np.round(cv2.idct(block * quantization_table) + 128)

def get(word):
    mas = ''
    for i in range(len(word)):
        if word[i] == ' ':
            mas += '00100000'
        else:
            mas += bin(ord(word[i])-848)[2::]
    mas += '0' * 8
    return mas   

def play_with_image(image,row=0,col=0):
    image = cv2.imread(image)
    broken_image = image.copy()
    for i in range(0, broken_image.shape[0], 8):
        for j in range(0, broken_image.shape[1]//2, 8):
            block = dct2(broken_image[i:i+8,j:j+8,2])
            block[row, col] /= 100
            broken_image[i:i+8,j:j+8,2] = idct2(block)
    cv2.imwrite('broken.bmp',broken_image)

def hide(image,message,row=3,col=3):
    message = get(message)
    #print(len(message)) #debug
    image = cv2.imread(image)
    #print(image.size/3//64) #debug
    if message == '00000000':
        print('No message')
        cv2.imwrite('secret.bmp', image)
        return None
    if (image.size / 3 // 64) < len(message):
        print('Too large messsage')
        sys.exit(1)
    secret_image = image.copy()
    pointer = 0
    for i in range(0, secret_image.shape[0], 8):
        for j in range(0, secret_image.shape[1], 8):
            block = dct2(secret_image[i:i+8,j:j+8,2])
            block[row, col] +=  - block[row, col] % 2 + int(message[pointer])
            #print(block[row, col]) #debug
            secret_image[i:i+8,j:j+8,2] = idct2(block)
            pointer += 1
            if pointer == len(message):
                break
        if pointer == len(message):
            break   
    cv2.imwrite('secret.bmp', secret_image)

def extract(image, row=3, col=3):
    img = cv2.imread(image)[:,:,2]
    message = ''
    text = ''
    end = '0' * 8
    for i in range(0,img.shape[0],8):
        for j in range(0, img.shape[1], 8):
            block = dct2(img[i:i+8, j:j+8])
            message += str(int(block[row, col]) % 2)
            if message[-8:] == end:
                break
        if message[-8:] == end:
                break    
    if message[-8:] != end or len(message) == 8:
        print('Message was not found or it is NULL')
        return ''
    #print(message) #debug1
    message = [message[x:x+8] for x in range(0, len(message)-8, 8)]
    for i in message:
        if int(i, 2) == 32:
            text += ' '
        else:
            text += chr(int(i,2)+848)
    return text

inpimage = 'plato2.bmp'
outpimage = 'secret.bmp'
opt = '1'
while opt in ['1', '2', '3', '4', '5', '6']:
    opt = input('Input 1 to hide and input 2 to extract,\ninput 3 for PSNR only'
                ', input 4 to break image: ')
    if opt == '1':
        #x = int(input('x: '))
        #y = int(input('y: '))    
        hide(inpimage, input('Write your message using RUS symbols:\n'))
        PSNR(inpimage, outpimage)
    elif opt == '2':
        #x = int(input('x: '))
        #y = int(input('y: '))    
        print(extract(outpimage), '\n')
    elif opt == '3':
        PSNR(inpimage,outpimage)
    elif opt == '4':
        play_with_image(inpimage)
    elif opt == '5':
        im = Image.open('secret.bmp')
        im.show()
        print()
    elif opt == '6':
        im = Image.open('broken.bmp')
        im.show()
        print()