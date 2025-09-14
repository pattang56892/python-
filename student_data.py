import pandas as pd

# Create Series with student data
id = pd.Series([1, 2, 3, 4, 5])
name = pd.Series(['Tom', 'Bob', 'Jary', 'Mary', 'Kim'])
score = pd.Series([78, 86, 66, 92, 70])
age = pd.Series([20, 23, 21, 19, 18])

# Create DataFrame - Method 1: Using dictionary with default index
student = pd.DataFrame({
    'name': name,
    'age': age,
    'score': score
})

print("Method 1 - Default index (0-4):")
print(student)
print()

# Create DataFrame - Method 2: Using dictionary with custom index
student_custom = pd.DataFrame({
    'name': name,
    'age': age,
    'score': score
}, index=[1, 2, 3, 4, 5])  # Now matches the data length

print("Method 2 - Custom index (1-5):")
print(student_custom)
print()

# Create DataFrame - Method 3: Including ID as a column
student_with_id = pd.DataFrame({
    'id': id,
    'name': name,
    'age': age,
    'score': score
})

print("Method 3 - With ID column:")
print(student_with_id)