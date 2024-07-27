import random
from itertools import chain

#Generarea unui tabel de permutare random
def generate_random_permutation(lenght):
    permutation = list(range(1, lenght + 1))
    random.shuffle(permutation)
    return permutation

#Generarea inversului tabelului de permutare
def generate_inverse_permutation(permutation):
    inverse_permutation = [0] * len(permutation)
    for i, pos in enumerate(permutation):
        inverse_permutation[pos-1] = i +1

    return inverse_permutation

#Generarea unui initial permutation (IP) si inversul lui (IP-1)
def generate_ip():
    return generate_random_permutation(64)

def generate_ip_inverse(ip):
    return generate_inverse_permutation(ip)

#Generarea unei chei random de permutare (pc1)
def generate_pc1():
    list_pc = [i for i in range(1, 65) if i % 8 != 0]
    random.shuffle(list_pc)
    return list_pc

#Generarea unei permutari random a compresiei (pc2)
def generate_pc2():
    list_pc = list(range(1, 57))
    random.shuffle(list_pc)
    return list_pc[:48]

#Generarea unei chei
def generate_key():
    return[random.randint(0, 1)for _ in range(64)]

#Generarea unei tabel de expansiune random (E)
def generate_expansion_table():
    list_e = list(range(1, 33))
    random.shuffle(list_e)
    list_e.extend(list_e[:16])
    return list_e

#Generarea a 8 s_boxes random de 16x4
def generate_s_boxes():
    s_boxes = []
    for _ in range(8):
        s_box = [list(range(16)) for _ in range(4)]
        for row in s_box:
            random.shuffle(row)
        s_boxes.append(s_box)
    return s_boxes

#Generarea unui tabel de permutare (P)
def generate_p_table():
    return generate_random_permutation(32)

#Functie de permutare a unui bloc conform unui tabel
def permute(block, table):
    return [block[i-1]for i in table]

#Functie de operare a operatiei XOR pe s blocuri de biti
def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

#Functie pentru a efectua substitutia in baza la s_box
def s_box_substitution(bits, s_boxes):
    output = []
    for i in range(8):
        block = bits[i * 6:(i + 1) * 6]
        row = int(f"{block[0]}{block[5]}", 2)
        col = int(''.join(map(str, block[1:5])), 2)
        s_box_val = s_boxes[i][row][col]
        output.extend([int(x) for x in format(s_box_val, '04b')])
    return output

#Generarea a 16 subchei din cheia principala
def generate_subkeys(key, pc1, pc2):
    key_permuted= permute(key, pc1)
    c, d = key_permuted[:28], key_permuted[28:]
    subkeys = []
    for i in range(16):
        shift = 1 if i in [0, 1, 8, 15] else 2
        c = c[shift:] + c[:shift]
        d = d[shift:] + d[:shift]
        subkeys.append(permute(c + d, pc2))
    return subkeys

#Functie round 
def des_round(block, subkey, e_table, s_boxes, p_table):
    left, right = block[:32], block[32:]
    right_expanded = permute(right, e_table)
    xor_result = xor(right_expanded, subkey)
    s_box_result = s_box_substitution(xor_result, s_boxes)
    p_result = permute(s_box_result, p_table)
    new_right = xor(left, p_result)
    return right + new_right

#Functie de encriptare DES
def des_encrypt(block, subkeys, ip, ip_inv, e_table, s_boxes, p_table):
    block = permute(block, ip)
    for subkey in subkeys:
        block = des_round(block, subkey, e_table, s_boxes, p_table)
    block = block[32:] + block[:32]
    return permute(block, ip_inv)

#Functie de decriptare DES
def des_decrypt(block, subkeys, ip, ip_inv, e_table, s_boxes, p_table):
    block = permute(block, ip)
    for subkey in reversed(subkeys):
        block = des_round(block, subkey, e_table, s_boxes, p_table)
    block = block[32:] + block[:32]
    return permute(block, ip_inv)

#Functie de convertire a string-ului in binar
def string_to_bits(s):
    return [int(bit) for char in s for bit in format(ord(char), '08b')]

#Functie de convertire a binar-ului in string
def bits_to_string(bits):
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(map(str, char)), 2)) for char in chars)

# Functie de pad pentru mesaj pana la un multiplu a 64 bits (se adauga spatiu)
def pad_message(message):
    padding_length = 64 - len(message) % 64
    return message + [0] * padding_length

#Genereaza ip, ip_inv, pc1, pc2, key, e, s_boxes, p
ip = generate_ip()
ip_inv = generate_ip_inverse(ip)
pc1 = generate_pc1()
pc2 = generate_pc2()
key = generate_key()
e = generate_expansion_table()
s_boxes = generate_s_boxes()
p = generate_p_table()

#Genereaza subchei
subkeys = generate_subkeys(key, pc1, pc2)

#Deschide fisierul test.txt si citeste ce e in el apoi il inchide
file = open("test.txt", "r")
file_content = file.read()
file.close()

#Face ca mesajul ce trebuie criptat sa fie textul din text.txt
message = file_content

#Printeaza mesajul ce trebuie criptat
print("Original message:", message)

#Message_bits va fi binar-ul string-ului message iar message_bits_padded va face message_bits sa fie padded padded
message_bits = string_to_bits(message)
message_bits_padded = pad_message(message_bits)

#Encripteaza mesajul si il printeaza
encrypted_message_bits = []
for i in range(0, len(message_bits_padded), 64):
    block = message_bits_padded[i:i + 64]
    encrypted_message_bits.extend(des_encrypt(block, subkeys, ip, ip_inv, e, s_boxes, p))

encrypted_message = bits_to_string(encrypted_message_bits)
print("Encrypted message (string):", encrypted_message)
print("Encrypted message (binary):", ''.join(map(str, encrypted_message_bits)))

#Decripteaza mesajul si il printeaza
decrypted_message_bits = []
for i in range(0, len(encrypted_message_bits), 64):
    block = encrypted_message_bits[i:i + 64]
    decrypted_message_bits.extend(des_decrypt(block, subkeys, ip, ip_inv, e, s_boxes, p))

decrypted_message = bits_to_string(decrypted_message_bits).rstrip('\x00')  #Scoate padding-ul
print("Decrypted message:", decrypted_message)

#Verifica daca decriptarea mesajului a fost efectuata corect
assert message == decrypted_message, "Decryption failed!"
