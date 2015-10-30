import arcode
from sys import platform as _platform

def bitReader(n): # number of bits to read
    global byteArr
    global bitPosition
    bitStr = ''
    for i in range(n):
        bitPosInByte = 7 - (bitPosition % 8)
        bytePosition = int(bitPosition / 8)
        byteVal = byteArr[bytePosition]
        bitVal = int(byteVal / (2 ** bitPosInByte)) % 2
        bitStr += str(bitVal)
        bitPosition += 1 # prepare to read the next bit
    return bitStr


def main():
    global byteArr
    global bitPosition
    path = raw_input("Enter .tpq or .spq filename: ")
    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    input_file = open(path, 'r')
    print input_file.read()

    while True:
        option = raw_input("Select option:  "
                           "\n 1: View file"
                           "\n 2: Exit"
                           "\n ..? ")

        if option == "2":
            print("/******************************END*********************************/")
            break
        elif option == "1":
            print("\n/****************************************************************/\n")
            file_c = path.rsplit("_", 1)
            file_extension = file_c.split(".")
            output_file_extension = ""
            if file_extension[0] == "1":

            elif file_extension[0] == "2":

            elif file_extension[0] == "3":

            elif file_extension[0] == "4":


            print("\n/****************************************************************/\n")
        else:
            print("Chosen option is not valid \n")


    ar = arcode.ArithmeticCode(False)
    ar.decode_file(input_file, output_file)