import sys
from collections import Counter

my_list = sys.argv[1].split(",")
numbers = [ int(x) for x in my_list ]
c = Counter(numbers)
print(c.most_common(1))

