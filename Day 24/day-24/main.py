# with open("my_file.txt") as file:     # Opens file in read-only mode
#     contents = file.read()
#     print(contents)
# # file.close()              # If we use a with statement, we don't have to close the file

# with open("my_file.txt", mode="w") as file:         # Allows you to write to file
#     file.write("New text.")

# with open("my_file.txt", mode="a") as file:           # Allows you to append to file
#     file.write("\nNew text.")

# with open("new_file.txt", mode="w") as file:            # Creates a new file in the current directory
#     file.write("New text.")


# Absolute File Path
with open("/Users/afmil/Desktop/my_file.txt") as file:
    contents = file.read()
    print(contents)

# Relative File Path
with open("../../../../Desktop/my_file.txt") as file:
    contents = file.read()
    print(contents)