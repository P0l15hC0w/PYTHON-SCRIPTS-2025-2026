import time
import itertools

max_length = 5

while True:
    while True:
        password = input("Enter your password: ")
        if len(password) < 6:
            break
        else: print('the password cant be longer than 5 characters, try again')
    confirm_password = input("Confirm your password: ")
    if password == confirm_password :
        break
    else:
        print("Passwords do not match. Please try again.")

print('Cracking your password...')
timerbg = time.time()

chars = [chr(i) for i in range(32, 127)]

found = False
attempt = ""
attempts = 0

for length in range(1, max_length + 1):
    
    for candidate in itertools.product(chars, repeat=length):
        attempts += 1
        attempt = ''.join(candidate)
        print(attempts, "attempt:", attempt)
        if attempt == password:
            found = True
            break
    if found:
        break

if found:
    print(f"Cracked password: {attempt}")
else:
    print("Password not found within max length.")

timerend = time.time()
print(f"attempts taken: {attempts}")
print(f"Time taken to crack the password was {timerend - timerbg} seconds!")