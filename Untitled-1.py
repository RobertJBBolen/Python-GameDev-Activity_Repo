import math

def add(num1, num2):
    return num1 + num2
def subtract(num1, num2):
    return num1 + num2
def multiply(num1, num2):
    return num1 + num2
def divide(num1, num2):
    if num2 == 0:
        return "Error Cannot divide by 0"
    else :
        return num1/num2

def power(num1, num2):
    return num1 ** num2

def square_root(num1):
      if num1 < 0:
        return "Error Cannot divide by 0"
      else: 
          return math.sqrt(num1)
      
def modulo(num1, num2):
    return num1 % num2


while True:
    print("---------- Simple Calculator ----------")
    print("1. Add    2. Subtract   3. Multiply    4. Divide")
    print("5. Power  6. SquareRoot  7. Modulo")
    print("0. Exit")

    
    choice = input("Choose: ")

    match choice:
        case '0':
            print("Exit")
            break
        case '1' | '2' | '3' | '4' | '5' | '7':
            num1 = float(input("Enter First Number: "))
            num2 = float(input("Enter Second Number: "))

            match choice:
                case '1':
                    result = add(num1, num2)
                case '2':
                    result = subtract(num1, num2)
                case '3':
                    result = multiply(num1, num2)
                case '4':
                    result = divide(num1, num2)
                case '5':
                    result = power(num1, num2)
                case '7':
                    result = modulo(num1, num2)

            print("Result: ", result)
            print("-------------------------------------------")
        
        case '6':
            num1 = float(input("Enter Number: "))
            result = square_root(num1)
            print("Result: ", result)

        case _:
            print("Invalid choice")
            print("-------------------------------------------")