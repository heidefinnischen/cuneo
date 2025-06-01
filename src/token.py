import re

token_spec = [

]

def tokenize(expression):
    token_pattern = re.compile(r"""
        (?P<PERCENT>\d+(\.\d+)?%)
      | (?P<NUMBER>\d+(\.\d+)?)
      | (?P<OPERATION>[+\-*/()])
      | (?P<FUNCTION>[a-zA-Z_]\w*)
      | (?P<WHITESPACE>\s+)
    """, re.VERBOSE)

    tokens = []
    for match in token_pattern.finditer(expression):
        kind = match.lastgroup
        value = match.group()

        if kind == "WHITESPACE":
            continue # Ignore
        tokens.append((kind, value))

    return tokens
        
