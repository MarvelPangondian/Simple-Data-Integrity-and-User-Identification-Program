import hashlib
import json
import random
from sympy import *

global username
global password
global modulus
global private_key
global public_key
global has_login
global done 
global user_input
global ob 

user_input = 0
modulus = -999
public_key = -999
private_key = -999
username = ""
password = ""
has_login = -1
done = 0
ob = {}


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
    e = random.randint(2,(phi_n)//2)
    while not (is_coprime(e,n) and is_coprime(e,phi_n) ):
        e = random.randint(2,(phi_n)//2)
    return e

# creates decryption key from encryption key
def generate_d_key(e, phi_n):
    # num = random.randint(1,10)
    # d = e*num
    # while ((e * d) % phi_n != 1):
    #     print(d)
        
    #     d += e
    #     if (d > phi_n-1):# making sure that d is within range
    #         num = random.randint(1,10)
    #         d = e*num 
    d = pow(e, -1, phi_n)
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

# verify password

def verify_password(username,password, signature,modulus,private_key, public_key):

    # Hash the provided password with SHA-256
    hashed_password = int(hashlib.sha256((username + password).encode()).hexdigest(), 16)

    # Ensure the hashed password is within the range of n
    hashed_password = hashed_password % modulus

    # Verification
    verified_password1 = pow(signature, public_key, modulus)
    verified_password2 = pow(hashed_password, private_key, modulus)

    return (verified_password1 == hashed_password) and (verified_password2 == signature)

def logout():
    global username
    global password
    global modulus
    global private_key
    global public_key
    global has_login
    global done 
    global user_input
    global ob 

    user_input = 0
    modulus = -999
    public_key = -999
    private_key = -999
    username = ""
    password = ""
    has_login = -1
    done = 0
    ob = {}

def login():
    global username
    global password
    global modulus
    global private_key
    global public_key
    global has_login
    global done 
    global user_input
    global ob

    data = load_database()
    

    username = input("Enter username : ")
    
    dict_data = {}
    for ob in data :
        if (ob["username"] == username):
            dict_data = ob

    if not(bool(dict_data)):
        print("That username doesn't exist")
        username = ""
        return
    
    password_temp = input("input password : ")
    private_temp = int(input("Input private key : "))
    public_temp = int(input("Input public key : "))
    modulus_temp = int(input("modulus : "))

    if (verify_password(username,password_temp,dict_data["signature"],modulus_temp,private_temp,public_temp)):
        print("Success !")
    else:
        print("verificaiton failed")
        logout()


def signing():
    print("=========================== Creating a new section in database ===========================")
    # loading data
    data = load_database()
    usernames = [ob["username"] for ob in data]

    username = input("Enter username : ")
    while (username in usernames):
        print("That username has already been taken, please enter a new username")
        username = input("Enter username : ")

    password = input("Enter password: ")

    keys = generate_random_key()
    n,e,d = keys
    signature = generate_signature(username,password,n,d)

    print("Generating keys....")
    print("Modulus          :",str(n))
    print("Private key (d)  :",str(d))
    print("Public key (e)   :",str(e))
    print()
    print("Please remember the keys generated to encrypt and decrypt in the future")

    print("To use features, please login to account")


    # updating data
    data.extend([{"id":len(data),"username" : username,"signature":signature,"data":[]}])
    json_object = json.dumps(data, indent=4)
    with open("./database/data.json", "w") as outfile:
        outfile.write(json_object)
    

def load_database():
    with open("./database/data.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def save_database():
    pass

# trying somehthing


# # example of implementation
# k = generate_random_key()
# print(k)
# n,e,d = k
# message = "hello nama saya adalah marvel"
# mess = encryption_rsa(n,e,message)
# print(mess)
# dec = decryption_rsa(n,d,mess)
# print(dec)


def main_menu():
    print("========================== main menu ==========================")
    global user_input
    user_input = 0
    print("1.login")
    print("2.logout")
    print("3.Encryption")
    print("4.Decryption")
    print("5.End program")

    user_input = input("Choice : ")

    while (user_input < 1 or user_input > 5):
        print("Input invalid ! \n")
        user_input = input("Choice : ")

    

if __name__ == "__main__":
    # print("Simple user identification program ")
    # print()

    # while not(done):
    #     main_menu()

    #     if (user_input == 1):
    #         if (has_login == 1):
    #             print("Please logout first")
    #         else:
    #             login()
    signing()
    login()

