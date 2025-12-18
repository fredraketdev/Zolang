# Just run the code to start!

import re
import random

# Token types
TOONTRANS = 'TOON.TRANSLATE'
ZOLANG = 'ZOLANG'
GREATER = 'GROTER'
LESS = 'KLEINER'
EQUAL = 'GELIJK'
NOT_EQUAL = 'NIET_GELIJK'
GETAL = 'GETAL'
TEKST = 'TEKST'
ALS = 'ALS'
DAN = 'DAN'
ANDERS = 'ANDERS'
LBRACE = 'LBRACE'   # {
RBRACE = 'RBRACE'   # }
NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MIN'
TIMES = 'MAAL'
DIVIDED = 'GEDEELD'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
SET = 'VERANDER'
TO = 'NAAR'
IDENTIFIER = 'IDENTIFIER'
TOON = 'TOON'
VRAAG = 'VRAAG'
STRING = 'STRING'


def tokenize(code):
    tokens = []
    # Remove comments: everything after // on a line
    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        if '//' in line:
            line = line.split('//', 1)[0]
        cleaned_lines.append(line)
    code = '\n'.join(cleaned_lines)

    i = 0
    while i < len(code):
        char = code[i]
        if char.isspace():
            i += 1
            continue
        elif char == '"':
            i += 1
            start = i
            while i < len(code) and code[i] != '"':
                i += 1
            if i >= len(code):
                raise SyntaxError("\033[91mUnterminated string \033[0m")
            value = code[start:i]
            tokens.append((STRING, value))
            i += 1  # skip closing "
        elif char == '(':
            tokens.append((LPAREN, char))
            i += 1
        elif char == ')':
            tokens.append((RPAREN, char))
            i += 1
        elif char == '{':
            tokens.append((LBRACE, char))
            i += 1
        elif char == '}':
            tokens.append((RBRACE, char))
            i += 1
        else:
            start = i
            while i < len(code) and not code[i].isspace() and code[i] not in '(){}':
                i += 1
            word = code[start:i].strip().lower()
            if not word:
                continue
            if word.isdigit():
                tokens.append((NUMBER, int(word)))
            elif word == 'plus':
                tokens.append((PLUS, word))
            elif word == 'min':
                tokens.append((MINUS, word))
            elif word == 'maal':
                tokens.append((TIMES, word))
            elif word == 'gedeeld':
                tokens.append((DIVIDED, word))
            elif word == 'verander':
                tokens.append((SET, word))
            elif word == 'naar':
                tokens.append((TO, word))
            elif word == 'toon':
                tokens.append((TOON, word))
            elif word == 'vraag':
                tokens.append((VRAAG, word))
            elif word == 'getal':
                tokens.append((GETAL, word))
            elif word == 'tekst':
                tokens.append((TEKST, word))
            elif word == 'als':
                tokens.append((ALS, word))
            elif word == 'dan':
                tokens.append((DAN, word))
            elif word == 'anders':
                tokens.append((ANDERS, word))
            elif word == 'groter':
                tokens.append((GREATER, word))
            elif word == 'kleiner' or word == 'minder':
                tokens.append((LESS, word))
            elif word == 'gelijk':
                tokens.append((EQUAL, word))
            elif word == 'niet_gelijk':
                tokens.append((NOT_EQUAL, word))
            elif word == 'zolang':
                tokens.append((ZOLANG, word))
            elif word == 'toon.translate':
                tokens.append((TOONTRANS, word))
            elif word[0].isalpha() and word.replace('_', '').isalnum():
                tokens.append((IDENTIFIER, word))
            else:
                raise SyntaxError(f"\033[91mUnknown token: '{word}' \033[0m")
    return tokens


# --- PARSER (all functions use `pos` and return (ast, new_pos)) ---

def parse_program(tokens):
    pos = 0
    statements = []
    while pos < len(tokens):
        if tokens[pos][0] == ALS:
            stmt, pos = parse_if(tokens, pos)
            statements.append(stmt)
        elif tokens[pos][0] == ZOLANG:
            stmt, pos = parse_while(tokens, pos)
            statements.append(stmt)
        elif tokens[pos][0] == SET:
            stmt, pos = parse_assignment_from_tokens(tokens, pos)
            statements.append(stmt)
        elif tokens[pos][0] == TOON:
            stmt, pos = parse_print_from_tokens(tokens, pos)
            statements.append(stmt)
        elif tokens[pos][0] == TOONTRANS:
            stmt, pos = parse_eastereggs_from_tokens(tokens, pos)
            statements.append(stmt)
        elif tokens[pos][0] == VRAAG:
            stmt, pos = parse_input_from_tokens(tokens, pos)
            statements.append(stmt)
        else:
            # Standalone expression (e.g., for future use)
            expr, pos = parse_comparison(tokens, pos)
            statements.append(('EXPR', expr))
    return ('PROGRAM', statements)


def parse_comparison(tokens, pos):
    """Parses: arith_expr ( (GREATER|LESS|EQUAL|NOT_EQUAL) arith_expr )? """
    left, pos = parse_expr(tokens, pos)
    if pos < len(tokens) and tokens[pos][0] in (GREATER, LESS, EQUAL, NOT_EQUAL):
        op = tokens[pos][0]
        pos += 1
        right, pos = parse_expr(tokens, pos)
        return ('COMPARE', op, left, right), pos
    else:
        return left, pos


def parse_expr(tokens, pos):
    """Parses addition/subtraction"""
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] in (PLUS, MINUS):
        op = tokens[pos][0]
        pos += 1
        right, pos = parse_term(tokens, pos)
        left = ('BINOP', op, left, right)
    return left, pos


def parse_term(tokens, pos):
    """Parses multiplication/division"""
    left, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos][0] in (TIMES, DIVIDED):
        op = tokens[pos][0]
        pos += 1
        right, pos = parse_factor(tokens, pos)
        left = ('BINOP', op, left, right)
    return left, pos


def parse_factor(tokens, pos):
    """Parses numbers, identifiers, strings, and parentheses"""
    if pos >= len(tokens):
        raise SyntaxError(f"\033[91mUnexpected end of input \033[0m")
    token_type, value = tokens[pos]
    if token_type == NUMBER:
        return ('NUMBER', value), pos + 1
    elif token_type == STRING:
        return ('STRING', value), pos + 1
    elif token_type == IDENTIFIER:
        return ('IDENTIFIER', value), pos + 1
    elif token_type == GETAL:
        pos += 1  # skip 'getal'
        if pos >= len(tokens) or tokens[pos][0] != LPAREN:
            raise SyntaxError(f"\033[91mExpected '(' after 'getal' \033[0m")
        pos += 1
        expr, pos = parse_comparison(tokens, pos)
        if pos >= len(tokens) or tokens[pos][0] != RPAREN:
            raise SyntaxError(f"\033[91mExpected ')' after 'getal(...)' \033[0m")
        pos += 1
        return ('TO_NUMBER', expr), pos

    elif token_type == TEKST:
        pos += 1  # skip 'tekst'
        if pos >= len(tokens) or tokens[pos][0] != LPAREN:
            raise SyntaxError("\033[91mExpected '(' after 'tekst' \033[0m")
        pos += 1
        expr, pos = parse_comparison(tokens, pos)
        if pos >= len(tokens) or tokens[pos][0] != RPAREN:
            raise SyntaxError("\033[91mExpected ')' after 'tekst(...)' \033[0m")
        pos += 1
        return ('TO_STRING', expr), pos
    elif token_type == VRAAG:
        pos += 1
        prompt_expr, pos = parse_comparison(tokens, pos)
        return ('INPUT', prompt_expr), pos
    elif token_type == LPAREN:
        pos += 1
        expr, pos = parse_comparison(tokens, pos)  # allow comparisons inside parens
        if pos >= len(tokens) or tokens[pos][0] != RPAREN:
            raise SyntaxError("\033[91mExpected ')' \033[0m")
        return expr, pos + 1
    else:
        raise SyntaxError(f"\033[91mUnexpected token: {tokens[pos]} \033[0m")


def parse_assignment_from_tokens(tokens, pos):
    if tokens[pos][0] != SET:
        raise SyntaxError(f"\033[91mExpected 'verander', got '{tokens[pos][1]}' \033[0m")
    pos += 1
    if pos >= len(tokens) or tokens[pos][0] != IDENTIFIER:
        raise SyntaxError(f"\033[91mExpected variable name after 'verander', got '{tokens[pos][1]}' \033[0m")
    var_name = tokens[pos][1]
    pos += 1
    if pos >= len(tokens) or tokens[pos][0] != TO:
        raise SyntaxError(f"\033[91mExpected 'naar' after variable name, got '{tokens[pos][1]}' \033[0m")
    pos += 1
    expr, pos = parse_comparison(tokens, pos)  # allow  x = a > b
    return ('ASSIGN', var_name, expr), pos


def parse_print_from_tokens(tokens, pos):
    if tokens[pos][0] != TOON:
        raise SyntaxError(f"\033[91mExpected 'toon', got '{tokens[pos][1]}' \033[0m")
    pos += 1
    expr, pos = parse_comparison(tokens, pos)
    return ('PRINT', expr), pos


def parse_eastereggs_from_tokens(tokens, pos):
    if tokens[pos][0] != TOONTRANS:
        raise SyntaxError(f"\033[91mExpected 'toon.translate', got '{tokens[pos][1]}' \033[0m")
    pos += 1
    return ('PRINT.TRANSLATE',), pos


def parse_input_from_tokens(tokens, pos):
    if tokens[pos][0] != VRAAG:
        raise SyntaxError(f"\033[91mExpected 'vraag', got '{tokens[pos][1]}' \033[0m")
    pos += 1
    expr, pos = parse_comparison(tokens, pos)
    return ('INPUT', expr), pos
    


def parse_if(tokens, pos):
    if pos >= len(tokens) or tokens[pos][0] != ALS:
        raise SyntaxError(f"\033[91mExpected 'als', got '{tokens[pos][1]}' \033[0m")
    pos += 1
    condition, pos = parse_comparison(tokens, pos)
    if pos >= len(tokens) or tokens[pos][0] != DAN:
        raise SyntaxError(f"\033[91mExpected 'dan' after condition, got '{tokens[pos][1]}' \033[0m")
    pos += 1
    if pos >= len(tokens) or tokens[pos][0] != LBRACE:
        raise SyntaxError("\033[91mExpected '{' after 'dan' \033[0m")
    pos += 1

    then_body = []
    while pos < len(tokens) and tokens[pos][0] != RBRACE:
        if tokens[pos][0] == ALS:
            stmt, pos = parse_if(tokens, pos)
            then_body.append(stmt)
        elif tokens[pos][0] == ZOLANG:
            stmt, pos = parse_while(tokens, pos)
            then_body.append(stmt)
        elif tokens[pos][0] == SET:
            stmt, pos = parse_assignment_from_tokens(tokens, pos)
            then_body.append(stmt)
        elif tokens[pos][0] == TOON:
            stmt, pos = parse_print_from_tokens(tokens, pos)
            then_body.append(stmt)
        elif tokens[pos][0] == TOONTRANS:
                stmt, pos = parse_eastereggs_from_tokens(tokens, pos)
                then_body.append(stmt)
        elif tokens[pos][0] == VRAAG:
            stmt, pos = parse_input_from_tokens(tokens, pos)
            then_body.append(stmt)
        else:
            expr, pos = parse_comparison(tokens, pos)
            then_body.append(('EXPR', expr))
    if pos >= len(tokens):
        raise SyntaxError("\033[91mExpected '}' \033[0m")
    pos += 1  # skip RBRACE

    else_body = []
    if pos < len(tokens) and tokens[pos][0] == ANDERS:
        pos += 1
        if pos >= len(tokens) or tokens[pos][0] != LBRACE:
            raise SyntaxError("\033[91mExpected '{' after 'anders' \033[0m")
        pos += 1
        while pos < len(tokens) and tokens[pos][0] != RBRACE:
            if tokens[pos][0] == ALS:
                stmt, pos = parse_if(tokens, pos)
                else_body.append(stmt)
            elif tokens[pos][0] == ZOLANG:
                stmt, pos = parse_while(tokens, pos)
                else_body.append(stmt)
            elif tokens[pos][0] == SET:
                stmt, pos = parse_assignment_from_tokens(tokens, pos)
                else_body.append(stmt)
            elif tokens[pos][0] == TOON:
                stmt, pos = parse_print_from_tokens(tokens, pos)
                else_body.append(stmt)
            elif tokens[pos][0] == TOONTRANS:
                stmt, pos = parse_eastereggs_from_tokens(tokens, pos)
                else_body.append(stmt)
            elif tokens[pos][0] == VRAAG:
                stmt, pos = parse_input_from_tokens(tokens, pos)
                else_body.append(stmt)
            else:
                expr, pos = parse_comparison(tokens, pos)
                else_body.append(('EXPR', expr))
        if pos >= len(tokens):
            raise SyntaxError("\033[91mExpected '}' in else block \033[0m")
        pos += 1  # skip RBRACE

    return ('IF', condition, then_body, else_body), pos


def parse_while(tokens, pos=0):
    if pos >= len(tokens) or tokens[pos][0] != ZOLANG:
        raise SyntaxError(f"\033[91mExpected 'zolang', got '{tokens[pos][1]}' \033[0m")
    pos += 1
    condition, pos = parse_comparison(tokens, pos)
    if pos >= len(tokens) or tokens[pos][0] != DAN:
        raise SyntaxError(f"\033[91mExpected 'dan' after condition, got '{tokens[pos][1]}' \033[0m")
    pos += 1
    if pos >= len(tokens) or tokens[pos][0] != LBRACE:
        raise SyntaxError("\033[91mExpected '{' after 'dan' \033[0m")
    pos += 1

    # Parse loop body
    body = []
    while pos < len(tokens) and tokens[pos][0] != RBRACE:
        if tokens[pos][0] == ALS:
            stmt, pos = parse_if(tokens, pos)
            body.append(stmt)
        elif tokens[pos][0] == ZOLANG:  # ← allow nested loops!
            stmt, pos = parse_while(tokens, pos)
            body.append(stmt)
        elif tokens[pos][0] == SET:
            stmt, pos = parse_assignment_from_tokens(tokens, pos)
            body.append(stmt)
        elif tokens[pos][0] == TOON:
            stmt, pos = parse_print_from_tokens(tokens, pos)
            body.append(stmt)
        elif tokens[pos][0] == TOONTRANS:
            stmt, pos = parse_eastereggs_from_tokens(tokens, pos)
            body.append(stmt)
        elif tokens[pos][0] == VRAAG:
            stmt, pos = parse_input_from_tokens(tokens, pos)
            body.append(stmt)
        else:
            expr, pos = parse_comparison(tokens, pos)
            body.append(('EXPR', expr))
    if pos >= len(tokens):
        raise SyntaxError("\033[91mExpected '}' \033[0m")
    pos += 1  # skip RBRACE

    return ('WHILE', condition, body), pos


# --- EVALUATOR ---

def evaluate(ast, env):
    node_type = ast[0]
    if node_type == 'PROGRAM':
        for stmt in ast[1]:
            evaluate(stmt, env)
    elif node_type == 'PRINT':
        value = evaluate(ast[1], env)
        print(">>>", value)
    elif node_type == 'PRINT.TRANSLATE':
        value = random.randrange(2)
        if value == 0:
            value2 = "\033[96mYou found easter egg 1! \033[0m"
            value = """Translate 'ha
ah
ha
ah
ah
ha
ha
ha
ha
ha
ha
ha
ha
a' 
from French to anny language you want and press the 'listen' button from French."""
        if value == 1:
            value2 = "\033[96mYou found easter egg 2! \033[0m"
            value = """Translate 'seal pushed me'
from English to French and press the 'listen' button from French."""
        print(">>>", value2, f"\033[92m{value} \033[0m")
    elif node_type == 'INPUT':
        prompt = evaluate(ast[1], env)
        if len(prompt) > 0:
            return input(f"{prompt} \n\033[91m>>> \033[0m")
        else:
            return input("\033[91m>>> \033[0m")
    elif node_type == 'ASSIGN':
        var_name = ast[1]
        value = evaluate(ast[2], env)
        env[var_name] = value
    elif node_type == 'IF':
        condition = evaluate(ast[1], env)
        if condition:
            for stmt in ast[2]:
                evaluate(stmt, env)
        else:
            for stmt in ast[3]:
                evaluate(stmt, env)
    elif node_type == 'WHILE':
        condition_ast = ast[1]
        body = ast[2]
        while True:
            condition_value = evaluate(condition_ast, env)
            if not condition_value:
                break
            for stmt in body:
                evaluate(stmt, env)
    elif node_type == 'EXPR':
        # Evaluate for side effects (none in this language yet)
        evaluate(ast[1], env)
    elif node_type == 'TO_NUMBER':
        value = evaluate(ast[1], env)
        try:
            # Try to convert to int, fall back to float
            if isinstance(value, str):
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            elif isinstance(value, (int, float)):
                return value
            else:
                raise ValueError(f"\033[91mCannot convert {repr(value)} to number \033[0m")
        except (ValueError, TypeError):
            raise RuntimeError(f"\033[91mCannot convert '{value}' to number \033[0m")

    elif node_type == 'TO_STRING':
        value = evaluate(ast[1], env)
        return str(value)
    elif node_type == 'NUMBER':
        return ast[1]
    elif node_type == 'STRING':
        return ast[1]
    elif node_type == 'IDENTIFIER':
        name = ast[1]
        if name in env:
            return env[name]
        else:
            raise NameError(f"\033[91mVariable '{name}' is not defined \033[0m")
    elif node_type == 'COMPARE':
        op, left, right = ast[1], ast[2], ast[3]
        lval = evaluate(left, env)
        rval = evaluate(right, env)
        if op == GREATER:
            return lval > rval
        elif op == LESS:
            return lval < rval
        elif op == EQUAL:
            return lval == rval
        elif op == NOT_EQUAL:
            return lval != rval
        else:
            raise RuntimeError(f"\033[91mUnknown comparison operator: {op} \033[0m")
    elif node_type == 'BINOP':
        op, left, right = ast[1], ast[2], ast[3]
        lval = evaluate(left, env)
        rval = evaluate(right, env)
        if op == PLUS:
            if isinstance(lval, (int, float)) and isinstance(rval, (int, float)):
                return lval + rval
            return str(lval) + str(rval)
        elif op == MINUS:
            if not isinstance(lval, (int, float)) or not isinstance(rval, (int, float)):
                raise TypeError("\033[91mCan only subtract numbers \033[0m")
            return lval - rval
        elif op == TIMES:
            if isinstance(lval, str) and isinstance(rval, int):
                return lval * rval
            if isinstance(rval, str) and isinstance(lval, int):
                return rval * lval
            if isinstance(lval, (int, float)) and isinstance(rval, (int, float)):
                return lval * rval
            raise TypeError("\033[91mInvalid types for 'maal' \033[0m")
        elif op == DIVIDED:
            if not isinstance(lval, (int, float)) or not isinstance(rval, (int, float)):
                raise TypeError("\033[91mCan only divide numbers \033[0m")
            if rval == 0:
                raise ZeroDivisionError("\033[91mDivision by zero \033[0m")
            return lval / rval
        else:
            raise RuntimeError(f"\033[91mUnknown operator: {op} \033[0m")
    else:
        raise RuntimeError(f"\033[91mUnknown AST node: {node_type} \033[0m")


# --- DEMO ---
if __name__ == "__main__":
    env = {}
    print("\033[94m")
    print(r"""  _____     _                   
 |__  /___ | | __ _ _ __   __ _ 
   / // _ \| |/ _` | '_ \ / _` |
  / /| (_) | | (_| | | | | (_| |
 /____\___/|_|\__,_|_| |_|\__, |
                          |___/ 
""")
    print("Welcome to zolang! Type your code (or 'stop' to end).\033[0m")
    while True:
        try:
            code = input("\033[92mzolang > \033[0m")
            if code.strip().lower() == 'stop':
                break
            if code.strip():
                tokens = tokenize(code)
                ast = parse_program(tokens)
                evaluate(ast, env)
        except Exception as e:
            print(e)
