def chain_of_characters(func):
    def wrapper():
        x=10
        chain=[]
        string = str('*')
        for x in range(11):
            chain.append(string)
        print(''.join(chain))
        func()
        print(''.join(chain))
    return wrapper

def chain_of_characters2(func):
    def wrapper():
        x=10
        chain=[]
        string = str('%')
        for x in range(11):
            chain.append(string)
        print(''.join(chain))
        func()
        print(''.join(chain))
    return wrapper

@chain_of_characters
@chain_of_characters2
def some_function():
    print("This is a message")


some_function()