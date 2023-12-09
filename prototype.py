def decryption_rsa(modulus, private, enc_message):
    decoded_message = ''
    for char in enc_message:
        decrypted_char = pow(char, private, modulus)
        # Ensure the decrypted character is within the valid ASCII range
        decoded_message += chr(decrypted_char % 128)
    return decoded_message

# Example usage:
modulus = 3233  # Replace with your actual modulus
private_key = 2753  # Replace with your actual private key

# Encrypted message (using a simple example)
encrypted_message = [2462, 2344, 23, 2462536456, 2455]

# Decrypt the message
decrypted_message = decryption_rsa(modulus, private_key, encrypted_message)
print(f"Decrypted message: {decrypted_message}")