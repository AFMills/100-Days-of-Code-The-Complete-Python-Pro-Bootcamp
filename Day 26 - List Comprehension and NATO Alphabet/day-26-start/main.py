# # List Comprehension
# numbers = [1, 2, 3]
# new_numbers = [n + 1 for n in numbers]
# print(new_numbers)

# name = "Angela"
# letters_list = [letter for letter in name]
# print(letters_list)

# range_list = [num * 2 for num in range(1, 5)]
# print(range_list)

# # Conditional List Comprehension
# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
# short_names = [name for name in names if len(name) < 5]
# long_names = [name.upper() for name in names if len(name) >= 5]
# # print(short_names)
# print(long_names)

# # Dictionary Comprehension
# import random
# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
# student_scores = {student:random.randint(1,100) for student in names}
#
# passed_students = {student:score for (student, score) in student_scores.items() if score >= 60}
# print(passed_students)

student_dict = {
    "student" : ["Angela", "James", "Lily"],
    "score" : [56, 76, 98]
}

# for (key, value) in student_dict.items():
#     print(value)

import pandas

student_data_frame = pandas.DataFrame(student_dict)
# print(student_data_frame)

# # Loop Through a Data Frame
# for (key, value) in student_data_frame.items():
#     print(value)

# Loop through the rows of a Data Frame
for (index, row) in student_data_frame.iterrows():
    # print(row.student)
    if row.student == "Angela":
        print(row.score)