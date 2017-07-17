# take in age
current_age = int(input("What's your current age?"))

retirement_age = int(input("At what age would you like to retire?"))

#take in intereste rate expectations and convert to a usable multiplier

interest_rate = 0.04

#static values
current_salary = int(input("Enter your current salary"))
percent_saved = float(input("Enter the % you want to save as a whole number"))
yearly_payments = percent_saved * current_salary
current_savings = int(input("What have you currently got in your pension pot?"))

#loop variables
loop_count = current_age
pension_pot = current_savings

while loop_count <= retirement_age:
    pension_pot +=  (pension_pot * interest_rate)
    pension_pot += yearly_payments
    # update payments for assumed inflationary rises
    yearly_payments *= 1.03
    loop_count += 1

pension_pot = int(pension_pot)
print("your pension pot will be: ")
print(pension_pot)

print("assuming inflationary pay rises")
