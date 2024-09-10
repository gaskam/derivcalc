def tokenize(expression: str):
    tokens = []
    i = 0
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
        elif expression[i] in ['+', '-', '*', '/', '^', '(', ')', ',']:
            tokens.append(expression[i])
            i += 1
        else:
            i += 1

    implicit_tokens = []
    for j, token in enumerate(tokens):
        implicit_tokens.append(token)
        
        if j + 1 < len(tokens):
            current = tokens[j]
            next_token = tokens[j + 1]
            
            if (is_number(current) or is_variable(current) or current == ')') and (next_token.isalnum() or next_token == '('):
                implicit_tokens.append('*')

    return implicit_tokens

def precedence(op):
    precedences = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    return precedences[op] if op in precedences else 0

def is_left_associative(op):
    return op != '^'

def is_operator(token):
    return token in ['+', '-', '*', '/', '^']

def is_function(token):
    functions = {'sin', 'cos', 'tan', 'log', 'sqrt', 'abs'}
    return token in functions

def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False
    
def is_variable(token):
    return token.isalpha() and token not in {'sin', 'cos', 'tan', 'log', 'sqrt', 'abs'}

def shunting_yard(tokens):
    output_queue = []
    operator_stack = []
    
    for token in tokens:
        if is_number(token) or is_variable(token):
            output_queue.append(token)
        elif is_function(token):
            operator_stack.append(token)
        elif is_operator(token):
            while (operator_stack and operator_stack[-1] != '(' and
                   (is_operator(operator_stack[-1]) and 
                    (precedence(operator_stack[-1]) > precedence(token) or
                    (precedence(operator_stack[-1]) == precedence(token) and is_left_associative(token))))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == ',':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses")
            operator_stack.pop()
            if operator_stack and is_function(operator_stack[-1]):
                output_queue.append(operator_stack.pop())
    
    while operator_stack:
        top = operator_stack.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses")
        output_queue.append(top)
    
    return output_queue

expression = tokenize(input("Enter an expression: "))
rpn = shunting_yard(expression)
print("Reverse Polish Notation:", rpn)
