"""
    ...
"""

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
    # This tuple is (dist, dist, last node). 2nd dist is used to help find smallest
    #   tentative distance
    dist = [[999999, 999999, -1] for nodes in unvisited]
    dist[source] = [0, 0, -1]
    path = []           # stores the computed path from source to node

    while unvisited or target in unvisited:
        # compute the distance to travel to each neighbour node
        for neighbour in graph[current]:
            if dist[current][0] + 1 < dist[neighbour][0]:
                dist[neighbour][0] = dist[current][0] + 1
                dist[neighbour][1] = dist[current][0] + 1
                dist[neighbour][2] = current

        unvisited.remove(current)  # remove the current node from unvisited set

        # select the next node with smallest distance. small_dist stores the index
        dist[current][1] = 0
        small_dist = dist.index(min(dist, key=lambda x: x[1] if x[1] > 0 else float('inf')))
        current = small_dist       # update the current node

    if dist[target][2] < 0:
        # no path found
        return -1

    # find the computed path
    node = target
    path.append(node)
    while len(path) <= dist[target][0]:
        node = dist[node][2]
        path.append(node)

    return (path, dist[target][0])
