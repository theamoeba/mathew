# Text Calculator Documentation

## Overview
The Text Calculator is a Python script that evaluates mathematical expressions, assigns variables, supports Boolean logic, and handles control structures such as conditions and loops.

## Usage
Run the script from the command line with an expression or a file:

```sh
python calc.py "1 + 2 * 3"
```

Or use a file as input:

```sh
python calc.py -f expressions.txt
```

## Supported Features

### 1. Basic Arithmetic Operations
The calculator supports:
- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Modulus (`%`)
- Power (`**`)

Example:
```sh
python calc.py "5 + 3 * 2"
```
Output:
```
11
```

### 2. Variable Assignments
Assign values to variables and use them in expressions.

Example:
```
a = 10
b = a * 2
c = b + 5
```

### 3. Boolean Expressions
Evaluates logical expressions and returns `0` (False) or `1` (True).

Example:
```sh
python calc.py "3 > 4"
```
Output:
```
0
```

### 4. If Conditions
Executes expressions only if a condition is true.

Example:
```
a = 5
if a > 3:
    b = a * 2
```

### 5. Loops
Supports `while` loops for iterative calculations.

Example:
```
a = 1
while a < 5:
    a = a + 1
```

### 6. Predefined Constants
Several predefined constants are available:
- `pi` (3.141592653589793)
- `e` (2.718281828459045)
- `c` (Speed of light: 299792458 m/s)
- `g` (Gravitational acceleration: 9.80665 m/s²)
- `h` (Planck’s constant: 6.62607015e-34 J⋅s)
- `G` (Gravitational constant: 6.67430e-11 m³⋅kg⁻¹⋅s⁻²)
- `Na` (Avogadro’s number: 6.02214076e23)
- `kb` (Boltzmann constant: 1.380649e-23 J/K)

Example:
```
energy = m * c**2
```

### 7. File Input Handling
You can pass a file containing multiple expressions, and the script will return an array of results with line numbers.

Example (`expressions.txt`):
```
a = 5
b = a * 2
c = b + 10
c
```
Run:
```sh
python calc.py -f expressions.txt
```
Output:
```
[(4, 20)]
```

## Error Handling
The script provides clear error messages if an expression is invalid or a variable is undefined.

Example:
```sh
python calc.py "x + 5"
```
Output:
```
Error: Undefined variable: x
```

## Conclusion
This calculator provides a powerful way to perform calculations, define variables, and handle logical conditions and loops. You can use it interactively or process entire files of expressions efficiently.

