print("Welcome to land of mysterious magical land of fairy pythons")

height = int(input("What is your height? "))


## check for height first

if height >= 120:
  print("You are tall enough to ride the fairy python!")
  age = int(input("What is your age ? "))
  if age > 18:
    print("You will be charge 12$ for this ride")
  elif age >= 12 and age <= 18:
    print("You will be charge 7$ for this ride")
  else:
    print("You will be charge 5$ for this ride")
else:
  print("Sorry You Cant Ride")
