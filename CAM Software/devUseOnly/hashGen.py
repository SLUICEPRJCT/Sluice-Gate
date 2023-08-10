import hashlib


def encrypt(text):
    # create a hash object using SHA-256 algorithm
    hash_obj = hashlib.sha256()

    # add the text to the hash object
    hash_obj.update(text.encode())

    # get the hashed value
    hashed_text = hash_obj.digest()

    # return the hashed value as a hexadecimal string
    return hashed_text.hex()


usr = input("Enter username: ")
psw = input("Enter password: ")

print(f"Username hash: {encrypt(usr)}")
print(f"Password hash: {encrypt(psw)}")