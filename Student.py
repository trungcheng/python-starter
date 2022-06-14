class Student:
    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getMajor(self):
        return self.major

    def walk():
        return "I'm walking!"

    def checkIsHighAge(self):
        if self.age >= 70:
            return True
        else:
            return False
