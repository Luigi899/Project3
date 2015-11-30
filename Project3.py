'''
    STEGANOGRAPHY - Hiding messages in different types of media.
    This part of the program is the encoder.
    It will encode our message into the image.
    '''

#Required: Libraries
from PIL import Image
from PIL import ImageFilter
import PIL.ImageOps
import getpass

#Definition to encode message into image
def encode_message(img, msg):
    #Check message length & mode
    length = len(msg)
    
    if(length>255):
        print("The message is too long. Keep it under 255 characters.")
        return False
    '''if(img.mode != "RGB"):
        print("Image needs to be in RBG mode.")
        return False'''
    
    #Creating image copy to encode
    encoded = img.copy()
    width, height = img.size
    counter = 0
    
    for x in range(height):
        for y in range(width):
            #Variables holding pixel values
            r, g, b = img.getpixel((y,x))
            if x == 0 and y == 0 and counter < length:
                #First pixel will show message length
                ascii_code = length
            elif counter <= length:
                char = msg[counter-1]
                #Getting ASCII value
                ascii_code = ord(char)
            else:
                #Set ascii value to red
                ascii_code = r
            
            #Encoding message into pixel red value
            encoded.putpixel((y, x), (ascii_code, g, b))
            counter += 1
    print("Message has been encoded.")
    return encoded

#Whatever image we decide to use converted to .bmp
ori_img = "secret.bmp"
img1 = Image.open(ori_img)
img2 = PIL.ImageOps.invert(img1)
img = img2.filter(ImageFilter.BLUR)
enc_img = "enc_" + ori_img

#Definition to decode message from image
def decode_message(img):
    width, height = img.size
    counter = 0
    msg = ''; #Empty variable to hold message
    
    for x in range(height):
        for y in range(width):
            #Get pixels, for this purpose red is the focus
            try:
                r, b, g = img.getpixel((y,x))
            except:
                r, b, g, a = img.getpixel((y,x))
            
            if x == 0 and y == 0:
                #First red pixel has our message length
                length = r
            elif counter <= length:
                #Change r(ASCII) value to a character and add it to msg
                msg += chr(r)
            counter += 1
return msg

#Set message to encode into image
msg = getpass.getpass("Set message: ")
savemsg = input("\nSave message to file? [y/n] ")
while savemsg:
    if (savemsg == "y") | (savemsg == "yes"):
        msgName = str(input("Name the text file: ")) + ".html"
        msgFile = open(msgName, "w")#File that will be create if does not already exist
        msgFile.write('<img src="enc_secret.bmp" /><p>' + msg + '</p>')#Write message
        msgFile.close()
        print(msgName + " successfully created.\n")
        break
    elif (savemsg == "n") | (savemsg == "no"):
        break
    else:
        savemsg = input("\nSave message to text file? [y/n] ")

#Set password to get decoded message
mypassword = getpass.getpass('Set password: ')
print("Encoding messasge..\n")

img_encoded = encode_message(img,msg)
if img_encoded:
    #Save encoded image
    import os
    img_encoded.save(enc_img)
    print("{} saved!".format(enc_img))
    
    #View the saved file, works with Windows only
    #os.startfile(msgName) #view html file
    #os.startfile(enc_img) #view image file
    
    viewmsg = input("Do you want to decode the message? [y/n]")
    while viewmsg:
        if (viewmsg == "y") | (viewmsg == "yes") | (viewmsg == "sure"):
            #Password Feature
            password = getpass.getpass("\nEnter password: ")
            print("Decoding messasge..\n")
            
            while(password!=mypassword):
                print("Wrong password!\nTry again.")
                password = getpass.getpass("Enter password: ")
            
            if(password==mypassword):
                img2 = Image.open(enc_img)
                secret_msg = decode_message(img2)
                print("Secret Message: " + secret_msg)
                break
        elif (viewmsg == "n") | (viewmsg == "no") | (viewmsg == "nah"):
            break
        else:
            viewmsg = input("Do you want to decode the message? [y/n]")

input("Press enter to exit.")