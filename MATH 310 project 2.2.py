import random
import locale

def main():
    #csv with mortality rates for ages 0-119. No labels.
    #format: "Male prob, Female prob \n"
    file = "mortalityrates.csv"
    prob_file = open(file, "r")
    prob = prob_file.readlines()
    locale.setlocale(locale.LC_ALL, '')
    print("Welcome to the annual premium calculator!")
    print("Determine the annual premium each policy holder should pay for "
          + "your insurance company to break even.")

    finished = False
    while not finished:
        policy, cumdead = get_data(prob)
        premium, net = optimize(policy, cumdead)
        print("The annual premium for this policy holder should be " +
              locale.currency(premium, grouping=True)+ ".")
        print("At this rate, the profit per policy holder would be around "+
              locale.currency(net, grouping=True)+ ".")
        done = input("Would you like to look at another policy? ")
        if done[0].lower() == "n":
            print("Thank you for using the annual premium calculator!")
            finished = True

def get_data(prob):    
    #Male = 0, Female = 1
    sex = None
    while sex == None:
        sex_input = input("Enter the sex (M/F) of the policy holder: ")
        if sex_input[0].lower() == "m":
            sex = 0
        elif sex_input[0].lower() == "f":
            sex = 1
    age = "NO"
    while not age.isdigit():
        age = input("Enter the integer age of the policy holder: ")
        if age.isdigit() and (( sex == 1 and int(age) > 93) or
                              (sex == 0 and int(age) > 92)):
            print("Not a valid age")
            age = "NO"
    age = int(age)
    policy = []
    cum_dead = [0]
    i = 0
    dead = 0
    while i < 20:
        policy.append(float(prob[age + i].split(",")[sex]))
        dead += float(prob[age + i].split(",")[sex])
        cum_dead.append(dead)
        i += 1
    return (policy, cum_dead)

def optimize(policy, cum_dead):
    premium = (sum(policy) * 100000)/20
    finished = False
    i = 0
    while not finished:
        net = test_premium(premium, policy, cum_dead)
        if net < .19 and net > 0:
            finished = True
        elif net < 0:
            premium += .01
        else:
            premium -= .01
    return (premium, net)

def test_premium(premium, policy, cum_dead):
    net = 0
    for i in range(len(policy)):
        net += (premium * (1-cum_dead[i]))
    net -= cum_dead[-1] * 100000
    return net

main()







    



