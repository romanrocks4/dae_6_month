list = [12, 23, 1, 4, 61, 32, 9, 5, 2, 10]
total = 0 


for i in range(len(list)):
    for j in range(i + 1, len(list)):
        if list[i] > list[j]:
            list[i], list[j] = list[j], list[i]

    total = total + list[i]

average = total/len(list)


print("Sorted list:", list)
print("Average number:", average)
print("Minimum number:", list[0])
print("Maximum number:", list[-1])

