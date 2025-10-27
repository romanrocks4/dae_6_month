# stack.py
# -----------------------------------------------------------------------------
# Your task: implement a simple Stack using a Python list.
#
# Functions to implement:
#   1. push(value)    -> put value on top of the stack
#   2. pop()          -> remove and return the top value, or None if empty
#   3. peek()         -> return the top value without removing it, or None if empty
#   4. is_empty()     -> return True if the stack has no items
#   5. size()         -> return how many items are in the stack
# -----------------------------------------------------------------------------
stack = []

def push(value):
    stack.insert(0, value)

def pop():
    num = len(stack)
    if num > 0:
        print(stack[0])
        stack.pop(0)
    else:
        print("***")

def peek():
    num = len(stack)
    if num > 0:
        print(stack[0])
    else:
        print("***")

def is_empty():
    num = len(stack)
    if num < 1:
        print("True")
    else:
        print("False")

def size():
    num = len(stack)
    print(num)

print("Hello!")

while True :

    cmd = input(">>:")

    if cmd == "push":
        value = input("Insert:")
        push(value)
    elif cmd == "pop":
        pop()
    elif cmd == "peek":
        peek()
    elif cmd == "is_empty":
        is_empty()
    elif cmd == "size":
        size()
    elif cmd == "quit":
        print("Goodbye!")
        break
    else:
        print("Invalid input...")