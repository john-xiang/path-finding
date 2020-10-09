"""
    ...
"""

from collections import defaultdict

# class Graph():

#     def __init__(self, graph):
#         self.graph = graph


def dijkstra(source, target, graph):
    """
        Dijkstra's algorithm finds the shortest path between a source and target node.
        The algorithm works as follows:
            1) All nodes are initially unvisited
            2) set the source node as the current node
            3) Initialize the tentative distance of the source node as 0
                all other nodes have distance of infinity
            4) While target node is unvisited
                a) compute the distance between current node and each neighbour node
                b) if computed distance is smaller than replace as current distance
                c) remove the current node from the unvisited list and continue
            5) Display result
        
        The inputs to dijkstra is source node, target node and graph.
            The graph is represented in a list such that each key is the node
            and the values of each key are the neighbours
    """

    current = source
    unvisited = list(graph)
    dist = [999999 for nodes in unvisited]
    dist[source] = 0
    dist_ = dist.copy() # helps find the smallest tenative distance of unvisited nodes
    path = []

    while not unvisited or target in unvisited:
        # compute the distance to travel to each neighbour node
        for neighbours in graph[current]:
            if dist[current] + 1 < dist[neighbours]:
                dist[neighbours] = dist[current] + 1
                dist_[neighbours] = dist[current] + 1

        unvisited.remove(current) # remove the current node from unvisited set
        path.append(current)      # append the current node to the path

        # select the next node with smallest distance [returns (position, value)]
        dist_[current] = 0
        small_dist = min(enumerate(dist_), key=lambda x: x[1] if x[1] > 0 else float('inf'))
        current = small_dist[0]     # update the current node

    print(path)

def main():
    """
        ...
    """
    g = defaultdict(list)

    g[0] = [3, 1, 12]
    g[1] = [0, 3, 7, 12]
    g[2] = [11, 12]
    g[3] = [0, 1, 5]
    g[4] = [6, 10]
    g[5] = [3, 7]
    g[6] = [4, 7]
    g[7] = [2, 5, 6]
    g[8] = [9, 10, 11]
    g[9] = [8, 10, 11]
    g[10] = [4, 8, 9]
    g[11] = [2, 8, 9]
    g[12] = [0, 1, 2]

    dijkstra(4, 12, g)


if __name__ == "__main__":
    main()
