import hashlib
import string
import pyautogui
import random
from datetime import datetime


def check_length_psw():
    global length_of_searched_psw, found_pass, count
    while True:
        guess_pass = random.choices(string.ascii_lowercase, k=length_of_searched_psw)
        guess_concat = ''.join(guess_pass)
        if len(found_pass.keys()) == len(string.ascii_lowercase) ** length_of_searched_psw:
            return 0, 0, False

        if guess_concat in found_pass.values():
            continue
        else:
            count += 1
            found_pass[count] = guess_concat
            hashed_pwd = hashlib.md5(guess_concat.encode('utf-8')).hexdigest()

            return hashed_pwd, guess_concat, True


def check_result(hashed_psw, list_with_psw, psw):
    global count
    if hashed_psw == list_with_psw[0]:
        print(f"This password is correct !\nThe password is {psw}")
        return True

    else:
        if count % 10000 == 0:
            print(f"Decrypting....\nTotal checked passwords {count}")
        return False


pswd_list = []
cond = False
result_time = 0
count = 0
found_pass = {}

while True:

    password_input = pyautogui.password("Enter your password:")

    length_of_searched_psw = int(input("How long is the searched password?\n"))

    hash = hashlib.md5(password_input.encode('utf-8')).hexdigest()
    pswd_list.append(hash)

    start_time = datetime.now()
    while True:

        hashed, psw, status = check_length_psw()
        if status:
            if check_result(hashed, pswd_list, psw):
                end_time = datetime.now()
                result_time = end_time - start_time
                cond = True
                break
            else:
                continue
        elif not status:
            print(f"\nAll password with length of {length_of_searched_psw} were tested.\nNo"
                  f" password was found. Would you like to try different password length?\n"
                  f"Press 'Y' to try new length or 'N' for exit!")
            enter_user_option = input()
            if enter_user_option.lower() == "y":
                length_of_searched_psw = int(input("\nHow long is the searched password?\n"))
                start_time = datetime.now()
                found_pass.clear()
            elif enter_user_option.lower() == "n":
                end_time = datetime.now()
                result_time = end_time - start_time
                cond = True
                break

    if cond:
        break

print(f"\nTotal count {count}\nTotal time: {result_time}")