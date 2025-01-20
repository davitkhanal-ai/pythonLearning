# ## Random Generetor
import random
# Original list of names
people_name = [
  'Davit', 'David',
  'Rohit', 'Pooja',
  'Rabindra', 'Suman',
  'Saroj', 'Riyaz',
  'Arpan', 'Harish'
]

# Convert the list to a comma-separated string
names_string = ", ".join(people_name)
# Split the string back into a list of names
names = names_string.split(", ")
random_name = random.choice(names)
print(f"{random_name} will be paying for this time")
