print("============ STUDENT GRADE CALCULATOR SYSTEM ========")

name = input("Hi, Enter your full name:  ")


maths = int(input("Enter Maths score: "))
english = int(input("Enter English score: "))
physics = int(input("Enter Physics score: "))

total = maths + english + physics
average = total / 3


#Introduce if statement
if average >= 90:
    grade = "A+"
elif average >= 80:
    grade = "A"
elif average >= 70:
    grade = "B"
elif average >= 60:
    grade = "C"
elif average >= 50:
    grade = "D"
else:
    grade = "F"

if average >= 50:
    status = "PASS"
else:
    status = "FAIL"


print()
print("======STUDENTS RESULTS ========")
print("Student's Name:", name)
print("Mathematics:", maths)
print("English:", english)
print("Physics:", maths)
print("Total:", total)
#print("Average: ", average)

print("Average:", round(average, 2))

print("Here is your Grade: ", grade)
print("Status:", status)
