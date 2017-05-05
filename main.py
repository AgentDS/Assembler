#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 PM4:10
# @Author  : Shiloh Leung
# @Site    : 
# @File    : main.py
# @Software: PyCharm Community Edition

from Assembler.AssemblerBag import *

InsFileName = input('输入指令文件名: ')
if len(InsFileName) < 1:
    InsFileName = 'InsIn.txt'

ins_arr = ReadInstruction(InsFileName)
BinOut = BinFileMaker(InsFileName)
lineCount = 0
for instruction in ins_arr:
    lineCount = lineCount + 1
    print("Line: ", lineCount)
    Assembling(instruction, lineCount, BinOut)

CloseBinFile(BinOut)