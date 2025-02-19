import sys
import re
import ast
import operator
import math

# Define allowed operations
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.Lt: operator.lt,
    ast.Gt: operator.gt,
    ast.LtE: operator.le,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}

# Predefined mathematical constants
PREDEFINED_VARIABLES = {
    "pi": math.pi,
    "e": math.e,
    "c": 299792458,  # Speed of light in m/s
    "g": 9.80665,  # Gravitational acceleration in m/s^2
    "h": 6.62607015e-34,  # Planck's constant in J⋅s
    "G": 6.67430e-11,  # Gravitational constant in m^3⋅kg^−1⋅s^−2
    "Na": 6.02214076e23,  # Avogadro's number
    "kb": 1.380649e-23,  # Boltzmann constant in J/K
}

def safe_eval(node, variables):
    """Safely evaluate AST nodes"""
    if isinstance(node, ast.Constant):  # Numbers (works in Python 3.8+)
        return node.value
    elif isinstance(node, ast.BinOp):  # Binary operations
        left = safe_eval(node.left, variables)
        right = safe_eval(node.right, variables)
        if type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.Compare):  # Comparisons
        left = safe_eval(node.left, variables)
        right = safe_eval(node.comparators[0], variables)
        if type(node.ops[0]) in SAFE_OPERATORS:
            return int(SAFE_OPERATORS[type(node.ops[0])](left, right))
    elif isinstance(node, ast.Name):  # Variables
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    raise ValueError("Unsupported operation")

def evaluate_expression(expression, variables):
    """Safely evaluate an expression with variable substitution"""
    try:
        tree = ast.parse(expression, mode='eval')
        return safe_eval(tree.body, variables)
    except Exception as e:
        return f"Error: {e}"

def process_lines(lines):
    """Process multiple lines of input, handling variable assignments and equations."""
    variables = PREDEFINED_VARIABLES.copy()
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line or line.startswith('#'):  # Ignore empty lines and comments
            i += 1
            continue
        
        # Handle variable assignment and equations
        if '=' in line:
            var, expr = map(str.strip, line.split('=', 1))
            try:
                variables[var] = evaluate_expression(expr, variables)
            except Exception as e:
                results.append((i + 1, f"Error in equation '{line}': {e}"))
        
        # Handle if conditions
        elif line.startswith('if '):
            condition = line[3:].strip()
            if not evaluate_expression(condition, variables):
                # Skip to next non-indented line (basic skipping logic)
                while i + 1 < len(lines) and lines[i + 1].startswith('    '):
                    i += 1
        
        # Handle loops (basic while loop)
        elif line.startswith('while '):
            condition = line[6:].strip()
            loop_start = i + 1
            loop_body = []
            
            while loop_start < len(lines) and lines[loop_start].startswith('    '):
                loop_body.append(lines[loop_start][4:])  # Remove indentation
                loop_start += 1
            
            while evaluate_expression(condition, variables):
                process_lines(loop_body)
            
            i = loop_start - 1  # Adjust index to continue after loop
        
        else:
            result = evaluate_expression(line, variables)
            results.append((i + 1, result))
        
        i += 1
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: calc.py 'expression' or calc.py -f filename")
        return
    
    if sys.argv[1] == '-f':
        if len(sys.argv) < 3:
            print("Error: No file specified")
            return
        with open(sys.argv[2], 'r') as f:
            lines = f.readlines()
        results = process_lines(lines)
        print(results)
    else:
        expression = ' '.join(sys.argv[1:])
        print(evaluate_expression(expression, PREDEFINED_VARIABLES.copy()))

if __name__ == "__main__":
    main()
