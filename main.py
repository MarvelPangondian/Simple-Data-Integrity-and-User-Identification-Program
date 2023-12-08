import hashlib
import json
import random
from sympy import *


def generate_random_prime():
    num = random.randint(1000,2000) # simple random prime number
    while (not (isprime(num))):
        num = random.randint(1000,2000)
    return num


def gcd(num1,num2):
    if (num1 == 0 or num2 == 0): 
        return 0
    if (num1 == num2):
        return num1
    if (num1 > num2):
        return gcd(num1 - num2, num2)
    return gcd(num1,num2 - num1)


def is_coprime(num1,num2):
    return (gcd(num1,num2) == 1)

# generates encryption key from modulus and phi_n
def generate_e_key(n,phi_n):
    e = random.randint(2,phi_n-1)
    while not (is_coprime(e,n) and is_coprime(e,phi_n)):
        e = random.randint(2,phi_n-1)
    return e

# creates decryption key from encryption key
def generate_d_key(e, phi_n):
    d = e+1
    while (e * d) % phi_n != 1:
        d += 1
    return d

def generate_random_key():
    
    #generate random prime numbers
    p = generate_random_prime()
    q = p
    while (q  == p):
        q = generate_random_prime()


    if (q > p):
        temp = q
        q = p 
        p = temp 
    
    #generate n and phi_n
    n = p*q 
    phi_n = (p - 1) * (q - 1)

    # generating encryption key, this is the public key
    e = generate_e_key(n,phi_n)

    # generating the decryption key, this is the 
    d = generate_d_key(e,phi_n)

    return (n,e,d)


def generate_signature(username,password,modulus,private):
    n,d = modulus,private
    user_pass = username + password
    
    # hashing using sha256
    hash_user_pass = int(hashlib.sha256(user_pass.encode()).hexdigest(), 16)
    hash_user_pass = hash_user_pass % n # making sure hash is within range of n

    # signature
    signature = pow(hash_user_pass, d, n)
    
    return signature


# Encryption function

def encryption_rsa(modulus,public,message):
    ciphertext = [pow(ord(char), public, modulus) for char in message]
    return ciphertext

def decryption_rsa(modulus,private,enc_message):
    message = ''
    for char in enc_message:
        message += chr(pow(char,private,modulus))
    return message


def load_database():
    pass

def save_database():
    pass

# trying somehthing


# example of implementation
k = generate_random_key()
n,e,d = k
message = "hello nama saya adalah marvel"
mess = encryption_rsa(n,e,message)
print(mess)
dec = decryption_rsa(n,d,mess)
print(dec)



