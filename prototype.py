def decryption_rsa(modulus, private, enc_message):
    decoded_message = ''
    for char in enc_message:
        decrypted_char = pow(char, private, modulus)
        decoded_message += chr(decrypted_char % 128)
    return decoded_message

# Example usage:
modulus = 3233  # Replace with your actual modulus
private_key = 2753  # Replace with your actual private key

encrypted_message = [2462, 2344, 23, 2462536456, 2455]

# Decrypt the message
decrypted_message = decryption_rsa(modulus, private_key, encrypted_message)
print(f"Decrypted message: {decrypted_message}")

def encryption_rsa(modulus, public, message):
    # Convert the message to a single integer
    message_int = int.from_bytes(message.encode(), 'big')

    # Encrypt the message as a single integer
    ciphertext = pow(message_int, public, modulus)

    return ciphertext

# def decryption_rsa(modulus, private, enc_message):
#     # Decrypt the ciphertext
#     decrypted_int = pow(enc_message, private, modulus)

#     # Convert the decrypted integer back to bytes and then to a string
#     decrypted_message = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode()

#     return decrypted_message

# # Example usage
# modulus = 58991
# public_key = 17
# private_key = 40013
# original_message = "Hello, RSA!"

# # Encryption
# encrypted_data = encryption_rsa(modulus, public_key, original_message)
# print("Encrypted Data:", encrypted_data)

# # Decryption
# decrypted_data = decryption_rsa(modulus, private_key, encrypted_data)
# print("Decrypted Data:", decrypted_data)


# def decryption_rsa(modulus, private, enc_message, encoding='latin-1'):
#     # Decrypt the ciphertext
#     decrypted_int = pow(enc_message, private, modulus)

#     try:
#         # Convert the decrypted integer back to bytes and then to a string
#         decrypted_message = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode(encoding)
#         return decrypted_message
#     except UnicodeDecodeError as e:
#         print(f"Error decoding: {e}")
#         return None  # Handle the error according to your requirements

# # Example usage
# modulus = 58991
# public_key = 17
# private_key = 40013
# original_message = "Hello, RSA!"

# # Encryption
# encrypted_data = encryption_rsa(modulus, public_key, original_message)
# print("Encrypted Data:", encrypted_data)

# # Decryption
# decrypted_data = decryption_rsa(modulus, private_key, encrypted_data)
# if decrypted_data is not None:
#     print("Decrypted Data:", decrypted_data)
# else:
#     print("Decryption failed.")


def decryption_rsa(modulus, private, enc_message, encoding='utf-8'):
    # Decrypt the ciphertext
    decrypted_int = pow(enc_message, private, modulus)

    try:
        # Convert the decrypted integer back to bytes and then to a string
        decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
        decrypted_message = decrypted_bytes.decode(encoding)
        return decrypted_message
    except UnicodeDecodeError as e:
        print(f"Error decoding: {e}")
        return None  # Handle the error according to your requirements

# Example usage
modulus = 58991
public_key = 17
private_key = 40013
original_message = "Hello, RSA!"

# Encryption
encrypted_data = encryption_rsa(modulus, public_key, original_message)
print("Encrypted Data:", encrypted_data)

# Decryption
decrypted_data = decryption_rsa(modulus, private_key, encrypted_data)
if decrypted_data is not None:
    print("Decrypted Data:", decrypted_data)
else:
    print("Decryption failed.")