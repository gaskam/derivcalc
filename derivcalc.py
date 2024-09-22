from math import gcd

if __name__ == "__main__":
    devMode = True
else:
    devMode = False

precedences = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
functions = ('sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'ctg', 'neg')
operators = ('+', '-', '*', '/', '^')

derivat = []

def log(*values, sep = " ", end = "\n"):
    if devMode:
        print(*values, sep=sep, end=end)

def isOperator(token):
    return token in precedences

def isFunction(token):
    return token in functions

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

def isVariable(token):
    return token.isalpha() and not isFunction(token)

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
                (isOperator(operators[-1]) and precedences[operators[-1]] > precedences[token]) or
                (precedences[operators[-1]] == precedences[token] and token != '^')
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
        if postfix[i] in functions:
            remaining += 1
        elif postfix[i] in operators:
            remaining += 2
        i -= 1

    return i + 1

def gr(postfix: list, index: int) -> int:
    return index - lgb(postfix, index)

def derivative(lwb: int, upb: int, postfix: list) -> list:
    global derivat
    if postfix[upb] in functions:
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
    elif postfix[upb] in operators:
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
            elif derivat[index] == "0":
                derivat.pop(index)
                if postfix[upb] == "-":
                    derivat.append("neg")
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

        elif postfix[upb] == '/':
            assert postfix[upb - 1] != "0" 

            zeros = 0
            firstHalf = ""

            prevIndex1 = len(derivat) - 1
            derivat.extend(postfix[lwb:middle])
            prevIndex2 = len(derivat) - 1
            derivative(middle, upb - 1, postfix)

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

def calcList(var: list, operator: str, nums=None, variables=None) -> list:
    if nums is None:
        nums = []
    if variables is None:
        variables = []

    try:
        if len(var) > 2 and isinstance(var[1], list):
            nums.append(var[0])
            calcList(var[1], operator, nums, variables)
            variables.append(var[2])
        else:
            nums.append(var[0])
            variables.extend(var[1:])
    except IndexError:
        nums.append(var[0])
        variables.extend(var[1:])

    log("List: ", var)
    log("Numbers:", nums)
    log("Variables:", variables)

    if len(variables) == 1:
        variables = variables[0]

    return [calculate(nums, operator), variables]

def simplify(derivat: list) -> list:
    if len(derivat) <= 2:
        return derivat

    for i in range(len(derivat)):
        if derivat[i] in operators:
            lgbIndex = lgb(derivat, i)
            terms = derivat[lgbIndex:i]
            if derivat[i] in operators:
                if derivat[i] == '*' and "0" in terms:
                    return ["0"]
                elif all(isNumber(term) for term in terms):
                    result = calculate(terms, derivat[i])
                    simplified = derivat[:lgbIndex] + [result] + derivat[i+1:]
                    return simplify(simplified)
                else:
                    variables = []
                    numbers = []
                    for term in terms:
                        if isinstance(term, list):
                            result = calcList(term, derivat[i])
                            numbers.append(result[0])
                            variables.extend(result[1] if isinstance(result[1], list) else [result[1]])
                        elif isVariable(term):
                            variables.append(term)
                        else:
                            numbers.append(term)
                    
                    if len(numbers) == 0:
                        numbers = ["1"] if derivat[i] in ('*', '/') else ["0"]
                    
                    numericResult = calculate(numbers, derivat[i])
                    
                    if derivat[i] in ('+', '-'):
                        if variables:
                            result = [[numericResult] + variables + [derivat[i]]]  
                        else:
                            result = [numericResult]
                    elif derivat[i] == '^':
                        if len(variables) == 1:
                            result = [[numericResult] + [f"{variables[0]}^{terms[-1]}"]]
                        else:
                            result = [f"({numericResult})^{terms[-1]}"]
                    else:  
                        if len(variables) == 0:
                            result = [numericResult]
                        elif len(variables) == 1:
                            result = [[numericResult] + variables + [derivat[i]]]  
                        else:
                            varCounts = {}
                            for var in variables:
                                if var in varCounts:
                                    varCounts[var] += 1
                                else:
                                    varCounts[var] = 1
                            
                            combinedVars = []
                            for var, count in varCounts.items():
                                if count == 1:
                                    combinedVars.append(var)
                                else:
                                    combinedVars.append(f"{var}^{count}")
                            
                            result = [[numericResult] + [''.join(combinedVars)] + [derivat[i]]]  
                    
                    simplified = derivat[:lgbIndex] + result + derivat[i+1:]
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
        elif token in operators:
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
        elif token in functions:
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
        # derivative(0, len(postfix)-1, postfix)
        # log("RPNderivat: ", derivat)
        simplified = simplify(postfix)
        log("Simplified: ", simplified)
        infixNotation = algebricNotation(simplified)
        print("Derivative: ", infixNotation, "\n\n", 30*'-', "\n")
        derivat.clear()

main()