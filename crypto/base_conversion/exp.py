import os

dir_name = os.path.dirname(os.path.abspath(__file__))
curr_name = os.path.join(dir_name, 'file.txt')

with open(curr_name, 'r') as f:
    raw_data = f.read()

nums = raw_data.split()

result = []

for num in nums:
    if num.startswith('b'):
        value = int(num[1:], 2)
    elif num.startswith('o'):
        value = int(num[1:], 8)
    elif num.startswith('d'):
        value = int(num[1:], 10)
    elif num.startswith('x'):
        value = int(num[1:], 16)
    else:
        continue

    result.append(chr(value))

flag = "".join(result)

print(flag)