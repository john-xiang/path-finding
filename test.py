from collections import defaultdict

graph = defaultdict()

for i in range(10):
    for j in range(10):
        graph[i,j] = i+j

# for nodes in graph:
#     print(nodes[0], nodes[1])

width = None

if not width:
    print('inside the if')
