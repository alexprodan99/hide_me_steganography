import numpy as np
import types


def convert_message_to_binary(message):
    if type(message) == str:
        return ''.join([ format(ord(char), "08b") for char in message ])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [ format(char, "08b") for char in message ]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")

# Function to hide the secret message into the image
def hide_data(image, secret_message):
    
    height, width, depth = image.shape
    # calculate the maximum bytes to encode
    n_bytes = height * width * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    #Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
  
    secret_message += "#####" # you can use any string as the delimeter

    data_index = 0
    # convert input data to binary format using messageToBinary() fucntion
    binary_secret_msg = convert_message_to_binary(secret_message)

    data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
    for i in range(0, height):
        for j in range(0, width):
            # convert RGB values to binary format
            r, g, b = convert_message_to_binary(image[i, j])
            
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # hide the data into least significant bit of red pixel
                image[i, j][0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # hide the data into least significant bit of green pixel
                image[i, j][1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # hide the data into least significant bit of  blue pixel
                image[i, j][2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def show_data(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = convert_message_to_binary(pixel) #convert the red,green and blue values into binary format
            binary_data += r[-1] #extracting data from the least significant bit of red pixel
            binary_data += g[-1] #extracting data from the least significant bit of red pixel
            binary_data += b[-1] #extracting data from the least significant bit of red pixel
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]

    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte,2))
        if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
            break
    return decoded_data[:-5] #remove the delimeter to show the original hidden message
