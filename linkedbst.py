"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log2
from datetime import datetime
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0
        # For alphabetical sorted tree
        self.__peek = None

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            left_sum = 0
            right_sum = 0
            if top.left is not None:
                left_sum = height1(top.left)
            if top.right is not None:
                right_sum = height1(top.right)
            return max(left_sum, right_sum) + 1

        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log2(len(list(self.inorder())) + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        result = []
        for item in self.inorder():
            if low <= item <= high:
                result.append(item)
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def helper_func(items):
            if not items:
                return
            mid = len(items) // 2
            node = BSTNode(items[mid])
            node.left = helper_func(items[:mid])
            node.right = helper_func(items[mid + 1:])
            return node

        self._root = helper_func(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in self.inorder():
            if elem > item:
                return elem

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        index = 0
        items = list(self.inorder())
        while items[index] < item:
            index += 1
            if index == len(items):
                break
        return items[index - 1] if items[0] < item else None

    def __add_in_alphabetical_order(self, item):
        """
        Function to add an element to the tree sorted in alphabetical order

        Works without recursion
        """
        if not self._root:
            self._root = BSTNode(item)
            self.__peek = self._root
        node = BSTNode(item)
        self.__peek.right = node
        self.__peek = node

    def __find_in_alphabetical_order(self, item):
        """
        Function to find an element in the tree sorted in alphabetical order

        Works without recursion
        """
        temp_node = self._root
        while temp_node is not None:
            if temp_node.data == item:
                return  temp_node.data
            temp_node = temp_node.right

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        items = []
        random_items = []
        with open(path) as file:
            items = [i.replace("\n", "") for i in file.readlines()]
            random_items = random.sample(items, k=10000)
            start = datetime.now()
            for item in random_items:
                items.index(item)
            print(f"Time for searching in list: {datetime.now() - start}")
        
        for item in items:
            self.__add_in_alphabetical_order(item)

        start = datetime.now()

        for item in random_items:
            self.__find_in_alphabetical_order(item)

        print(f"Time for searching in sorted binary tree: {datetime.now() - start} ")

        self.clear()

        random.shuffle(items)

        for item in items:
            self.add(item)

        start = datetime.now()
        for random_item in random_items:
            self.find(random_item)

        print(f"Time for searching in not sorted binary tree: {datetime.now() - start}")

        self.rebalance()

        for random_item in random_items:
            start = datetime.now()
            self.find(random_item)
        print(f"Time for searching in not sorted binary tree after rebalancing: {datetime.now() - start}")

        self.clear()

tree = LinkedBST()
tree.demo_bst("words.txt")