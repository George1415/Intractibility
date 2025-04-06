def sat3_to_3dm(clauses):
    X, Y, Z = set(), set(), set()
    triples = []

    var_ids = set(abs(lit) for clause in clauses for lit in clause)
    var_ids = sorted(var_ids)

    # Track elements to ensure uniqueness
    id_counter = 1
    def fresh(prefix):
        nonlocal id_counter
        name = f"{prefix}{id_counter}"
        id_counter += 1
        return name

    # Variable gadgets
    var_to_gadgets = {}
    for var in var_ids:
        # Two options: true or false
        # Create elements and triples for each assignment
        x_true = fresh(f"x{var}_T")
        y_true = fresh(f"y{var}_T")
        z_true = fresh(f"z{var}_T")
        triples.append((x_true, y_true, z_true))
        
        x_false = fresh(f"x{var}_F")
        y_false = fresh(f"y{var}_F")
        z_false = fresh(f"z{var}_F")
        triples.append((x_false, y_false, z_false))

        # Save gadget for reference in clauses
        var_to_gadgets[var] = {
            True: (x_true, y_true, z_true),
            False: (x_false, y_false, z_false)
        }

        X.update([x_true, x_false])
        Y.update([y_true, y_false])
        Z.update([z_true, z_false])

    # Clause gadgets
    for idx, clause in enumerate(clauses):
        clause_tag = f"C{idx+1}"

        matched = False
        for lit in clause:
            var = abs(lit)
            is_positive = lit > 0
            x, y, z = var_to_gadgets[var][is_positive]

            # Create unique clause projection
            cx = fresh(f"{clause_tag}_x")
            cy = fresh(f"{clause_tag}_y")
            cz = fresh(f"{clause_tag}_z")
            triples.append((cx, cy, cz))
            triples.append((x, cy, cz))  # Connect to variable match

            X.add(cx)
            Y.add(cy)
            Z.add(cz)

    # Padding/fillers to equalize X, Y, Z
    while len(X) < len(Y) or len(X) < len(Z):
        fx, fy, fz = fresh("fx"), fresh("fy"), fresh("fz")
        X.add(fx)
        Y.add(fy)
        Z.add(fz)
        triples.append((fx, fy, fz))

    return {
        "X": list(X),
        "Y": list(Y),
        "Z": list(Z),
        "triples": triples
    }


# Example: 3-SAT formula with 2 clauses
clauses = [
    [1]
    # [1, -2, 3],   # x1 ∨ ¬x2 ∨ x3
    # [-1, 2, -3]   # ¬x1 ∨ x2 ∨ ¬x3
]

instance = sat3_to_3dm(clauses)

print("X =", instance["X"])
print("Y =", instance["Y"])
print("Z =", instance["Z"])
print("Triples:")
for t in instance["triples"]:
    print("  ", t)
