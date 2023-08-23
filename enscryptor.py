############################################################################################################
#
# Only use in the same directory as your main script or else it can travel elsewhere and overwrite something!
# for example with ../../../../../../myscript.py 
#############################################################################################################


import subprocess
import sys
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def get_id ():
    uname_out = subprocess.getoutput('uname')
    whoami_out = subprocess.getoutput('whoami')
    hostname_out = subprocess.getoutput('hostname')
    shell_type = subprocess.getoutput('echo $SHELL')
    shell_type_out = subprocess.getoutput(f'{shell_type} --version')

    identity = f'{whoami_out}-{hostname_out}-{uname_out}-{shell_type_out}'
    identity ="".join(identity.strip().replace(" ","").splitlines()).lower()
    return identity

def get_pass():
    return input("Password: (Leave blank for no password)\n")


def encrypt(text, key):
    text = text.encode('utf-8')
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    # Padding the text
    padding_length = 16 - len(text) % 16
    padded_text = text + bytes([padding_length]) * padding_length
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    return iv + ciphertext

def decrypt(ciphertext, key):
    # Extract the IV (first 16 bytes) and the actual ciphertext
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]

    # Create a cipher object with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_text = decryptor.update(actual_ciphertext) + decryptor.finalize()

    # Remove the padding (last byte tells us how many padding bytes were added)
    padding_length = padded_text[-1]
    original_text = padded_text[:-padding_length]

    return original_text    
    
def key():
    key = base64.b64encode(f'{get_pass()}{get_id()}'.encode("utf-8"))
    sha256_hash = hashlib.sha256()
    sha256_hash.update(key)
    key = sha256_hash.digest()
    return key

if not os.path.exists("./dist"):
    os.mkdir("dist")
    print("Creating /dist directory...")
else:
    print("Directory /dist already exists...")

file = sys.argv[1]

print("Generating encyption key...")
key = key()

with open(f'{file}', "r") as f:
    text_to_encrypt = f.read()
    print("Encrypting...")
    encrypt_script = base64.b64encode(encrypt(text_to_encrypt, key)).decode()
    with open(f'./dist/stewed-{file}', "w") as stew:
        with open("./src/decrypt.txt", "r") as dec:
            content = dec.read()
            print(f'Writing {stew.name} to file...')
            content = content.replace("ENCRYPTED_SCRIPT", f'{encrypt_script}')
            stew.write(content)
            print("All done!")









