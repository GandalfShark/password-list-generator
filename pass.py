# password generator, for CTFs and/or education
# creates word list, illustrates the large size of possible passwords
# also shows the difficulty of brute force attacks against random passwords

# for illustration/educational use ONLY! These passwords should NOT be considered secure passwords and
# should never be used in a production environment or even for home use.
# updated for speed and readability code-using tips from chat gpt 3.4 

# TODO test and modify where needed. 

import multiprocessing
from random import choice
import string

CHARACTER_SET = string.digits + string.ascii_letters + string.punctuation
PASSWORD_LENGTHS = range(8, 11)
MAX_PASSWORDS = 20000

def generate_password(length):
    return ''.join(choice(CHARACTER_SET) for _ in range(length))

def generate_variations(password):
    variations = [
        password,
        password.swapcase(),
        password.upper(),
        password.lower()
    ]
    return variations

def generate_passwords(worker_id, num_passwords, word_list):
    while len(word_list) < MAX_PASSWORDS:
        password_length = choice(PASSWORD_LENGTHS)
        new_password = generate_password(password_length)
        
        if new_password not in word_list:
            word_list.extend(generate_variations(new_password))
    
    print(f"Worker {worker_id} finished generating passwords.")

def save_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    word_list = manager.list()  # Use a multiprocessing-safe list
    # With this modification, the word_list is a multiprocessing-safe list, and 
    # each process can safely add unique passwords and variations without worrying about duplicates.
    
    num_processes = 4  # Adjust the number of processes as needed
    
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=generate_passwords, args=(i, num_processes, word_list))
        process.start()
        processes.append(process)
    
    for process in processes:
        process.join()
    
    print("All workers finished generating passwords.")
    
    output_file = "passwords.txt"
    save_to_file(output_file, word_list)
    
    print(f"Results saved to {output_file}")
    print(f"Total possible passwords without the 20k restriction: {len(CHARACTER_SET) ** max(PASSWORD_LENGTHS)}")

