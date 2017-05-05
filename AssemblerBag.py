#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 PM4:11
# @Author  : Shiloh Leung
# @Site    : 
# @File    : AssemblerBag.py
# @Software: PyCharm Community Edition



def ReadInstruction(InstructionFname):
    fr = open(InstructionFname)
    strArray = [line for line in fr.readlines()]
    fr.close()
    return strArray


def BinFileMaker(InstructionFname):
    BinName = '.'.join(InstructionFname.split('.')[0:-1]) + '_BINOUT.txt'
    BinOut = open(BinName, 'w')
    return BinOut


def CloseBinFile(BinOut):
    BinOut.close()


def ErrPrinter(lineCount, errMessage):
    print('***LINE:', end='')
    print("%3d  " % (lineCount), end='')
    print(errMessage)



def Lexer(Instruction, lineCount):
    wordList = Instruction.strip().split()
    lexTuple = []

    for word in wordList:
        wordLength = len(word)
        First = 0
        Second = 0
        while First < wordLength:
            if word[First].isalpha():
                Second = Second + 1
                while (Second < wordLength and (word[Second].isalpha() or word[Second].isdigit())):
                    Second = Second + 1
                singleWord = word[First:Second]
                lexTuple.append(singleWord)
                First = Second

            elif word[First].isdigit():
                Second = Second + 1
                while Second < wordLength and word[Second].isdigit():
                    Second = Second + 1
                constant = word[First:Second]
                lexTuple.append(constant)
                First = Second

            elif word[First] == ',':
                singleWord = ','
                lexTuple.append(singleWord)
                First = First + 1
                Second = Second + 1

            elif word[First] == '(':
                singleWord = '('
                lexTuple.append(singleWord)
                First = First + 1
                Second = Second + 1

            elif word[First] == ')':
                singleWord = ')'
                lexTuple.append(singleWord)
                First = First + 1
                Second = Second + 1

            else:
                ErrPrinter(lineCount, "指令错误, 不支持当前字符 '" + word[First] + "'")
                return None


    return lexTuple


def BinZeroExt(BinStr, BitNum):
    len1 = len(BinStr)
    if len1 > BitNum:
        return BinStr[0:BitNum]
    else:
        return '0'*(BitNum - len1) + BinStr



def Parser(lexTuple, lineCount):
    operation = lexTuple[0]
    if operation == 'add' or operation == 'and' or operation == 'or' or operation == 'xor':
        if len(lexTuple) != 6 or lexTuple[2] != ',' or lexTuple[4] != ',':
            ErrPrinter(lineCount, "语法错误")
            raise SyntaxError("语法错误")
        rd = BinZeroExt(bin(int(lexTuple[1]))[2:], 5)    # [14:10]
        rs = BinZeroExt(bin(int(lexTuple[3]))[2:], 5)    # [9:5]
        rt = BinZeroExt(bin(int(lexTuple[5]))[2:], 5)    # [4:0]
        # [31:26]
        if operation == 'add':
            op = '000000'
        else:
            op = '000001'
        # [25:20]
        if operation == 'add' or operation == 'and':
            op2 = '000001'
        elif operation == 'or':
            op2 = '000010'
        else:
            op2 = '000100'

        return op + op2 + '00000' + rd + rs + rt

    elif operation == 'sra' or operation == 'srl' or operation == 'sll':
        if len(lexTuple) != 6 or lexTuple[2] != ',' or lexTuple[4] != ',':
            ErrPrinter(lineCount, "语法错误")
            raise SyntaxError("语法错误")
        op = '000010'    # [31:26]
        # [25:20]
        if operation == 'sra':
            op2 = '000001'
        elif operation == 'srl':
            op2 = '000010'
        else:
            op2 = '000011'

        shift = BinZeroExt(bin(int(lexTuple[5]))[2:], 5)    # [19:15]
        rd = BinZeroExt(bin(int(lexTuple[1]))[2:], 5)  # [14:10]
        rt = BinZeroExt(bin(int(lexTuple[3]))[2:], 5)  # [4:0]

        return op + op2 + shift + rd + '00000' + rt

    elif operation == 'addi':
        if len(lexTuple) != 6 or lexTuple[2] != ',' or lexTuple[4] != ',':
            ErrPrinter(lineCount, "语法错误")
            raise SyntaxError("语法错误")
        op = '000101'    # [31:26]

        # [25:10]
        if int(lexTuple[5]) < 0:
            imm = bin(int(lexTuple[5]) + 2**16)[2:0]
        else:
            imm = BinZeroExt(bin(int(lexTuple[5]))[2:], 16)

        rs = BinZeroExt(bin(int(lexTuple[3]))[2:], 5)  # [9:5]
        rt = BinZeroExt(bin(int(lexTuple[1]))[2:], 5)  # [4:0]

        return op + imm + rs + rt

    elif operation == 'andi' or operation == 'ori' or operation == 'xori':
        if len(lexTuple) != 6 or lexTuple[2] != ',' or lexTuple[4] != ',':
            ErrPrinter(lineCount, "语法错误")
            raise SyntaxError("语法错误")
        # [31:26]
        if operation == 'andi':
            op = '001001'
        elif operation == 'ori':
            op = '001010'
        elif operation == 'xori':
            op = '001100'

        imm = BinZeroExt(bin(int(lexTuple[5]))[2:], 16)  # [25:10]
        rs = BinZeroExt(bin(int(lexTuple[3]))[2:], 5)  # [9:5]
        rt = BinZeroExt(bin(int(lexTuple[1]))[2:], 5)  # [4:0]

        return op + imm + rs + rt

    elif operation == 'load' or operation == 'store':
        if len(lexTuple) != 7 or lexTuple[2] != ',' or lexTuple[4] != '(' or lexTuple[6] != ')':
            ErrPrinter(lineCount, "load/store指令语法错误")
            raise SyntaxError("语法错误")

        # [31:26]
        if operation == 'load':
            op = '001101'
        else:
            op = '001110'

        # [25:10]
        if int(lexTuple[3]) < 0:
            offset = bin(int(lexTuple[3]) + 2**16)[2:0]
        else:
            offset = BinZeroExt(bin(int(lexTuple[3]))[2:], 16)

        rs = BinZeroExt(bin(int(lexTuple[5]))[2:], 5)  # [9:5]
        rt = BinZeroExt(bin(int(lexTuple[1]))[2:], 5)  # [4:0]

        return op + offset + rs + rt

    elif operation == 'beq' or operation == 'bne':
        if len(lexTuple) != 6 or lexTuple[2] != ',' or lexTuple[4] != ',':
            ErrPrinter(lineCount, "条件转移指令语法错误")
            raise SyntaxError("语法错误")
        # [31:26]
        if operation == 'beq':
            op = '001111'
        else:
            op = '010000'

        # [25:10]
        if int(lexTuple[5]) < 0:
            offset = bin(int(lexTuple[5]) + 2**16)[2:0]
        else:
            offset = BinZeroExt(bin(int(lexTuple[5]))[2:], 16)
        rs = BinZeroExt(bin(int(lexTuple[1]))[2:], 5)  # [9:5]
        rt = BinZeroExt(bin(int(lexTuple[3]))[2:], 5)  # [4:0]

        return op + offset + rs + rt

    elif operation == 'jump':
        if len(lexTuple) != 2 or lexTuple[1][-1] != 'H':
            ErrPrinter(lineCount, "jump指令语法错误")
            raise SyntaxError("语法错误")
        op = '010010'
        target = BinZeroExt(bin(int(lexTuple[1][:-1], 16))[2:], 32)
        if target[-2:] != '00':
            ErrPrinter(lineCount, "jump指令中跳转地址格式错误, 必须为4的整数倍")
            raise SyntaxError("地址格式错误")
        address = target[4:-2]    # [25:0]

        return op + address

    else:
        ErrPrinter(lineCount, "指令错误, 不支持当前操作 '" + operation + "'")
        raise SyntaxError("未知指令")


def BinInsPrinter(BinIns, BinOut):
    print(BinIns, file=BinOut)


class SyntaxError(Exception):
    pass


def Assembling(Instruction, lineCount, BinOut):
    """
    ArgIn:
    Instruction : str, one instruction in assembly language

    ArgOut:
    BinStr : str, instruction in bin string format;

    if return None, then instruction has syntax errors
    """
    # lexer
    lexTuple = Lexer(Instruction, lineCount)
    #print(lexTuple)
    if lexTuple is None:
        raise SyntaxError("语法错误, 请检查")
    if len(lexTuple) != 0:
        BinInstruction = Parser(lexTuple, lineCount)
        BinInsPrinter(BinInstruction, BinOut)









