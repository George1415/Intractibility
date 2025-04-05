clauses = [
    [1, 2, 3, 4, 5, 6]
]
new_literal = 849

def literal_to_str(lit):
    var = chr(ord('a') + abs(lit) - 1) 
    return f"¬{var}" if lit < 0 else var

clauses_3SAT = []

for clause in clauses:
    k = len(clause)
    if k > 3:
        for i in range(k-3):
            if i == 0:
                clauses_3SAT.append([clause[i], clause[i+1], new_literal])
            else:
                clauses_3SAT.append([-(new_literal-1), clause[i+1], new_literal])
            
            new_literal += 1
        new_literal -= 1
        clauses_3SAT.append([-(new_literal), clause[-2], clause[-1]])

expression = ""        
for clause in clauses_3SAT:
    if expression == "":
        expression = "("
    else:
        expression += " ∧ ("
    for literal in clause:
        if expression[-1] == "(":
            expression += f"{literal_to_str(literal)}"
        else:
            expression += f" ∨ {literal_to_str(literal)}"
    expression += ")"
print(expression)

