#  <span style="color: DeepSkyBlue  ">DES encryption and decryption
___
## **Pasul 1**
### *<span style="color: HotPink ">Primim un mesaj dintr-un fișier .txt*
````
file = open("test.txt", "r")
file_content = file.read()
file.close()

message = file_content

print("Original message:", message)
````
## **Pasul 2**

### *<span style="color: HotPink ">Conversia în cod binar </span>*
````
message_bits = string_to_bits(message)
message_bits_padded = pad_message(message_bits)
````
## **Pasul 3**

### *<span style="color: HotPink ">Generarea unui IP* 
````
def generate_ip():
    return generate_random_permutation(64)
````
## **Pasul 4**

### *<span style="color: HotPink ">Generarea IP<sup>-1</sup> (IP minus gradul 1)*
````
def generate_ip_inverse(ip):
    return generate_inverse_permutation(ip)
````
## **Pasul 5**

### *<span style="color: HotPink ">Generarea unei chei*

````
def generate_key():
    return[random.randint(0, 1)for _ in range(64)]
````
## **Pasul 6**

### *<span style="color: HotPink ">Codificăm cheia de 16 ori*

````
for subkey in subkeys:
        block = des_round(block, subkey, e_table, s_boxes, p_table)
    block = block[32:] + block[:32]
    return permute(block, ip_inv)
````
## **Pasul 7**

### *<span style="color: HotPink ">Folosim cheia pentru a codifica textul*

````
encrypted_message_bits = []
for i in range(0, len(message_bits_padded), 64):
    block = message_bits_padded[i:i + 64]
    encrypted_message_bits.extend(des_encrypt(block, subkeys, ip, ip_inv, e, s_boxes, p))
encrypted_message = bits_to_string(encrypted_message_bits)
print("Encrypted message (string):", message)
print("Encrypted message (binary):", ''.join(map(str, encrypted_message_bits)))
````
## **Pasul 8**

### *<span style="color: HotPink ">Decodarea folosește aceleași chei, dar în ordine inversă*

````
decrypted_message_bits = []
for i in range(0, len(encrypted_message_bits), 64):
    block = encrypted_message_bits[i:i + 64]
    decrypted_message_bits.extend(des_decrypt(block, subkeys, ip, ip_inv, e, s_boxes, p))

decrypted_message = bits_to_string(decrypted_message_bits).rstrip('\x00')  # Remove padding
print("Decrypted message:", decrypted_message)
````
## **Pasul 9**

### *<span style="color: HotPink ">Gata! Prin aplicarea decodării, ne primim mesajul înapoi*



