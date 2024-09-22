from math import gcd

if __name__ == "__main__":
    devMode = True
else:
    devMode = False

PRECEDENCES = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
FUNCTIONS = ('sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'ctg', 'neg')
OPERATORS = ('+', '-', '*', '/', '^')

derivat = []

def log(*values, sep = " ", end = "\n"):
    if devMode:
        print(*values, sep=sep, end=end)

def isOperator(token):
    return token in PRECEDENCES

def isFunction(token):
    return token in FUNCTIONS

def isNumber(token):
    if isinstance(token, list):
        for i in token:
            if not isNumber(i):
                return False
        return True
    try:
        float(token)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def isVariable(token):
    try:
        if token.isalpha() and not isFunction(token) and not isOperator(token):
            return True
        else:
            return False
    except AttributeError:
        return False

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
            if isFunction(expression[start:i]):
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

def addImplicitMultiplication(tokens: list[str]) -> list[str]:
    result = []
    for i, token in enumerate(tokens):
        result.append(token)
        if i + 1 < len(tokens):
            current, nextToken = token, tokens[i + 1]
            if (isNumber(current) or isVariable(current) or current == ')') and (nextToken[0].isalpha() or isNumber(nextToken[0]) or nextToken == '('):
                result.append('*')
    return result

def shuntingYard(tokens):
    output = []
    operators = []
    
    for token in tokens:
        if isNumber(token) or isVariable(token):
            output.append(token)
        elif isFunction(token):
            operators.append(token)
        elif token == ',':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
        elif isOperator(token):
            while operators and operators[-1] != '(' and (
                (isOperator(operators[-1]) and PRECEDENCES[operators[-1]] > PRECEDENCES[token]) or
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
            if operators and isFunction(operators[-1]):
                output.append(operators.pop())
    
    while operators:
        if operators[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(operators.pop())
    
    return output

def lgb(postfix: list, index: int) -> int:
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

def gr(postfix: list, index: int) -> int:
    return index - lgb(postfix, index)

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
            assert postfix[upb - 1] != "0" 
            derivative(lwb, upb-1, postfix)
            derivat.extend(postfix[lwb:upb])
            derivat.append("/")
        elif postfix[upb] == 'exp':
            derivative(lwb, upb-1, postfix)
            derivat.extend(postfix[lwb:upb])
            derivat.extend(("exp", "*"))
        elif postfix[upb] == 'sqrt':
            assert postfix[upb - 1] != "0" 
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
        middle = lgb(postfix, upb - 1)
        if postfix[upb] == '+' or postfix[upb] == '-':
            derivative(lwb, middle - 1, postfix)
            prevIndex2 = len(derivat) - 1
            derivative(middle, upb-1, postfix)
            index = len(derivat) - 1
            if derivat[prevIndex2] == "0" and derivat[index] == "0":
                derivat.pop()
            elif derivat[prevIndex2] == "0":
                derivat.pop(prevIndex2)
                if postfix[upb] == "-":
                    derivat.append("neg")
            elif derivat[index] == "0":
                derivat.pop(index)
            else:
                derivat.append(postfix[upb])

        elif postfix[upb] == '*':
            zeros = 0

            prevIndex1 = len(derivat) - 1
            derivat.extend(postfix[lwb:middle])
            prevIndex2 = len(derivat) - 1
            derivative(middle, upb - 1, postfix)

            index = len(derivat) - 1

            if derivat[prevIndex2] == "0" or derivat[index] == "0":
                derivat = derivat[:prevIndex1 + 1]
                zeros += 1
            elif derivat[prevIndex2] == "1":
                derivat.pop(prevIndex2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            ind1 = len(derivat) - 1

            prevIndex1 = len(derivat) - 1
            derivative(lwb, middle-1, postfix)
            prevIndex2 = len(derivat) - 1
            derivat.extend(postfix[middle:upb])

            index = len(derivat) - 1

            if derivat[prevIndex2] == "0" or derivat[index] == "0":
                derivat = derivat[:prevIndex1 + 1]
                zeros += 1
            elif derivat[prevIndex2] == "1":
                derivat.pop(prevIndex2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            if zeros == 0:
                derivat.append("+")
            elif zeros == 2:
                derivat.append("0")

        elif postfix[upb] == '/':
            assert postfix[upb - 1] != "0" 

            zeros = 0
            firstHalf = ""

            prevIndex1 = len(derivat) - 1
            derivat.extend(postfix[middle:upb])
            prevIndex2 = len(derivat) - 1
            derivative(lwb, middle - 1, postfix)

            index = len(derivat) - 1

            if derivat[prevIndex2] == "0" or derivat[index] == "0":
                derivat = derivat[:prevIndex1 + 1]
                firstHalf = "0"
                zeros += 1
            elif derivat[prevIndex2] == "1":
                derivat.pop(prevIndex2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            ind1 = len(derivat) - 1

            prevIndex1 = len(derivat) - 1
            derivative(middle, upb - 1, postfix)
            prevIndex2 = len(derivat) - 1
            derivat.extend(postfix[lwb:middle])

            index = len(derivat) - 1

            if derivat[prevIndex2] == "0" or derivat[index] == "0":
                derivat = derivat[:prevIndex1 + 1]
                zeros += 1
            elif derivat[prevIndex2] == "1":
                derivat.pop(prevIndex2)
            elif derivat[index] == "1":
                derivat.pop()
            else:
                derivat.append("*")

            if firstHalf == "0" and derivat[ind1 + 1:] != []:
                derivat.append("neg")
            elif not derivat[ind1 + 1:] == [] and firstHalf != "0":
                derivat.append("-")

            if zeros == 2:
                derivat.append("0")
            elif postfix[upb - 1] != "1":
                derivat.extend(postfix[middle:upb])
                derivat.extend(("2", "^", "/"))

        elif postfix[upb] == '^':
            if postfix[upb - 1] == "0" or postfix[middle - 1] == "0":
                derivat.append("0")
            elif postfix[middle - 1] == "1":
                derivat.append("0")
            else:
                u = postfix[lwb:middle]
                v = postfix[middle:upb]
                expression = v + u + ["log", "*"]
                derivative(0, len(expression) - 1, expression)
                derivat.extend(expression + ["exp", "*"])

    else:
        if postfix[upb] == "x":
            derivat.append("1")
        else:
            derivat.append("0")               

class Fraction:
    def __init__(self, numerator, denominator=1):
        if isinstance(numerator, str) and '/' in numerator:
            numerator, denominator = map(int, numerator.split('/'))
        else:
            numerator = int(numerator)
            denominator = int(denominator)
        
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        
        common = gcd(numerator, denominator)
        self.numerator = numerator // common
        self.denominator = denominator // common

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Fraction(other)
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

    def __pow__(self, power):
        if isinstance(power, int):
            if power >= 0:
                return Fraction(self.numerator ** power, self.denominator ** power)
            else:
                return Fraction(self.denominator ** -power, self.numerator ** -power)
        else:
            return pow(float(self), power)

    def __float__(self):
        return self.numerator / self.denominator

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

def calculate(numbers: list, operator: str) -> str:
    result = Fraction(numbers[0])
    for num in numbers[1:]:
        num = Fraction(num)
        if operator == '+':
            result += num
        elif operator == '-':
            result -= num
        elif operator == '*':
            result *= num
        elif operator == '/':
            result /= num
        elif operator == '^':
            result = result ** float(num)
    return str(result)

def calcList(terms: list, operator: str, nums=None, variables=None) -> list:
    if nums is None:
        nums = []
    if variables is None:
        variables = []

    log("List: ", terms)
    log("Numbers:", nums)
    log("Variables:", variables)

    if operator == '*' or operator == '/':
        for term in terms:
            if isinstance(term, list):
                nums.append(term[0])
                try:
                    if isinstance(term[1], list):
                        calcList(term[1], operator, nums, variables)
                    else:
                        variables.append(term[1])
                except IndexError:
                    pass
            elif isNumber(term):
                nums.append(term)
            else:
                variables.append(term)

        if len(variables) == 0:
            return [calculate(nums, operator)]
        elif len(variables) > 1:
            if all(var == variables[0] for var in variables):
                return [calculate(nums, operator), str(variables[0]) + '^' + str(len(variables))]

        return [calculate(nums, operator), ''.join(variables)]

    elif operator == '+' or operator == '-':
        if all(isinstance(term, list) for term in terms):
            if terms[0][1] == terms[1][1]:
                calc = calculate([terms[0][0], terms[1][0]], operator)
                if calc == "0":
                    return ["0"]
                elif calc == "1":
                    return [terms[0][1]]
                else:
                    return [calc, terms[0][1], '*']
            else:
                return [terms[0], terms[1], operator]
        else:
            return [terms[0], terms[1], operator]

def simplify(derivat: list) -> list:
    if len(derivat) <= 2:
        return derivat

    for i in range(len(derivat)):
        if derivat[i] in OPERATORS:
            lgbIndex = lgb(derivat, i)
            terms = derivat[lgbIndex:i]
            log("Terms: ", terms)
            if derivat[i] == '^':
                if len(terms) == 2:
                    if terms[1] == "0":
                        return ["1"]
                    elif terms[1] == "1":
                        return terms[0]
                    elif terms[0] == "0":
                        return ["0"]
                    elif terms[0] == "1":
                        return ["1"]
                    elif isNumber(terms):
                        result = calculate(terms, derivat[i])
                        simplified = derivat[:lgbIndex] + [result] + derivat[i+1:]
                        return simplify(simplified)
                    else:                      
                        result = []
                        result.extend((simplify(terms[0]), simplify(terms[1]), derivat[i]))

                        log("Result: ", result)
                        
                        simplified = derivat[:lgbIndex] + [result] + derivat[i+1:]
                        return simplify(simplified)
                
            elif derivat[i] in OPERATORS:
                if derivat[i] == '*' and "0" in terms:
                    return ["0"]
                elif isNumber(terms):
                    result = calculate(terms, derivat[i])
                    simplified = derivat[:lgbIndex] + [result] + derivat[i+1:]
                    return simplify(simplified)
                else:
                    variables = []
                    numbers = []
                    for term in terms:
                        if isinstance(term, list):
                            result = calcList(terms, derivat[i])
                            simplified = derivat[:lgbIndex] + [result] + derivat[i+1:]
                            return simplify(simplified)
                        elif isVariable(term):
                            variables.append(term)
                        else:
                            numbers.append(term)
                    
                    if len(numbers) == 0 and derivat[i] in ('*', '/'):
                        numbers = ["1"]
                    
                    result = []
                    result.extend((calculate(numbers, derivat[i]), *variables, derivat[i]))

                    log("Result: ", result)
                    
                    simplified = derivat[:lgbIndex] + [result] + derivat[i+1:]
                    return simplify(simplified)

    return derivat

def algebricNotation(derivat: list) -> str:
    stack = []
    for token in derivat:
        if isinstance(token, list):
            if len(token) >= 2 and isNumber(token[0]):
                coefficient = token[0]
                variable = token[1]
                operator = token[2] if len(token) > 2 else '*'  
                if coefficient == "1" and operator == '*':
                    stack.append(variable)
                elif coefficient == "-1" and operator == '*':
                    stack.append(f"-{variable}")
                else:
                    if operator in ('+', '-'):
                        stack.append(f"{coefficient}{operator}{variable}")
                    else:
                        stack.append(f"{coefficient}*{variable}")
            else:
                stack.append(algebricNotation(token))
        elif token in OPERATORS:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(f"{a} + {b}")
            elif token == '-':
                stack.append(f"{a} - {b}")
            elif token == '*':
                if a == "0" or b == "0":
                    stack.append("0")
                elif a == "1":
                    stack.append(b)
                elif b == "1":
                    stack.append(a)
                else:
                    stack.append(f"{a}*{b}")
            elif token == '/':
                assert b != "0"
                if a == "0":
                    stack.append("0")
                elif b == "1":
                    stack.append(a)
                else:
                    stack.append(f"{a}/{b}")
            elif token == '^':
                if a == "0":
                    stack.append("0")
                elif b == "0":
                    stack.append("1")
                elif b == "1":
                    stack.append(a)
                else:
                    stack.append(f"{a}^{b}")
        elif token in FUNCTIONS:
            if token == 'neg':
                a = stack.pop()
                stack.append(f"-{a}")
            else:
                a = stack.pop()
                stack.append(f"{token}({a})")
        else:
            stack.append(token)
    
    return stack[0] if stack else "0"

def credits():
    if not devMode:
        print("Derivative Calculator © 2024 Gaskam.com - All rights reserved.\nProgrammed by Leys Kamil and Lebaube Gaspard - github.com/gaskam-com\nInspired by 'SYMBOLIC DERIVATION WITHOUT USING EXPRESSION TREES (2001)' by V. KRTOLICA and S. STANIMIROVIC\n\nFor more information, visit github.com/gaskam-com/derivcalc\n\nEnjoy! :)\n")

def main():
    credits()
    while True:
        expression = input("Expression: ")
        tokens = tokenize(expression)
        tokensWithImplicitMult = addImplicitMultiplication(tokens)
        postfix = shuntingYard(tokensWithImplicitMult)
        log("RPN: ", postfix)
        derivative(0, len(postfix)-1, postfix)
        log("RPNderivat: ", derivat)
        simplified = simplify(derivat)
        log("Simplified: ", simplified)
        infixNotation = algebricNotation(derivat)
        print("Derivative: ", infixNotation, "\n\n", 30*'-', "\n")
        derivat.clear()

main()