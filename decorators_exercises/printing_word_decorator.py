def print_words_before_and_after(func):
    def wrapper():
        print("My name is before function!")
        func()
        print("My name is after function!")
    return wrapper


@print_words_before_and_after
def some_random_function():
    print("My name is during function and I can only be printed if the original function is running!!")#



some_random_function()
