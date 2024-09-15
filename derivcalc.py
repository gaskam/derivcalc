PRECEDENCES = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
FUNCTIONS = ('sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'ctg', 'neg')
OPERATORS = ('+', '-', '*', '/', '^')

derivat = []

def is_operator(token):
    return token in PRECEDENCES

def is_function(token):
    return token in FUNCTIONS

def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_variable(token):
    return token.isalpha() and not is_function(token)

def tokenize(expression: str) -> list[str]:
    tokens = []
    i = 0
    expression = expression.replace("**", "^").replace(' ', '')

    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            tokens.append(expression[start:i])
        elif expression[i].isalpha():
            start = i
            while i < len(expression) and expression[i].isalpha():
                tokens.append(expression[i])
                i += 1
            if is_function(expression[start:i]):
                tokens.append(expression[start:i])
                for _ in range(i - start):
                    tokens.pop(-2)
        elif expression[i] in ['+', '*', '/', '^', '(', ')', ',']:
            tokens.append(expression[i])
            i += 1
        elif expression[i] == '-':
            if expression[i + 1].isdigit() or expression[i + 1] == '.':
                start = i
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                if start == 0 or expression[start - 1] in ['+', '-', '*', '/', '^', '(']:
                    tokens.append(expression[start:i])
                else:
                    tokens.extend(['+', expression[start:i]])
            else:
                if i == 0 or expression[i - 1] in ['+', '-', '*', '/', '^', '(']:
                    tokens.extend(['-1', '*'])
                else:
                    tokens.extend(['+', '-1', '*'])
                i += 1
        else:
            i += 1
    return tokens

def add_implicit_multiplication(tokens: list[str]) -> list[str]:
    result = []
    for i, token in enumerate(tokens):
        result.append(token)
        if i + 1 < len(tokens):
            current, next_token = token, tokens[i + 1]
            if (is_number(current) or is_variable(current) or current == ')') and (next_token[0].isalpha() or is_number(next_token[0]) or next_token == '('):
                result.append('*')
    return result

def shunting_yard(tokens):
    output = []
    operators = []
    
    for token in tokens:
        if is_number(token) or is_variable(token):
            output.append(token)
        elif is_function(token):
            operators.append(token)
        elif token == ',':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
        elif is_operator(token):
            while operators and operators[-1] != '(' and (
                (is_operator(operators[-1]) and PRECEDENCES[operators[-1]] > PRECEDENCES[token]) or
                (PRECEDENCES[operators[-1]] == PRECEDENCES[token] and token != '^')
            ):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()
            if operators and is_function(operators[-1]):
                output.append(operators.pop())
    
    while operators:
        if operators[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(operators.pop())
    
    return output

def LGB(postfix: list, index: int) -> int:
    remaining = 1
    i = index
    while remaining > 0:
        remaining -= 1
        if postfix[i] in FUNCTIONS:
            remaining += 1
        elif postfix[i] in OPERATORS:
            remaining += 2
        i -= 1

    return i + 1

def GR(postfix: list, index: int) -> int:
    return index - LGB(postfix, index)

def derivative(lwb: int, upb: int, postfix: list) -> list:
    global derivat
    if postfix[upb] in FUNCTIONS:
        if postfix[upb] == 'sin':
            derivat.extend(postfix[lwb:upb])
            derivat.append("cos")
            if postfix[upb - 1] != "0":
                derivative(lwb, upb-1, postfix)
                derivat.append("*")
        elif postfix[upb] == 'cos':
            if postfix[upb - 1] != "0":
                derivat.extend(postfix[lwb:upb])
                derivat.append("sin")
                derivative(lwb, upb-1, postfix)
                derivat.extend(("neg", "*"))
            else:
                derivat.append("0")
        elif postfix[upb] == 'log':
            assert postfix[upb - 1] != "0" # Logarithm of zero
            derivative(lwb, upb-1, postfix)
            derivat.extend(postfix[lwb:upb])
            derivat.append("/")
        elif postfix[upb] == 'exp':
            derivative(lwb, upb-1, postfix)
            derivat.extend(postfix[lwb:upb])
            derivat.extend(("exp", "*"))
        elif postfix[upb] == 'sqrt':
            assert postfix[upb - 1] != "0" # Logarithm of zero
            if postfix[upb - 1] == "1":
                derivat.extend(postfix[lwb:upb])
                derivat.extend(("2", "/"))
            else:
                derivative(lwb, upb-1, postfix)
                derivat.append("2")
                derivat.extend(postfix[lwb:upb])
                derivat.extend(("sqrt", "*", "/"))
        elif postfix[upb] == 'neg':
            derivative(lwb, upb-1, postfix)
            if derivat[-1] != "0":
                derivat.append("neg")
    elif postfix[upb] in OPERATORS:
        middle = LGB(postfix, upb - 1)
        if postfix[upb] == '+' or postfix[upb] == '-':
            derivative(lwb, middle - 1, postfix)
            prev_index2 = len(derivat) - 1
            derivative(middle, upb-1, postfix)
            index = len(derivat) - 1
            if derivat[prev_index2] == "0" and derivat[index] == "0":
                derivat.pop()
            elif derivat[prev_index2] == "0":
                derivat.pop(prev_index2)
            elif derivat[index] == "0":
                derivat.pop(index)
                if postfix[upb] == "-":
                    derivat.append("neg")
            else:
                derivat.append(postfix[upb])

        elif postfix[upb] == '*':
            Zeros = 0

            prev_index1 = len(derivat) - 1
            derivat.extend(postfix[lwb:middle])
            prev_index2 = len(derivat) - 1
            derivative(middle, upb - 1, postfix)

            index = len(derivat) - 1

            if derivat[prev_index2] == "0" or derivat[index] == "0":
                derivat = derivat[:prev_index1 + 1]
                Zeros += 1
            elif derivat[prev_index2] == "1":
                derivat.pop(prev_index2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            ind1 = len(derivat) - 1

            prev_index1 = len(derivat) - 1
            derivative(lwb, middle-1, postfix)
            prev_index2 = len(derivat) - 1
            derivat.extend(postfix[middle:upb])

            index = len(derivat) - 1

            if derivat[prev_index2] == "0" or derivat[index] == "0":
                derivat = derivat[:prev_index1 + 1]
                Zeros += 1
            elif derivat[prev_index2] == "1":
                derivat.pop(prev_index2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            if Zeros == 0:
                derivat.append("+")

        elif postfix[upb] == '/':
            assert postfix[upb - 1] != "0" # Division by zero

            Zeros = 0
            firstHalf = ""

            prev_index1 = len(derivat) - 1
            derivat.extend(postfix[lwb:middle])
            prev_index2 = len(derivat) - 1
            derivative(middle, upb - 1, postfix)

            index = len(derivat) - 1

            if derivat[prev_index2] == "0" or derivat[index] == "0":
                derivat = derivat[:prev_index1 + 1]
                firstHalf = "0"
                Zeros += 1
            elif derivat[prev_index2] == "1":
                derivat.pop(prev_index2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            ind1 = len(derivat) - 1

            prev_index1 = len(derivat) - 1
            derivative(lwb, middle-1, postfix)
            prev_index2 = len(derivat) - 1
            derivat.extend(postfix[middle:upb])

            index = len(derivat) - 1

            if derivat[prev_index2] == "0" or derivat[index] == "0":
                derivat = derivat[:prev_index1 + 1]
                Zeros += 1
            elif derivat[prev_index2] == "1":
                derivat.pop(prev_index2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            if firstHalf == "0":
                derivat.append("neg")
            elif not derivat[-1] == "0":
                derivat.append("-")

            if postfix[upb - 1] != "1":
                derivat.extend(postfix[middle:upb])
                derivat.extend(("2", "^", "/"))

        elif postfix[upb] == '^':
            if postfix[upb - 1] == "0" or postfix[middle - 1] == "0":
                derivat.append("0")
            elif postfix[middle - 1] == "1":
                derivat.append("0")
            else:
                derivat.extend(postfix[middle:upb])
                
                derivative(lwb, middle - 1, postfix)

                if derivat[-1] == "1":
                    derivat.pop()
                else:
                    derivat.append("*")

                derivat.extend(postfix[lwb:upb])
                derivat.extend(("1", "-", "^", "*"))    

    else:
        if postfix[upb] == "x":
            derivat.append("1")
        else:
            derivat.append("0")               

# def simplify(derivat: list) -> list:
#     pass

def algebric_notation(derivat: list) -> str:
    stack = []
    for token in derivat:
        if token in OPERATORS:
            b = stack.pop()
            a = stack.pop()
            if token == '+' or token == '-':
                stack.append(a + " " +  token + " " + b)
            elif token == '*':
                stack.append(a + "*" + b)
            elif token == '/':
                stack.append(a + "/" + b)
            elif token == '^':
                stack.append(a + "^" + b)
        elif token in FUNCTIONS:
            if token == 'neg':
                a = stack.pop()
                stack.append("-" + a)
            else:
                a = stack.pop()
                stack.append(token + "(" + a + ")")
        else:
            stack.append(token)
    
    return stack[0] if stack else ""

def credits():
    print("Derivative Calculator © 2024 Gaskam.com - All rights reserved.\nProgrammed by Leys Kamil and Lebaube Gaspard - github.com/gaskam-com\nInspired by 'SYMBOLIC DERIVATION WITHOUT USING EXPRESSION TREES (2001)' by V. KRTOLICA and S. STANIMIROVIC\n\nFor more information, visit github.com/gaskam-com/derivcalc\n\nEnjoy! :)\n")

def main():
    credits()
    while True:
        expression = input("Expression: ")
        tokens = tokenize(expression)
        tokens_with_implicit_mult = add_implicit_multiplication(tokens)
        postfix = shunting_yard(tokens_with_implicit_mult)
        derivative(0, len(postfix)-1, postfix)
        # siplified = simplify(derivat)
        infix_notation = algebric_notation(derivat)
        print("Derivative: ", infix_notation, "\n\n", 30*'-', "\n")
        derivat.clear()

main()