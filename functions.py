import struct
import keystone
from keystone import *
import binascii
import math
import os

def make_hex(x, r):
    p = math.floor(math.log(x, 2))
    a = round(16*(p-2) + x / 2**(p-4))
    if a<0: a += 128
    a = 2*a + 1
    h = hex(a).lstrip('0x').rjust(2,'0').upper()
    hex_value = f'0{r}' + h[1] + '02' + h[0] + '1E' 
    print(hex_value)
    return hex_value

def asm_to_hex(asm_code):
    ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    encoding, count = ks.asm(asm_code)
    return ''.join('{:02x}'.format(x) for x in encoding)

def mvdk_hex23(num):
    num = round(num, 15)
    packed = struct.pack('!f', num)
    full_hex = ''.join('{:02x}'.format(b) for b in packed)
    hex_1 = full_hex[:4]
    hex_2 = full_hex[4:]
    asm_1 = f"movz w10, #0x{hex_2}"
    asm_2 = f"movk w10, #0x{hex_1}, lsl #16"
    asm_3 = f"movz w8, #0x{hex_2}"
    asm_4 = f"movk w8, #0x{hex_1}, lsl #16"
    hex_value1 = asm_to_hex(asm_1)
    hex_value2 = asm_to_hex(asm_2)
    hex_value3 = asm_to_hex(asm_3)
    hex_value4 = asm_to_hex(asm_4)
    return hex_value1, hex_value2, hex_value3, hex_value4