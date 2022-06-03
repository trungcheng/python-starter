employees = open("employees.txt", "r")

print(employees.read())
# return content of file
print(employees.readable())
# return true
print(employees.readline())
# return a line
print(employees.readlines())
# return an array of lines

employees.close()
