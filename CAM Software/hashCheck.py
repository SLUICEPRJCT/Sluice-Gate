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


def login(usrName, usrPass):
    # get the hashed value of the original input
    pasHash = '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4'  # replace with the original hashed value
    usrHash = '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4'  # replace with the original hashed value

    # # get the input from the user
    # user_input = input("Enter your password: ")

    # encrypt the user input using the same technique as the original input
    hashedUsrName = encrypt(usrName)
    hashedUsrPass = encrypt(usrPass)

    # compare the hashed input with the original hashed value
    if hashedUsrPass == pasHash and hashedUsrName == usrHash:
        return "success"
    else:
        return "failed"
