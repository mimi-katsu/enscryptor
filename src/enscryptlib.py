"""Library to aid in encrypting and decrypting python scripts"""
import subprocess
import os
import getpass
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def get_id ():
    """generate string of host characteristics to provide a fingerprint of the device"""
    uname_out = subprocess.getoutput('uname')
    whoami_out = subprocess.getoutput('whoami')
    hostname_out = subprocess.getoutput('hostname')
    shell_type = subprocess.getoutput('echo $SHELL')
    shell_type_out = subprocess.getoutput(f'{shell_type} --version')

    identity = f'{whoami_out}-{hostname_out}-{uname_out}-{shell_type_out}'
    identity ="".join(identity.strip().replace(" ","").splitlines()).lower()
    return identity

def get_pass():
    """use get pass module to obtain user pass securely"""
    return getpass.getpass("Enter a password. Leave blank for none.")

def encrypt(text, key):
    """encrypt a file with provided key and return base64 encoded"""
    text = text.encode('utf-8')
    IV = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    encryptor = cipher.encryptor()
    # Padding the text
    padding_length = 16 - len(text) % 16
    padded_text = text + bytes([padding_length]) * padding_length
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    ciphertext = IV + ciphertext
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def decrypt(ciphertext, key):
    """decode from base64 then decrypt using provided key"""
    ciphertext = base64.b64decode(ciphertext)
    # Extract the iv (first 16 bytes) and the actual ciphertext
    IV = ciphertext[:16]
    true_cypher_text = ciphertext[16:]

    # Create a cipher object with the key and iv
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_text = decryptor.update(true_cypher_text) + decryptor.finalize()

    # Remove the padding (last byte tells us how many padding bytes were added)
    padding_length = padded_text[-1]
    unencrypted_text = padded_text[:-padding_length]
    unencrypted_text = unencrypted_text.decode()
    return unencrypted_text

def keygen(*args):
    """generate a sha-256 hash from the chosen auth methods (passwords, fingerprinting, etc)"""
    key = base64.b64encode(f'{args}'.encode("utf-8"))
    sha256_hash = hashlib.sha256()
    sha256_hash.update(key)
    key = sha256_hash.digest()
    return key
