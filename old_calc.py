import sys
import re

def evaluate_expression(expression, variables):
    """Evaluate a mathematical or boolean expression with variables."""
    try:
        # Replace variable names with their values
        for var in variables:
            expression = re.sub(rf'\b{var}\b', str(variables[var]), expression)
        
        # Evaluate boolean expressions
        if any(op in expression for op in ['<', '>', '<=', '>=', '==', '!=']):
            return int(eval(expression))  # Convert True to 1, False to 0
        
        # Evaluate arithmetic expressions
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

def process_lines(lines):
    """Process multiple lines of input."""
    variables = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line or line.startswith('#'):  # Ignore empty lines and comments
            i += 1
            continue
        
        # Handle variable assignment
        if '=' in line:
            var, expr = map(str.strip, line.split('=', 1))
            variables[var] = evaluate_expression(expr, variables)
        
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
            print(evaluate_expression(line, variables))
        
        i += 1

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
        process_lines(lines)
    else:
        expression = ' '.join(sys.argv[1:])
        print(evaluate_expression(expression, {}))

if __name__ == "__main__":
    main()
