import sys
from collections import Counter

def mode(y_list):
    c = Counter(y_list)
    most_common = c.most_common(1)
    result = most_common[0][0]
    contador = most_common[0][1] / len(y_list)
    print([int(result),int(contador)])
    
#print(sys.argv[1:])
data_input = str(sys.argv[1:])
data_input = data_input.replace("[",'')
data_input = data_input.replace("]",'')
data_input = data_input.replace("'",'')
data_input = data_input.replace(" ",'')
data_list = list(data_input.split(','))
mode(data_list)