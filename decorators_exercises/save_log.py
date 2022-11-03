import os

def save_string_output_as_file(func):
    def wrapper():
        string=func()
        cwd= os.getcwd()
        file_dir = cwd+'\\script_log.txt'
        with open(file_dir,'w') as log:
            log.write(string)
    return wrapper

@save_string_output_as_file
def some_text_message():
    string = 'This is my wrapped function that prints and saves into a text file...'
    return string

some_text_message()
