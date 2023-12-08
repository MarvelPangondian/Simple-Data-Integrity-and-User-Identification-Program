import hashlib
import json
import random


def generate_random_prime():
    pass

def generate_coprime(num):
    pass

def generate_random_key():
    pass


def generate_signature():
    pass

def load_database():
    pass

def save_database():
    pass



import random
import os

def generate_key_pair():
    p = 61
    q = 53

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi_n)

    # Public key: (n, e), Private key: (n, d)
    public_key = (n, e)
    private_key = (n, d)

    return private_key, public_key

def encrypt_message(message, public_key):
    n, e = public_key
    ciphertext = [pow(ord(char), e, n) for char in message]
    return ciphertext

def decrypt_message(ciphertext, private_key):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return decrypted_message

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

private_key, public_key = generate_key_pair()

# User inputs message
user_message = input("Enter a message to encrypt: ")

# Encrypt the message
encrypted_message = encrypt_message(user_message, public_key)
print(f"Encrypted message: {encrypted_message}")

# Save encrypted message to a file
save_to_file(','.join(map(str, encrypted_message)), 'encrypted_message.txt')
print("Encrypted message saved to 'encrypted_message.txt'")

# Read encrypted message from file
encrypted_message_from_file = list(map(int, read_from_file('encrypted_message.txt').split(',')))

# Decrypt the message
decrypted_message = decrypt_message(encrypted_message_from_file, private_key)
print(f"Decrypted message: {decrypted_message}")
