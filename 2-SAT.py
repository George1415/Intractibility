from collections import defaultdict

# 2-SAT expression of the form (a ∨ b) ∧ (¬a ∨ c)
clauses = [
    [1, -2],  
    [-1, 2],  
    [1, -3],
    [-1,-2]
]

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

# Display implication graph
# for node in sorted(graph):
#     print(f"[{node}]: {graph[node]}")

