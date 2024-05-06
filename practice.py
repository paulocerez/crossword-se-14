class Human():

	def __init__(self, name, age, job):
		self.name = name
		self.age = age
		self.job = job

	def getAge(self):
		return f"{self.name} is {self.age} years old."

	
human = Human("Paulo", 24, "Student")
print(human.getAge())