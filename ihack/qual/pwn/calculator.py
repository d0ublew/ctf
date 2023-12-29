# uncompyle6 version 3.8.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: calculator.py
# Compiled at: 2022-12-09 16:17:40
import sys

print(
    "Welcome to IHACK2022. \nThis python program will calculate the prime numbers up to a given number.\nPlease enter a number to be calculated"
)
sys.stdout.flush()
number = input("")
sys.stdout.flush()
number = int(number)


def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, number):
        if number % i == 0:
            return False

    return True


def print_primes(number):
    for i in range(1, number + 1):
        if is_prime(i):
            print(i)


print("The prime numbers up to", number, "are:")
sys.stdout.flush()
print_primes(number)
