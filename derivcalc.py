PRECEDENCES = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
FUNCTIONS = ('sin', 'cos', 'log', 'exp', 'sqrt', 'ctg', 'neg')
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
        match postfix[i]:
            case _ if postfix[i] in FUNCTIONS:
                remaining += 1
            case _ if postfix[i] in OPERATORS:
                remaining += 2
        i -= 1

    return i + 1

def GR(postfix: list, index: int) -> int:
    return index - LGB(postfix, index)

def derivative(lwb: int, upb: int, postfix: list) -> list:
    if postfix[upb] in FUNCTIONS:
        match postfix[upb]:
            case 'sin':
                derivat.extend(postfix[lwb:upb])
                derivat.append("cos")
                if postfix[upb - 1] != "0":
                    derivative(lwb, upb-1, postfix)
                    derivat.append("*")
            case 'cos':
                if postfix[upb - 1] != "0":
                    derivat.extend(postfix[lwb:upb])
                    derivat.append("sin")
                    derivative(lwb, upb-1, postfix)
                    derivat.extend(("neg", "*"))
                else:
                    derivat.append("0")
            case 'log':
                assert postfix[upb - 1] != "0" # Logarithm of zero

                derivative(lwb, upb-1, postfix)
                derivat.extend(postfix[lwb:upb])
                derivat.append("/")
            case 'exp':
                derivative(lwb, upb-1, postfix)
                derivat.extend(postfix[lwb:upb])
                derivat.extend(("exp", "*"))
            case 'sqrt':
                assert postfix[upb - 1] != "0" # Logarithm of zero

                if postfix[upb - 1] == "1":
                    derivat.extend(postfix[lwb:upb])
                    derivat.extend(("2", "/"))
                else:
                    derivative(lwb, upb-1, postfix)
                    derivat.append("2")
                    derivat.extend(postfix[lwb:upb])
                    derivat.extend(("sqrt", "*", "/"))
            case 'neg':
                derivative(lwb, upb-1, postfix)
                if derivat[-1] != "0":
                    derivat.append("neg")
    elif postfix[upb] in OPERATORS:
        middle = LGB(postfix, upb) + 1
        match postfix[upb]:
            case '+' | '-':
                derivative(lwb, middle-1, postfix)
                prev_index = len(derivat) - 1
                derivative(middle, upb-1, postfix)

                index = len(derivat) - 1

                if derivat[prev_index] == "0" and derivat[index] == "0":
                    derivat.pop()
                elif derivat[prev_index] == "0":
                    derivat.pop(prev_index)
                elif derivat[index] == "0":
                    derivat.pop(index)
                    if postfix[upb] == "-":
                        derivat.append("neg")
                else:
                    derivat.append(postfix[upb])

            case '*':
                firstHalf = ""

                derivat.extend(postfix[lwb:middle])
                prev_index = len(derivat) - 1
                derivative(middle, upb - 1, postfix)

                index = len(derivat) - 1

                if derivat[prev_index] == "0" or derivat[index] == "0":
                    derivat.pop()
                    derivat.pop()
                    derivat.append("0")
                    firstHalf = "0"
                elif derivat[prev_index] == "1":
                    derivat.pop(prev_index)
                elif derivat[index] == "1":
                    derivat.pop()
                else:
                    derivat.append("*")

                ind1 = len(derivat) - 1

                derivative(lwb, middle-1, postfix)
                prev_index = len(derivat) - 1
                derivat.extend(postfix[middle:upb])

                index = len(derivat) - 1

                if derivat[prev_index] == "0" or derivat[index] == "0":
                    derivat.pop()
                    derivat.pop()
                    derivat.append("0")
                    secondHalf = "0"
                elif derivat[prev_index] == "1":
                    derivat.pop(prev_index)
                    secondHalf = "1"
                elif derivat[index] == "1":
                    derivat.pop()
                    secondHalf = "1"
                else:
                    derivat.append("*")

                if firstHalf == "0":
                    derivat.pop(ind1)
                elif secondHalf == "0":
                    derivat.pop()
                else:
                    derivat.append("+")

            case '/':
                assert postfix[upb - 1] != "0" # Division by zero

                firstHalf = ""

                derivat.extend(postfix[lwb:middle])
                prev_index = len(derivat) - 1
                derivative(middle, upb - 1, postfix)

                index = len(derivat) - 1

                if derivat[prev_index] == "0" or derivat[index] == "0":
                    derivat.pop()
                    derivat.pop()
                    derivat.append("0")
                    firstHalf = "0"
                elif derivat[prev_index] == "1":
                    derivat.pop(prev_index)
                elif derivat[index] == "1":
                    derivat.pop()
                else:
                    derivat.append("*")

                ind1 = len(derivat) - 1

                derivative(lwb, middle-1, postfix)
                prev_index = len(derivat) - 1
                derivat.extend(postfix[middle:upb])

                index = len(derivat) - 1

                if derivat[prev_index] == "0" or derivat[index] == "0":
                    derivat.pop()
                    derivat.pop()
                    derivat.append("0")
                    secondHalf = "0"
                elif derivat[prev_index] == "1":
                    derivat.pop(prev_index)
                    secondHalf = "1"
                elif derivat[index] == "1":
                    derivat.pop()
                    secondHalf = "1"
                else:
                    derivat.append("*")

                if firstHalf == "0":
                    derivat.pop(ind1)
                    derivat.append("neg")
                elif secondHalf == "0":
                    derivat.pop()
                else:
                    derivat.append("-")

                if postfix[upb - 1] != "1":
                    derivat.extend(postfix[middle:upb])
                    derivat.extend(("^", "2", "/"))

    else:
        if postfix[upb] == "x":
            derivat.append("1")
        else:
            derivat.append("0")               
        
if __name__ == "__main__":
    expression = input()
    tokens = tokenize(expression)
    tokens_with_implicit_mult = add_implicit_multiplication(tokens)
    postfix = shunting_yard(tokens_with_implicit_mult)
    print(postfix)

    derivative(0, len(postfix)-1, postfix)
    print(derivat)