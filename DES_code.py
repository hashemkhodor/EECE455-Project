from flask import Flask, request, render_template
app = Flask(__name__) #create instance of flask


############## Defined variables #########################################################################
initial_permutation_indices = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]
inverse_initial_permutation_indices = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]
input_key_indices = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
]
permuted_choice_1_indices = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]

permuted_choice_2_indices = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]

left_shift_schedule_indices = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

e_table_indices = [
    32,
    1,
    2,
    3,
    4,
    5,
    4,
    5,
    6,
    7,
    8,
    9,
    8,
    9,
    10,
    11,
    12,
    13,
    12,
    13,
    14,
    15,
    16,
    17,
    16,
    17,
    18,
    19,
    20,
    21,
    20,
    21,
    22,
    23,
    24,
    25,
    24,
    25,
    26,
    27,
    28,
    29,
    28,
    29,
    30,
    31,
    32,
    1,
]

p_box_indices = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]
s_box_1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
]

s_box_2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
]

s_box_3 = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
]

s_box_4 = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
]

s_box_5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
]

s_box_6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
]

s_box_7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
]

s_box_8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]

s_box_indices = [s_box_1, s_box_2, s_box_3, s_box_4, s_box_5, s_box_6, s_box_7, s_box_8]


##########################################################################################################


def permutation_function(plaintext, new_indices):
    # assert len(plaintext)>=len(new_indices) , "Invalid Permutation"
    new_text = ["" for i in range(len(new_indices))]
    old_plain_text = len(plaintext)
    for i in range(len(new_text)):
        # print(i,new_indices[i]-1,len(plaintext),old_plain_text)
        old_plain_text = len(plaintext)
        new_text[i] = plaintext[new_indices[i] - 1]
    return "".join(new_text)


def initial_permutation(plaintext):
    return permutation_function(plaintext, initial_permutation_indices)


def inverse_initial_permutation(ciphertext):
    return permutation_function(ciphertext, inverse_initial_permutation_indices)


def permuted_choice_1(key):
    return permutation_function(key, permuted_choice_1_indices)


def permuted_choice_2(key):
    return permutation_function(key, permuted_choice_2_indices)


def bit_swap_32(plaintext):
    return plaintext[32:] + plaintext[0:32]


def schedule_left_shifts(index):
    return left_shift_schedule_indices[index]


def e_table(plaintext):
    # plaintext_copy=plaintext+plaintext[0:16]
    return permutation_function(plaintext, e_table_indices)


def xor(x, y, min_size=0):
    return int_to_bin(bin_to_int(x) ^ bin_to_int(y), min_size)


def group_text(text, group_size):
    if group_size == 0:
        return []
    result = []
    index = 0
    n = len(text)
    while index < n:
        group = text[index : min(index + group_size, index + n - index + 1)]
        result.append(group)
        index = index + group_size
    return result


def bin_to_int(binary_str):
    binary_str_copy = binary_str[::-1]
    # print(binary_str_copy)
    coeff = 1
    result = 0
    for i in range(len(binary_str_copy)):
        result += int(binary_str_copy[i]) * coeff
        coeff = coeff * 2
    return result


def int_to_bin(x, min_size):
    result = []
    while x > 0:
        bit = "1" if x % 2 == 1 else "0"
        result.append(bit)
        x = x // 2
    result.reverse()
    result = ["0"] * (min_size - len(result)) + result
    return "".join(result)


def s_shrink(plaintext, s_box_table):
    row = bin_to_int(plaintext[0] + plaintext[-1])
    col = bin_to_int(plaintext[1:-1])
    return int_to_bin(s_box_table[row][col], 4)


def s_box(plaintext):
    groups = group_text(plaintext, 6)
    result = []
    for i in range(len(groups)):
        group = groups[i]
        s_group = s_shrink(group, s_box_indices[i])
        result.append(s_group)
    return "".join(result)


def p_box(plaintext):
    return permutation_function(plaintext, p_box_indices)


def generate_all_keys(key):
    keys = []
    key = permuted_choice_1(key)
    # print(len(key))
    for i in range(16):
        rotations = schedule_left_shifts(i)
        key = circularshiftleft(key, rotations)
        _key_ = permuted_choice_2(key)
        keys.append(_key_)
    keys.reverse()
    return keys


def DES(plaintext, key):
    keys=[]
    L,R=[],[]
    
    
    plaintext = initial_permutation(plaintext)
    keys.append("")
    L.append(str(hex(int('0b{}'.format(plaintext[:32]),2))))
    R.append(str(hex(int('0b{}'.format(plaintext[32:]),2))))
    key = permuted_choice_1(key)
    # print(len(key))
    for i in range(16):
        rotations = schedule_left_shifts(i)
        
        key = circularshiftleft(key, rotations)
        _key_ = permuted_choice_2(key)
        
        
        
        
        
        plaintext = round(plaintext, _key_, i)
        keys.append(hex(int('0b{}'.format('0'*(64-len(_key_))+_key_),2)))
        L.append(str(hex(int('0b{}'.format(plaintext[:32]),2))))
        R.append(str(hex(int('0b{}'.format(plaintext[32:]),2))))
        
        
        
    ciphertext = bit_swap_32(plaintext)
    ciphertext = inverse_initial_permutation(ciphertext)
    # print(len(ciphertext))
    L.append(str(hex(int('0b{}'.format(ciphertext[:32]),2))))
    R.append(str(hex(int('0b{}'.format(ciphertext[32:]),2))))
    keys.append("")
    return keys,L,R

def DES_DECRYPT(ciphertext, key):
    keyss=[]
    L,R=[],[]
    ciphertext = initial_permutation(ciphertext)
    keyss.append("")
    L.append(str(hex(int('0b{}'.format(ciphertext[:32]),2))))
    R.append(str(hex(int('0b{}'.format(ciphertext[32:]),2))))
    keys = generate_all_keys(key)
    for i in range(16):      
        ciphertext = round(ciphertext, keys[i], i)
        _key_ = keys[i]
        keyss.append(hex(int('0b{}'.format('0'*(64-len(_key_))+_key_),2)))
        L.append(str(hex(int('0b{}'.format(ciphertext[:32]),2))))
        R.append(str(hex(int('0b{}'.format(ciphertext[32:]),2))))
    plaintext = bit_swap_32(ciphertext)
    L.append(str(hex(int('0b{}'.format(plaintext[:32]),2))))
    R.append(str(hex(int('0b{}'.format(plaintext[32:]),2))))
    keyss.append("")
    return keyss,L,R


"""
def DES_decrypt(ciphertext, key):
    ciphertext = initial_permutation(ciphertext)
    # ciphertext = bit_swap_32(ciphertext)
    key = permuted_choice_1(key)
    keys = generate_all_keys(key)
    for i in range(len(keys)):
        _key_ = keys[i]
        ciphertext = round(ciphertext, _key_, i)

    plaintext = bit_swap_32(ciphertext)
    return inverse_initial_permutation(plaintext)
"""


def circularshiftleft(key, rotated):
    # print(rotated)
    C = key[0:28]
    D = key[28:56]
    # print('C_i= ',C)
    # print('D_i=',D)
    # Temp1=C[::]
    # Temp2=D[::]
    # C
    C = C[rotated:] + C[:rotated]
    D = D[rotated:] + D[:rotated]
    # print('C_ix= ',C)
    # print('D_ix=',D)
    return C + D


def round(plaintext, key, i):
    L = plaintext[0:32]
    R = plaintext[32:64]
    L_new = R
    R_new = xor(L, F(R, key), 32)
    return L_new + R_new


def F(plaintext, key):
    plaintext = e_table(plaintext)
    plaintext = xor(plaintext, key, 48)
    plaintext = s_box(plaintext)
    return p_box(plaintext)


def nice_format(text):
    return " ".join(group_text(text, 4))

@app.route("/",methods=['POST','GET'])
def m(): 
    result = []
    proc = ""
    r = ""
    if request.method == 'POST':
        if 'encrypt' in request.form:
            p = int(request.form.get('plain'),16)
            plaintext=str(bin(p))[2:]
            plaintext="0"*(64-len(plaintext))+plaintext
            
            k = int(request.form.get('key'),16)

            key=str(bin(k))[2:]
            key="0"*(64-len(key))+key
            keys,L,R=DES(plaintext,key)
            rounds = ["IP",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,"IP-1"]
            result = [(x, y, z,w) for x, y, z,w in zip(rounds,keys, L, R)]
            proc = "Encryption"
            r = str(L[17])+str(R[17])
           
        else:
            p = int(request.form.get('plain'),16)
    
            plaintext=str(bin(p))[2:]
            plaintext="0"*(64-len(plaintext))+plaintext
            k = int(request.form.get('key'),16)
            key=str(bin(k))[2:]
            key="0"*(64-len(key))+key
            keys,L,R=DES_DECRYPT(plaintext,key)
            rounds = ["IP",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,"IP-1"]
            result = [(x, y, z,w) for x, y, z,w in zip(rounds,keys, L, R)]
            proc = "Decryption"
            r = str(L[17])+str(R[17])
            
    return render_template("DES.html",result=result, proc=proc, r =r )
if __name__ == "__main__":
    app.run() 
    
    
    
    