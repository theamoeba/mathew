import sys
import re
import ast
import operator
import math
import cmath
import json

"""
Enhanced Text Calculator

Usage:
  - Run interactively: `python calc.py`
  - Evaluate an expression: `python calc.py "3 + 5 * 2"`
  - Execute from file: `python calc.py -f filename.txt`
  - Exit interactive mode: Type `exit`
"""

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
    ast.And: operator.and_,
    ast.Or: operator.or_,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
}

SAFE_FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log,
    'exp': math.exp,
    'abs': abs,
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
    'deg': math.degrees,
    'rad': math.radians,
    'factorial': math.factorial,
    'complex': complex,
}

# Predefined mathematical constants
PREDEFINED_VARIABLES = {
    "pi": math.pi,
    "e": math.e,
    "c": 299792458,
    "g": 9.80665,
    "h": 6.62607015e-34,
    "G": 6.67430e-11,
    "Na": 6.02214076e23,
    "kb": 1.380649e-23,
}

SESSION_FILE = "session.json"

def load_session():
    """Load saved session variables."""
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_session(variables):
    """Save session variables to a file."""
    with open(SESSION_FILE, 'w') as f:
        json.dump(variables, f)

def safe_eval(node, variables):
    """Safely evaluate AST nodes."""
    if isinstance(node, ast.Constant):  # Numbers
        return node.value
    elif isinstance(node, ast.BinOp):  # Binary operations
        left = safe_eval(node.left, variables)
        right = safe_eval(node.right, variables)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Division by zero")
        return SAFE_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.Compare):  # Comparisons
        left = safe_eval(node.left, variables)
        right = safe_eval(node.comparators[0], variables)
        return int(SAFE_OPERATORS[type(node.ops[0])](left, right))
    elif isinstance(node, ast.Name):  # Variables
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    elif isinstance(node, ast.Call):  # Function calls
        func_name = node.func.id
        if func_name in SAFE_FUNCTIONS:
            arg = safe_eval(node.args[0], variables)
            return SAFE_FUNCTIONS[func_name](arg)
        raise ValueError(f"Unsupported function: {func_name}")
    elif isinstance(node, ast.BoolOp):  # Boolean operations
        values = [safe_eval(v, variables) for v in node.values]
        return int(all(values) if isinstance(node.op, ast.And) else any(values))
    raise ValueError("Unsupported operation")

def evaluate_expression(expression, variables):
    """Safely evaluate an expression with variable substitution."""
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
        if '=' in line:
            var, expr = map(str.strip, line.split('=', 1))
            try:
                variables[var] = evaluate_expression(expr, variables)
            except Exception as e:
                results.append((i + 1, f"Error in equation '{line}': {e}"))
        else:
            result = evaluate_expression(line, variables)
            results.append((i + 1, result))
        i += 1
    return results

def interactive_shell():
    """Start an interactive calculation session."""
    variables = load_session()
    print("Interactive Mode. Type 'exit' to quit.")
    while True:
        try:
            expr = input("calc> ").strip()
            if expr.lower() == "exit":
                save_session(variables)
                break
            result = evaluate_expression(expr, variables)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point of the program."""
    if len(sys.argv) < 2:
        interactive_shell()
        return
    if sys.argv[1] == '-f':
        if len(sys.argv) < 3:
            print("Error: No file specified")
            return
        with open(sys.argv[2], 'r') as f:
            lines = f.readlines()
        results = process_lines(lines)
        for line_num, result in results:
            print(f"Line {line_num}: {result}")
    else:
        expression = ' '.join(sys.argv[1:])
        print(evaluate_expression(expression, PREDEFINED_VARIABLES.copy()))

if __name__ == "__main__":
    main()
