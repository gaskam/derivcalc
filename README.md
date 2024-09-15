# Derivative Calculator for Numworks

This project is a symbolic derivative calculator designed for the Numworks calculator, implemented in Python. It uses **Reverse Polish Notation (RPN)** to directly compute derivatives without expression trees. The calculator handles both basic arithmetic operations and advanced functions like trigonometry, logarithms, and exponentiation.

## Features

- Supports core operations: `+`, `-`, `*`, `/`, `^`.
- Handles functions such as `sin`, `cos`, `tan`, `log`, `exp`, `sqrt`, and more.
- Efficient derivative computation without the use of expression trees, saving memory and processing time.
- Simplifies expressions involving implicit multiplication and redundant terms.
- Allowing users to input complex mathematical expressions and receive their symbolic derivatives.

## How it Works

This program is inspired by the paper **“Symbolic Derivation without Using Expression Trees (2001)”** by **Predrag V. Krtolica** and **Predrag S. Stanimirović**. Here's a high-level overview of the process:

1. **Tokenization**: The mathematical expression is broken into manageable tokens, including numbers, operators, and functions.
2. **Reverse Polish Notation (RPN)**: Instead of creating an expression tree, the tokens are converted into RPN using the shunting yard algorithm. RPN ensures proper precedence of operations without the need for parentheses.
3. **Derivative Calculation**: The program traverses the RPN in reverse order, applying derivative rules for each token. The recursive algorithm simplifies the derivative as it progresses, applying the chain rule and product rule where necessary.
4. **Simplification**: After computing the derivative, the algorithm eliminates redundant terms (e.g., `x * 0`, `1 * x`, etc.) and outputs a simplified expression.
5. **Infix Notation**: Finally, the result is converted back into infix notation, making it easy to read.

This method is memory-efficient, as it avoids the creation of expression trees and requires only two arrays: one for the input expression (in RPN) and one for the derivative (also in RPN).

### Example

Given the input:

```bash
Expression: sin(x) + x^2
```

The program will return:

```bash
Derivative: cos(x) + 2*x
```

## Usage

### Numworks Integration

This program is intended for use on a Numworks calculator. Visit our official [Numworks page](https://my.numworks.com/python/numworks/derivcalc) to import easily the program.

You can also follow these steps to transfer the program to your Numworks device:

1. **Connect the Calculator to Your Computer**:
   - Use the Numworks USB cable to connect your calculator to a PC.
   - Open your browser and navigate to the official [Numworks Python interface](https://my.numworks.com/).
   
2. **Install the Python Script**:
   - Click on "Upload a script" in the Python interface.
   - Upload the `derivcalc.py` file from this repository.
   
3. **Run the Program**:
   - On your Numworks calculator, navigate to the Python app.
   - Run the `derivcalc.py` script.
   - Input the expression you want to differentiate when prompted, and the calculator will return the symbolic derivative.

### Requirements

- A **Numworks calculator** with Python enabled!
- Alternatively, you can run the program on any Python environment, such as on a desktop with **Python 3.x** installed.

## To-Do

* Correct the derivative of the `^` operator.

* Fully implement `ctg` and `tan` functions.

* Simplify the final output expression.

* Correct bugs and make the program more robust.

* Implement more test cases.

* And more...

## Credits

Created by [Leys Kamil](https://github.com/kamil-leys) and [Lebaube Gaspard](https://github.com/PatafixPLTX).

Based on **"Symbolic Derivation without Using Expression Trees"** by **Predrag V. Krtolica** and **Predrag S. Stanimirović**.

This project is designed specifically for the **Numworks calculator** ^^ 

***NUMWORKS, WE WANT A CAS ON YOUR CALCULATOR ! IT'S EASY TO IMPLEMENT WITH SYMPY !***

## Sources

- [Numworks Python Interface](https://my.numworks.com/python/)
- [Reverse Polish Notation (RPN)](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
- [Shunting Yard Algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm)
- [Symbolic Derivation without Using Expression Trees (2001)](https://www.researchgate.net/publication/268863620_Symbolic_derivation_without_using_expression_trees)

## License

This project is licensed under **Gaskam.com** © 2024. All rights reserved.

For more information, visit our [GitHub page](https://github.com/gaskam-com/derivcalc).