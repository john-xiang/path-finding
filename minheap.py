"""
    The path-finding algorithms rely on the a priority queue to make the search more efficient.
    A priority queue is an extention of a regular queue where each element has a priority score
    and is released based on priority. This will be done with a min-heap which is a complete
    binary tree where the parent node is <= the two children nodes. Implementation based from
    https://bradfieldcs.com/algos/trees/priority-queues-with-binary-heaps/

"""

class MinHeap:
    """
    MinHeap class will contain the following methods
        Constructor() - initializes an empty binary heap
        insert(node) - inserts node into the heap
        find_min() - returns the minimum value in the heap
        extract_min() - returns the minimum value in the heap and removes it
        is_empty() - returns true if heap is empty otherwise return false
        size() - returns the size of the heap
        build_heap(list) - builds a new heap from a list
    """
    def __init__(self):
        self.heap = [0]

    def __len__(self):
        """
        Returns the size of the heap.
        There is a -1 because of the extra 0 at 0th index
        """
        return len(self.heap) - 1

    def items(self):
        """
        Returns the keys in the heap
        """
        return self.heap

    def decrease_key(self, index, new_key):
        """
        Modifies the key at specified index in the heap
        """
        self.heap[index] = new_key  # modify the key
        self.heapify_up(index)      # fix the heap structure

    def heapify_up(self, index):
        """
        Fixes the heap structure after inserting. This ensures that the
        min heap structure is kept (the parent node is smaller than
        both children nodes)
        """
        while index // 2 > 0:
            if self.heap[index] < self.heap[index // 2]:
                # if child is smaller than parent then we swap positions
                #   position at index is child
                #   position at index // 2 is parent
                self.heap[index // 2], self.heap[index] = \
                    self.heap[index], self.heap[index // 2]
            index //= 2     # check the parent node next

    def heapify_down(self, index):
        """
        Fixes the heap structure after extraction.
        """
        while index * 2 <= len(self):
            # Find the child with minimum value
            left_child = index * 2
            right_child = index * 2 + 1
            min_child = None
            if right_child > len(self) or \
                self.heap[left_child] < self.heap[right_child]:
                min_child = left_child
            else:
                min_child = right_child

            # If the minimum children is smaller than parent, then swap places
            if self.heap[index] > self.heap[min_child]:
                self.heap[index], self.heap[min_child] = \
                    self.heap[min_child], self.heap[index]

            index = min_child

    def insert(self, node):
        """
        Inserts a node into the heap.
        """
        self.heap.append(node)
        self.heapify_up(len(self))

    def find_min(self):
        """
        returns the minimum of the heap (first element)
        """
        return self.heap[1]

    def extract_min(self):
        """
        returns the node with minimum value (root node).

        puts the last element in the heap to the min spot and
        swaps with its new children nodes until the heap structure
        is satisfied again.
        """
        min_value = self.heap[1]
        # move the last element to the root
        self.heap[1] = self.heap[len(self)]
        # heapify
        self.heap.pop()
        self.heapify_down(1)

        return min_value

    def build_heap(self, array):
        """
        Converts an array into a min heap
        """
        index = len(array) // 2
        self.heap[1::] = array

        # heapify
        while index > 0:
            self.heapify_down(index)
            index -= 1
