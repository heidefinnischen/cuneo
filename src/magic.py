import re
import math
from decimal import Decimal, getcontext, InvalidOperation, ROUND_HALF_UP

# Set precision
getcontext().prec = 28

def sanitize_expression(expression):
    return re.sub(r'[\+\-\*/\^x√]+\s*$', '', expression)

def format_result(value) -> str:
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    value = round_to_9_places(value)
    abs_val = abs(value)

    if (abs_val != 0 and abs_val < Decimal("0.001")) or abs_val >= Decimal("1000000"):
        return format(value.normalize(), "E").replace("+0", "+").replace("-0", "-")
    s = format(value, 'f').rstrip('0').rstrip('.') if '.' in str(value) else str(value)
    return s

def round_to_9_places(val: Decimal) -> Decimal:
    if val.is_zero():
        return Decimal("0")
    return val.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)

def replace_superscripts(expr):
    superscript_map = {
        '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
        '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
    }

    result = ""
    i = 0
    while i < len(expr):
        if expr[i] in superscript_map:
            # Go backwards to find the base (number or closing parenthesis)
            j = len(result) - 1
            while j >= 0 and result[j] in "0123456789.":
                j -= 1
            if j >= 0 and result[j] == ')':
                # Walk back to the matching '('
                depth = 1
                k = j - 1
                while k >= 0:
                    if result[k] == ')':
                        depth += 1
                    elif result[k] == '(':
                        depth -= 1
                        if depth == 0:
                            break
                    k -= 1
                base = result[k:]
                result = result[:k]
            else:
                base = result[j + 1:]
                result = result[:j + 1]
            # Collect all superscript digits
            power = ""
            while i < len(expr) and expr[i] in superscript_map:
                power += superscript_map[expr[i]]
                i += 1
            result += f"{base}^{power}"
        else:
            result += expr[i]
            i += 1
    return result



def ast_to_string(node, percent_base=None):
    if isinstance(node, Number):
        return str(node.value)
    elif isinstance(node, Constant):
        return node.name
    elif isinstance(node, Percent):
        if percent_base is None:
            return f"({node.value} / 100)"
        return f"(({percent_base} * {node.value}) / 100)"
    elif isinstance(node, BinOp):
        left_str = ast_to_string(node.left)
        right_str = ast_to_string(node.right, percent_base=evaluate(node.left)
                                  if isinstance(node.right, Percent) else None)
        return f"({left_str} {node.op} {right_str})"
    elif isinstance(node, Function):
        return f"{node.name}({ast_to_string(node.arg)})"
    else:
        return "?"

# ---------------------
# 1. TOKENIZER
# ---------------------
def tokenize(expression):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?%?'),
        ('CONST',    r'\bpi\b|π'),
        ('FUNC',     r'sqrt|sin|cos|tan|log|abs'),
        ('SQRT',     r'√'),
        ('OP',       r'[+\-*/x^]'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    get_token = re.compile(tok_regex).match
    pos = 0
    tokens = []
    mo = get_token(expression, pos)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('PERCENT' if value.endswith('%') else 'NUMBER', value))
        elif kind in ('FUNC', 'CONST', 'SQRT', 'OP', 'LPAREN', 'RPAREN'):
            tokens.append((kind, value))
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character {value!r}')
        pos = mo.end()
        mo = get_token(expression, pos)
    return tokens

# ---------------------
# 2. AST NODES
# ---------------------
class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = Decimal(value)

class Constant(ASTNode):
    def __init__(self, name):
        if name == 'π':
            name = 'pi'
        self.name = name
        self.value = Decimal(str(math.pi))

class Percent(ASTNode):
    def __init__(self, value):
        self.value = Decimal(value)

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Function(ASTNode):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

# ---------------------
# 3. PARSER
# ---------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type=None, expected_val=None):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if expected_type and token[0] != expected_type:
                raise SyntaxError(f"Expected token type {expected_type}, got {token[0]}")
            if expected_val and token[1] != expected_val:
                raise SyntaxError(f"Expected token value {expected_val}, got {token[1]}")
            self.pos += 1
            return token
        return None

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        node = self.power()
        while self.peek()[1] in ('*', '/', 'x'):
            op = self.consume()[1]
            if op == 'x':
                op = '*'
            right = self.power()
            node = BinOp(node, op, right)
        return node

    def power(self):
        node = self.factor()
        while self.peek()[1] == '^':
            self.consume()
            right = self.factor()
            node = BinOp(node, '^', right)
        return node

    def factor(self):
        tok_type, tok_val = self.peek()
        if tok_type == 'NUMBER':
            self.consume()
            return Number(tok_val)
        elif tok_type == 'PERCENT':
            self.consume()
            return Percent(tok_val.rstrip('%'))
        elif tok_type == 'CONST':
            self.consume()
            return Constant(tok_val)
        elif tok_type == 'FUNC':
            self.consume()
            self.consume('LPAREN')
            arg = self.expr()
            self.consume('RPAREN')
            return Function(tok_val, arg)
        elif tok_type == 'SQRT':
            self.consume()
            arg = self.factor()
            return Function('sqrt', arg)
        elif tok_type == 'LPAREN':
            self.consume()
            node = self.expr()
            self.consume('RPAREN')
            return node
        else:
            raise SyntaxError(f"Unexpected token {tok_type}:{tok_val}")

# ---------------------
# 4. EVALUATOR
# ---------------------
def evaluate(node, percent_base=None):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, Constant):
        return node.value
    elif isinstance(node, Percent):
        if percent_base is None:
            raise ValueError("Percent used without a base value")
        return (node.value / Decimal("100")) * percent_base
    elif isinstance(node, BinOp):
        left_val = evaluate(node.left)
        right_val = evaluate(node.right, left_val if isinstance(node.right, Percent) else None)
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            return left_val / right_val
        elif node.op == '^':
            return left_val ** right_val
    elif isinstance(node, Function):
        arg_val = evaluate(node.arg)
        if node.name == 'sqrt':
            return arg_val.sqrt()
        elif node.name == 'sin':
            return Decimal(math.sin(float(arg_val)))
        elif node.name == 'cos':
            return Decimal(math.cos(float(arg_val)))
        elif node.name == 'tan':
            return Decimal(math.tan(float(arg_val)))
        elif node.name == 'log':
            return Decimal(math.log10(float(arg_val)))
        elif node.name == 'abs':
            return abs(arg_val)
        else:
            raise ValueError(f"Unknown function {node.name}")

# ---------------------
# 5. TEST CASES
# ---------------------
expressions = [
    "5 + 50%",
    "100 - 25%",
    "10 * 50%",
    "10 x 50%",
    "sqrt(16)",
    "√16",
    "5 + sqrt(49)",
    "(5 + 5) * 2",
    "100 + 10% + 5%",
    "2 ^ 8",
    "sin(0)",
    "cos(0)",
    "tan(0)",
    "log(1000)",
    "abs(-123)",
    "pi",
    "2 * pi",
    "2²",
    "3³",
    "10¹",
    "10² + 2",
    "(1 + 2)³",
]

results = []
for expr in expressions:
    try:
        expr = replace_superscripts(expr)
        sanitized = sanitize_expression(expr)
        tokens = tokenize(sanitized)
        ast = Parser(tokens).parse()
        result = evaluate(ast)
        results.append((expr, format_result(result)))
    except Exception as e:
        results.append((expr, f"Error: {e}"))

for expr, res in results:
    print(f"{expr} = {res}")

