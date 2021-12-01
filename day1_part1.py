# Day 1 - part 1

# Read the text file 'input/day1' and put it in a list of strings seperated by '\n'
depth_report = []
with open('input/day1_part1') as f:
    depth_report = f.read().splitlines()

# The first order of business is to figure out how quickly the depth increases.
# To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.)

increase_count = 0

for i in range(len(depth_report) - 1):
    depth = int(depth_report[i])
    next_depth = int(depth_report[i + 1])
    if depth < next_depth:
        increase_count += 1
        print('{} (increased)'.format(depth))
    elif depth > next_depth:
        print('{} (decreased)'.format(depth))
    else:
        print('{} (no change)'.format(depth))

print(increase_count)