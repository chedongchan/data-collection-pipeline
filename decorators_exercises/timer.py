import time
def timer(func):
    def wrapper(*arg):
        start_time = time.time()
        func(*arg)
        time.sleep(2)
        time_taken = time.time()- start_time
        print(f"It took {time_taken} seconds to complete the function")
    return wrapper


@timer
def my_random_function(some_number1, some_number2):
    return int(some_number1) - int(some_number2)


my_random_function(1,2)
