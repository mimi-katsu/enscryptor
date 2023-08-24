"""Main script for Enscryptor"""
import os
import sys
sys.path.append("./src")
import enscryptlib

def main ():
    """boiler plate"""
    if not os.path.exists("./dist"):
        os.mkdir("dist")
        print("Creating /dist directory...")
    else:
        print("Directory /dist already exists...")

    FILE_PATH = sys.argv[1]

    print("Generating encryption key...")
    key = enscryptlib.keygen(enscryptlib.get_id(), enscryptlib.get_pass())

    with open("./src/enscryptlib.py", "r", encoding="utf-8") as lib:
        LIB_CONTENT = lib.read()
        with open("./dist/enscryptlib.py", "w", encoding="utf-8") as distlib:
            distlib.write(LIB_CONTENT)

    with open(f'{FILE_PATH}', "r", encoding="utf-8") as f:
        SCRIPT_TO_ENCRYPT = f.read()
        print("Encrypting...")
        ENCRYPTED_SCRIPT = enscryptlib.encrypt(SCRIPT_TO_ENCRYPT, key).decode()
        with open(f'./dist/{FILE_PATH}', "w", encoding="utf-8") as E:
            with open("./src/boilerplate.txt", "r", encoding="utf-8") as TXT:
                content = TXT.read()
                print(f'Writing {E.name} to file...')
                content = content.replace("ENCRYPTED_SCRIPT", f'{ENCRYPTED_SCRIPT}')
                E.write(content)
                print("All done!")

if __name__ == "__main__":
    main()
