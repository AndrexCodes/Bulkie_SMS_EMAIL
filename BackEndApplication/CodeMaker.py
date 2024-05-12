alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
string = alphabets+numbers

import random

def genCode(num):
    code = ""
    for _ in range(num):
        code = code+random.choice(string)
    return code
