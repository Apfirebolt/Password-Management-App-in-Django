from cryptography.fernet import Fernet

key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)
print('Your key is : ', key.decode("utf-8").encode())

sample_string = 'Darkness Overflows'
encoded_text = cipher_suite.encrypt(str.encode(sample_string))
decoded_text = cipher_suite.decrypt(encoded_text)

print('Encoded text ', encoded_text)
print('Decoded text ', decoded_text.decode("utf-8") )