import time


def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
    return wrapper_function         # Removing parentheses makes it so that the function is returned, not its output

@delay_decorator                    # Using the decorator function, we can add the functionality of the decorator to the function on the following line (i.e. say_hello())
def say_hello():
    print("Hello")

@delay_decorator
def say_bye():
    print("Bye")

def say_greeting():
    print("How are you?")

say_hello()
say_greeting()
say_bye()

decorated_function = delay_decorator(say_greeting)      # We can also call the decorator function directly to get a modified instance of the function that is being passed through it
decorated_function()

current_time = time.time()
print(current_time)  # seconds since Jan 1st, 1970
