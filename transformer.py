import sys;

"""
This program receives Input (messages file),
Instructions(encryption file) and output file
name as input and encrypts the messages from 
input file to generate output file.

Once the output file is passed as input
with type argument as t, the encrypted
messages will be decrypted and it will
match exactly with the input file.

"""


def Input(message, instructions, type):
    '''

    Based on the infrmation entered, this method
    will split the instruction in readable format
    which is then passed to the methods as parameters
    for ecnryption and decryption.

    :param message: Input message that needs to be encrypted
    :param instructions: encryption pattern
    :param type: e/d based on what needs to be done encryption or decryption
    :returns String message:
    '''

    strinst_new = instructions.split(';')
    if (type == 'd'):
        strinst = strinst_new.__reversed__()
    else:
        strinst = strinst_new
    Finalmessage = message
    for i in strinst:
        strlist = str(i)
        opInst = strlist.split(',')
        operator = opInst[0]
        if (opInst[1] != ''):
            exponent = int(opInst[1])
        else:
            exponent = 1
        Finalmessage = encrypt(Finalmessage, operator, exponent, type)
    return Finalmessage


def encrypt(message, operator, exponent, type):
    '''
    Based on the pattern entered, this methid will gice call
    to the respective methods for applying
    encryption/decryption algorithms

    :param message: Input message
    :param operator: current operator symbol
    :param exponent: no of times we need to perform the fucntion
    :param type: encryption/decryption
    :returns String message:
    '''
    operation = operator[0]
    pos1 = 0
    pos2 = 0
    groups = 0
    index = 0
    noofgroups = 0
    if (operation != 'T'):
        if(operation != 'A'):
            index = int(operator[1])
        else: index=0
    else:
        if (operator[1] == '('):
            noofgroups = int(operator[2])
            pos1 = int(operator[4])
            pos2 = int(exponent)
        else:
            pos1 = int(operator[1])
            pos2 = int(exponent)

    if operation == "S":
        encryptedMessage = Shift(message, index, exponent, type)
    elif operation == "R":
        encryptedMessage = Rotate(message, exponent, type)
    elif operation == "D":
        encryptedMessage = Duplicate(message, index, exponent, type)
    elif operation == "A":
        encryptedMessage = shiftself(message,exponent,type)
    elif operation == "T":
        if operator[1] != '(':
            encryptedMessage = Swap(message, pos1, pos2, type)
        else:
            message = message
            encryptedMessage = Swap_groups(message, pos1, pos2, noofgroups, type)
    else:
        encryptedMessage = "Input function incorrect"
    return encryptedMessage


def Shift(message, index, exponent, type):
    '''
    type - encryption
    Shifts the letter at index i forward one
    letter in the alphabet

    type - decryption
    will perform he opposite of encryption in reverse
    order of instructions

    :param message: Input message
    :param operator: current operator symbol
    :param exponent: no of times we need to perform the fucntion
    :param type: encryption/decryption
    :returns String message:
    '''


    changechar = message[index]
    asciivalue = ord(changechar)

    if (type == 'e'):
        for i in range(exponent):
            asciivalue = asciivalue + 1
            changechar = chr(asciivalue)
            newmessage = message.replace(message[index], changechar, 1)

        return newmessage
    else:
        for i in range(exponent):
            asciivalue = asciivalue - 1
            changechar = chr(asciivalue)
            newmessage = message.replace(message[index], changechar, 1)
        return newmessage


def Rotate(message, exponent, type):
    '''
     Rotates the string one poistion to
     right
     type - decryption
     will perform he opposite of encryption in reverse
     order of instructions
     :param message: Input message
     :param exponent: no of times we need to perform the fucntion
     :param type: encryption/decryption
     :returns String message:
     '''

    for i in range(exponent):
        if (type == 'e'):
            message = message[-1] + message[:-1]
        # print(message)
        return message
    else:
        message = message[1:] + message[0]
        # print(message)
        return message


def Duplicate(message, index, exponent, type):

    '''
    Duplicates the letter at index index

    type - decryption
    will perform he opposite of encryption in reverse
    order of instructions

    :param message: Input message
    :param operator: current operator symbol
    :param exponent: no of times we need to perform the fucntion
    :param type: encryption/decryption
    :returns String message:
    '''


    duplchar = message[index]
    newmessage = message[:index + 1]

    if (type == 'e'):
        for i in range(exponent):
            newmessage = newmessage + duplchar
        Finalmessage = newmessage + message[index + 1:]

        return Finalmessage
    else:

        Finalmessage = newmessage + message[(index + exponent) + 1:]

        return Finalmessage


def Swap(message, pos1, pos2, type):

    '''
    Swaps the letter at index pos1 and pos2

    type - decryption
    will perform he opposite of encryption in reverse
    order of instructions

    :param message: Input message
    :param pos1: the first index for swapping
    :param pos2: Second index for swapping
    :param type: encryption/decryption
    :returns String message:
    '''


    if (pos1 < pos2):
        newmessage = message[:pos1] + message[pos2] + message[(pos1) + 1:pos2] + message[pos1] + message[pos2 + 1:]
    elif (pos1 > pos2):
        newmessage = message[:pos2] + message[pos1] + message[(pos2) + 1:pos1] + message[pos2] + message[(pos1) + 1:]
    else:
        newmessage = message


    return newmessage

def Swap_groups(message, pos1, pos2, noofgroups, type):

    '''
    divide the strings into 'noofgroups' individual
    groups and then swaps the strings from pos1 and pos2

    type - decryption
    will perform he opposite of encryption in reverse
    order of instructions

    :param message: Input message
    :param pos1: the first index for swapping
    :param pos2: Second index for swapping
    :param noofgroups: noofgroups in which string needs to be divided
    :param type: encryption/decryption
    :returns String message:
    '''

    if (noofgroups>0):
        n = int(len(message))/noofgroups
    else:
        n=1;
    sub = []
    result=[]
    partial_step=''
    s=''
    newmessage=''
    for i in message:
        sub+=i
        if len(sub)==n:
            result+=[sub]
            sub=[]
    if sub :
        result+=[sub]

    result[pos1],result[pos2] = result[pos2],result[pos1]

    for i in range(int(len(result))):
        newmessage= newmessage+ partial_step.join(result[i])

    return newmessage

def shiftself(message,exponent,type):

    '''
    This will shift all the charachters by 1.
    so for eg input DELL with exponent 5 (A,5)
    output will be IJQQ

    type - decryption
    will perform he opposite of encryption in reverse
    order of instructions

    :param message: Input message
    :param exponent: no of characters to be shifted
    :param type: encryption/decryption
    :returns String message:
    '''

    data=list(message[:-1])
    if (type=='e'):
        for i, char in enumerate(data):
            data[i] = chr((ord(char) - ord('A') + exponent)%26 + ord('A'))
        newmessage = ''.join(data)
        Finalmessage = newmessage + "\n"
        return Finalmessage
    else:
        for i, char in enumerate(data):
            data[i] = chr((ord(char) - ord('A') - exponent)%26 + ord('A'))
        newmessage = ''.join(data)
        Finalmessage = newmessage + "\n"
        return Finalmessage

def main():


    '''
    Reads the input , instuctions and Output
    files as input from system command line
    arguments and prints the output both at console
    and output file.

    '''

    Inputfile = sys.argv[1]

    Instructionsfile = sys.argv[2]
    Outputfile = sys.argv[3]
    typeInst = sys.argv[4]

    file = open('' + Inputfile + '.txt', "r")
    messageList = file.readlines()

    file2 = open('' + Instructionsfile + '.txt', "r")
    InstructionsList = file2.readlines()

    file3 = open('' + Outputfile + '.txt', "a")
    for i in range(len(InstructionsList)):
        message = messageList[i]
        Instructions = InstructionsList[i]
        finalmessage = Input(message, Instructions, typeInst)
        print("Input string : - " + message)
        print("Output String after applying " + InstructionsList[i] + " is \n" + finalmessage)

        file3.write(finalmessage)
    file3.close()


if __name__ == '__main__':
    main()