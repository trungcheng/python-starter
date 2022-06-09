from Student import Student
# import Student

# object = Student.Student
# student1 = object('John', 34, 'Business')
student1 = Student('John', 34, 'Business')

print(student1.name)  # ok
print(student1.getName())  # ok
print(student1.getAge())  # ok
print(student1.getMajor())  # ok
print(student1.walk())  # this get an error
