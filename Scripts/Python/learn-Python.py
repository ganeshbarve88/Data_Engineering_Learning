def check_age(age):
    if age < 18:
        print("You are a minor.")
    elif age >= 18 and age < 65:
        print("You are an adult.")
    else:
        print("You are a senior citizen.")

if __name__ == "__main__":
    user_age = int(input("Enter your age: "))
    check_age(user_age)


###########################################

def list_demo():
    fruits = ["apple", "banana", "cherry"]
    
    print("Printing fruits:")
    for fruit in fruits:
        print(f"I like {fruit}")

if __name__ == "__main__":
    list_demo()

###########################################

def countdown(n):
    while n > 0:
        print(f"Countdown: {n}")
        n -= 1
    print("Blast off!")

if __name__ == "__main__":
    countdown(5)

###########################################

def calculate_area(length, width):
    return length * width

def main():
    l = 10
    w = 5
    area = calculate_area(l, w)
    print(f"The area of a {l}x{w} rectangle is: {area}")

if __name__ == "__main__":
    main()

###########################################

def filter_numbers(data_list):
    even_numbers = []
    for num in data_list:
        if num % 2 == 0:  # Modulo operator to check for even numbers
            even_numbers.append(num)
    return even_numbers

if __name__ == "__main__":
    raw_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = filter_numbers(raw_data)
    print(f"Original: {raw_data}")
    print(f"Filtered Even Numbers: {result}")


###########################################