from collections import defaultdict

# 2-SAT expression of the form (a ∨ b) ∧ (¬a ∨ c)

# Satisfiable
num = 3
clauses = [
    [1, -2],  
    [-1, 2],  
    [1, -3],
    [-1,-2],
]
# Unsatisfiable
# num = 4
# clauses = [
#     [1, 2],  
#     [-1, 3],  
#     [-2, 3],
#     [-3,4],
#     [-4,1],
#     [-1,-3]
# ]

def literal_to_str(lit):
    var = chr(ord('a') + abs(lit) - 1) 
    return f"¬{var}" if lit < 0 else var

expression = ""
for a, b in clauses:
    if expression == "":
        expression = f"({literal_to_str(a)} ∨ {literal_to_str(b)}) "
    else:
        expression += f"∧ ({literal_to_str(a)} ∨ {literal_to_str(b)}) "
# Implication graph represented as an adjacency list
graph = defaultdict(list)
reversed_graph = defaultdict(list)


for a, b in clauses:
    # for a clause (a ∨ b), the implications are (¬a -> b) and (¬b ∨ a)
    graph[-a].append(b)
    graph[-b].append(a)

    # for a clause (a ∨ b), the reverse implications are (b -> ¬a) and (a ∨ ¬b)
    reversed_graph[b].append(-a)
    reversed_graph[a].append(-b)


# Kosaraju's Algorithm

visited = set()
finished_order = []

# Depth First Search on the initial graph
def dfs(node):
    visited.add(node)
    for next in graph[node]:
        if next not in visited:
            dfs(next)
    finished_order.append(node)


literals = set()
# set of all literals
for clause in clauses:
    literals.update(clause)
    literals.update([-clause[0], -clause[1]])

# Ensure nodes separate from main graph are still included
for node in literals:
    if node not in visited:
        dfs(node)


# Strongly connected component (SCC) - a group of nodes in a directed graph where every node can reach every other node
strongly_connected_component = {} # Dictionary that maps each node to the label of the SCC


# Depth First Search on the reversed graph
def dfs_reversed(node, label):
    strongly_connected_component[node] = label
    for next in reversed_graph[node]:
        if next not in strongly_connected_component:
            dfs_reversed(next, label)


for node in reversed(finished_order):
    if node not in strongly_connected_component:
        dfs_reversed(node, node)


# If literal and its negation in same SCC, then expression unsatisfiable
is_satisfiable = True
for literal in range(1, num + 1):
    if strongly_connected_component.get(literal) == strongly_connected_component.get(-literal):
        is_satisfiable = False
        break

if is_satisfiable:
    print(f"The expression {expression} is SATISFIABLE")
    assignment = {}
    for literal in range(1, num + 1):
        # By nature, each SCC are connected in only one direction
        # To avoid contradictions, we assign each variable based on whether the literal or its negation is later in the order of SSCs
        assignment[literal_to_str(literal)] = (strongly_connected_component[-literal] > strongly_connected_component[literal])
    print("The satisfying assignment is:")
    print(assignment)
else:
    print(f"The expression {expression} is UNSATISFIABLE")