# 42_a_maze_ing

We use two algorythm:
- Depth-First Search (DFS) backtracking algorithm: The algorithm begins at the root node and explores deeper into the tree until it reaches a leaf node. Then, it backtracks up the tree until it finds an unexplored child node. This process continues until the desired node is found or all nodes have been explored. We've implemented the iterative version. We maintain a stack of references to unexplored siblings of the nodes we have already accessed.