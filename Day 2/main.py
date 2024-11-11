##Mathematics
print("Welcome to the tip calculator")
bill = float(input("What was the total bill? $"))
tip = int(input("What percentage tip would you like to give? 10, 12, or 15? "))
split = int(input("How many people to split the bill? "))

total_amount = bill + (bill * tip / 100)
per_each = round(total_amount/split,2)

print(f"You total bill amount is {total_amount}.With each giving {per_each}")