# password generator, for CTFs and/or education
# creates word list, illustrates the large size of possible passwords
# also shows the difficulty of brute force attacks against random passwords

# for illustration/educational use ONLY! These passwords should NOT be considered secure passwords and
# should never be used in a production environment or even for home use.

import multiprocessing
from random import choice
import string
import os
from time import time

start_time = time()

CHARACTER_SET = string.digits + string.ascii_letters + string.punctuation
PASSWORD_LENGTHS = range(8, 12)
MAX_PASSWORDS = 20000
TOTAL_PROCESSES = 2
# use constants here so code can quickly be updated as needed



def generate_password(length):
    return ''.join(choice(CHARACTER_SET) for _ in range(length))
    # return a string made of a random set of 8 to 12 chars


def generate_variations(password):
    variations = [
        password,
        password.swapcase(),
        password.upper(),
        password.lower()
    ]
    return variations

# for i in range(10):
#     i = generate_password(12)
#     print(i)


def generate_passwords(worker_id, working_lock, working_word_set, working_word_list):
    # To track unique passwords within each process
    while len(working_word_list) < MAX_PASSWORDS:
        password_length = choice(PASSWORD_LENGTHS)
        new_password = generate_password(password_length)

        with working_lock:
            if new_password not in working_word_set:
                working_word_set.add(new_password)
                working_word_list.extend(generate_variations(new_password))

    print(f"Worker {worker_id} finished generating passwords.")


def save_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(f"{item}\n")


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    word_list = manager.list()

    lock = multiprocessing.Lock()
    word_set = set()
    processes = []
    for i in range(TOTAL_PROCESSES):
        n = i
        process = multiprocessing.Process(target=generate_passwords, args=(n, lock, word_set, word_list))
        process.start()
        processes.append(process)
        print('module name:', __name__)
        print('parent process:', os.getppid())
        print('process id:', os.getpid())

    for process in processes:
        process.join()

    # timing stats
    print("All workers finished generating passwords.")
    end_time = time()
    print(f'Program took {(end_time - start_time):.2f} seconds with {TOTAL_PROCESSES} processes.')

    # adjusting the output to create files each time it runs
    file_title = input('What do you want to call your password_list?')
    output_file = 'passwords_' + file_title + '.txt'
    save_to_file(output_file, word_list)
    print(f"Results saved to {output_file}")

""" 
time trials:
# of processors - seconds
5 - 0.36, 0.37, 0.33, 0.32, 0.33
4 - 0.32, 0.33, 0.34, 0.32
3 - 0.31, 0.31, 0.31, 0.31, 0.30
2 - 0.28, 0.28, 0.28, 0.29, 0.32, 0.29
1 - 0.31, 0.30, 0.29, 0.26, 0.28, 0.33
The more processors the slower it runs, :(
boo-unrs! so far 2 is the magic number... 
"""
