# # FileNotFound Error
# with open("a_file.txt") as file:
#     file.read()

# # Key Error
# a_dictionary = {"key":"value"}
# value = a_dictionary["non_existent-key"]

# # Index Error
# fruit_list = ["Apple", "Banana", "Pear"]
# fruit = fruit_list[3]

# # Type Error
# text = "abc"
# print(text + 5)

# try:
#     file = open("a_file.txt")
#     a_dictionary = {"key": "value"}
#     # value = a_dictionary["non_existent_key"]
#     print(a_dictionary["key"])
# except FileNotFoundError:
#     file = open("a_file.txt", "w")
#     file.write("Something")
# except KeyError as error_message:
#     print(f"The key {error_message} does not exist")
# else:
#     content = file.read()
#     print(content)
# finally:
#     # file.close()
#     # print("File was closed.")
#     raise TypeError("This is an error that I made up.")                      # Raise an error of your choosing


height = float(input("Height: "))
weight = float(input("Weight: "))

if height > 3:
    raise ValueError("No one is that tall.")

bmi = weight / height ** 2
print(bmi)