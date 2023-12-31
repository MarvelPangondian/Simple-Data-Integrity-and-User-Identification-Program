import hashlib
import json
import random
from sympy import *
from art import *
from miscellaneous import *

global ob 
ob = {}


def gcd(num1,num2):
    if (num1 == 0 or num2 == 0): 
        return 0
    if (num1 == num2):
        return num1
    if (num1 > num2):
        return gcd(num1 - num2, num2)
    return gcd(num1,num2 - num1)

def generate_random_prime():
    num = random.randint(500,1000)
    while (not (isprime(num))):
        num = random.randint(500,1000)
    return num

def is_coprime(num1,num2):
    return (gcd(num1,num2) == 1)

# generates encryption key from modulus and phi_n
def generate_e_key(n,phi_n):
    e = random.randint(2,(phi_n)//2)
    while not (is_coprime(e,n) and is_coprime(e,phi_n) ):
        e = random.randint(2,(phi_n)//2)
    if (e > pow(e, -1, phi_n)):
        return generate_e_key(n,phi_n)
    return e

# creates decryption key from encryption key
def generate_d_key(e, phi_n):
    d = pow(e, -1, phi_n)
    return d

def generate_random_key():
    
    #generate random prime numbers
    p = generate_random_prime()
    q = p
    while (q  == p):
        q = generate_random_prime()

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

# verification functions 
def verify_password(username,password, signature,modulus,private_key, public_key):

    # Hash the provided password with SHA-256
    hashed_password = int(hashlib.sha256((username + password).encode()).hexdigest(), 16)       

    # Ensure the hashed password is within the range of n
    hashed_password = hashed_password % modulus

    # Verification
    verified_password1 = pow(signature, public_key, modulus)
    verified_password2 = pow(hashed_password, private_key, modulus)

    return (verified_password1 == hashed_password) and (verified_password2 == signature)


def verify_content(text,signature):
    hashed_text = int(hashlib.sha256(text.encode()).hexdigest(), 16)
    hashed_text = hashed_text % modulus

    # verification 
    verified_text = pow(signature, public_key, modulus)

    return (verified_text == hashed_text)


# Encryption function
def encryption_message():
    n,d = modulus,private_key

    # encrpytion text
    print(" Encryption ".center(50,"="))
    text = input("Enter your log : ")
    text_enc = encryption_rsa(modulus,public_key,text)
    text_enc = [text_enc]
    
    print()
    # creating signature to ensure integrity 
    hash_message = int(hashlib.sha256(text.encode()).hexdigest(), 16)
    hash_message = hash_message % n # making sure hash is within range of n
    signature_text = pow(hash_message, d, n)
    
    # adding signature to data
    text_enc.append(signature_text)

    ob["data"].append(text_enc)
    print("Encryption successful !")

def encryption_rsa(modulus,public,message):
    ciphertext = [pow(ord(char), public, modulus) for char in message]
    text_enc = ""
    for i in ciphertext:
        text_enc = text_enc + str('{:06}'.format(i)) # pad zero
    
    return text_enc

def decryption_message():
    print(" Decryption  ".center(50,"="))
    arr_text = ob["data"]
    if (arr_text != []):
        k = len(arr_text)
        selection = int(input(f"Select entry ({k} entries) : "))
        while (selection < 1 or selection > k):
            print("Please enter the correct entry !")
            selection = int(input(f"Select entry ({k} entries) : "))


        dec_text = decryption_rsa(modulus,private_key,arr_text[selection - 1][0])

        # verify content 
        if (not verify_content(dec_text,arr_text[selection - 1][-1])):
            print_with_color("WARNING, DATA INTEGRITY HAS BEEN COMPROMISED!\n",91)
            print("CORRUPTED TEXT : ")
            print(dec_text)
        else:
            print("Decrypted Text : ")
            print(dec_text)
    else:
        print("Data is empty")

def decryption_rsa(modulus,private,enc_message):
    message = enc_message
    message_parsed  = []
    message_arr = []
    i = 0
    while i < int(len(message)):
        if ((i + 6) > int(len(message)) ):
            # do nothing, possible corrupted text
            pass
        else:
            if (message[i:i+6].isnumeric()):
                message_parsed.append(message[i:i+6])
            else:
                pass
        i += 6
    for i in range (len(message_parsed)):
        try:
            message_arr.append(int(message_parsed[i]))
        except ValueError:
            raise ValueError("empty...")
    decoded_message = ''
    for char in message_arr:
        decrypted_char = pow(char, private, modulus)
        decoded_message += chr(decrypted_char % 128)
    return decoded_message
    

def load_database():
    with open("./database/data.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def save_database():
    data = load_database()
    data[ob["id"]] = ob
    json_object = json.dumps(data, indent=4)
    with open("./database/data.json", "w") as outfile:
        outfile.write(json_object)


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
    print(" login  ".center(50,"="))

    data = load_database()
    username = input("Enter username     : ")
    username_hash = int(hashlib.sha256(username.encode()).hexdigest(), 16)
    dict_data = {}
    for ob in data :
        if (ob["username"] == username_hash):
            dict_data = ob

    if not(bool(dict_data)):
        print("That username doesn't exist")
        username = ""
        return
    
    password_temp =     input("input password     : ")
    private_temp =  int(input("Input private key  : "))
    public_temp =   int(input("Input public key   : "))
    modulus_temp =  int(input("modulus            : "))

    if (verify_password(username,password_temp,dict_data["signature"],modulus_temp,private_temp,public_temp)):
        print_with_color("Success !",92)
        print()
        password = password_temp
        modulus = modulus_temp
        private_key = private_temp
        public_key = public_temp
        ob = dict_data
        has_login = 1

    else:
        print_with_color("verification failed\n",91)
        logout_and_init()

def logout_and_init():
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
    if (ob != {}):
        save_database()
    ob = {}


def signing():
    print(" Sign Up  ".center(50,"="))
    # loading data
    data = load_database()
    usernames = [ob["username"] for ob in data]

    username = input("Enter username   : ")
    username_hash = int(hashlib.sha256(username.encode()).hexdigest(), 16)
    while (username_hash in usernames):
        print("That username has already been taken, please enter a new username")
        username = input("Enter username   : ")
        username_hash = int(hashlib.sha256(username.encode()).hexdigest(), 16)

    password = input("Enter password   : ")

    keys = generate_random_key()
    n,e,d = keys
    signature = generate_signature(username,password,n,d)

    print()
    print("Generating keys....")
    print("Private key (d)  :",str(d))
    print("Public key (e)   :",str(e))
    print("Modulus          :",str(n))
    print()
    print("Please remember the keys generated to encrypt and decrypt in the future")

    print("To use features, please login to account")


    # updating data
    data.extend([{"id":len(data),"username" : username_hash,"signature":signature,"data":[]}])
    json_object = json.dumps(data, indent=4)
    with open("./database/data.json", "w") as outfile:
        outfile.write(json_object)
    




def main_menu():
    print(" main menu ".center(50,"=") )
    global user_input
    user_input = 0
    print("1.Login")
    print("2.Logout")
    print("3.Sign up")
    print("4.Encryption")
    print("5.Decryption")
    print("6.End program")

    user_input = int(input("Choice : "))

    while (user_input < 1 or user_input > 6):
        print("Input invalid ! \n")
        user_input = int(input("Choice : "))
    print()

if __name__ == "__main__":
    tprint("identification program")
    print()
    logout_and_init()
    while not(done):
        main_menu()

        if (user_input == 1):
            if (has_login == 1):
                print("Please logout first")
            else:
                login()
        elif (user_input == 2):
            if (has_login == 1):
                logout_and_init()
                print("logout successful !")
            else:
                print("You're not in any account right now")
        elif (user_input == 3):
            if (not has_login == 1):
                signing()
            else:
                print("You're already in an account...")
    
        elif (user_input == 4):
            if (has_login == 1):
                encryption_message()
            else:
                print("You're not in any account right now")
        elif (user_input == 5):
            if (has_login == 1):
                decryption_message()
            else:
                print("You're not in any account right now")
        elif (user_input == 6):
            done = 1
            print(" THANK YOU !  ".center(50,"="))
            if (ob  != {}):
                save_database()
        print()

