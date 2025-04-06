clauses = [
    [1],
    [1,2],
    [1,2,3,],
    [1,2,3,4],
    [1,2]
]
new_literal = 849

def literal_to_str(lit):
    var = chr(ord('a') + abs(lit) - 1) 
    return f"¬{var}" if lit < 0 else var

clauses_3SAT = []

for clause in clauses:
    k = len(clause)
    # Introduce two variables and ensure their assignment has no effect on satisfiability through 4 clauses of each combination
    if k == 1:
        for a in [1, -1]:
            for b in [1, -1]:
                clauses_3SAT.append([clause[0], a * new_literal, b * (new_literal + 1)])
        new_literal += 2
    
    # Introduce a variable and ensure their assignment has no effect on satisfiability through a clause for both its value and negation
    elif k == 2:
        clauses_3SAT.append([clause[0], clause[1], new_literal])
        clauses_3SAT.append([clause[0], clause[1], -new_literal])
        new_literal += 1
    
    # Case already satisfied
    elif k == 3:
        clauses_3SAT.append(clause)

    # Progressively split clause
    elif k > 3:
        for i in range(k-3):
            if i == 0:
                clauses_3SAT.append([clause[i], clause[i+1], new_literal])
            else:
                clauses_3SAT.append([-(new_literal-1), clause[i+1], new_literal])
            
            new_literal += 1
        clauses_3SAT.append([-(new_literal-1), clause[-2], clause[-1]])

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

