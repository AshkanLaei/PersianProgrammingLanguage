#!/usr/bin/env python3
import sys
import os
from sly import Lexer, Parser

class PPLLexer(Lexer):
    tokens = {
            FROM, DO, RUN, RAW_INPUT,
            NUM_INPUT, EQEQ, SHOMARANDE, NAME, NUMBER,
            STRING, IF, THEN, ELSE, FOR, TO, MEANS, PRINT
    }
    ignore = '\t '

    literals = { '=', '+', '-', '*', '/', '(', ')', ',', ';', '.' }

    # Define tokens
    IF = r'اگر'
    THEN = r'باشد آنگاه'
    ELSE = r'وگرنه'
    FROM = r'از'
    DO = r'انجام بده'
    FOR = r'برای'
    RUN = r'را اجرا کن'
    TO = r'تا'
    MEANS = r'یعنی'
    EQEQ = r'برابر'
    SHOMARANDE = r'شمارنده'
    RAW_INPUT = r'ورودی'
    NUM_INPUT = r'عددگیر'
    NAME = r'[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی‌]+'
    STRING = r'"(""|.)*?"'
    PRINT = r"چاپ_کن"

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*', r'//.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class PPLParser(Parser):
    tokens = PPLLexer.tokens

    precedence = (
        ('left', '.'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    @_('FOR NAME FROM expr TO expr DO statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', ('var_assign', p.NAME, p.expr0), p.expr1), p.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, p.statement0, p.statement1)

    @_('NAME MEANS statement')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME RUN')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('expr SHOMARANDE expr')
    def condition(self, p):
        return ('condition_shomarande', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr "." expr')
    def expr(self, p):
        return ('addstr', p.expr0, p.expr1)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('RAW_INPUT')
    def expr(self, p):
        return ('raw_input',)

    @_('NUM_INPUT')
    def expr(self, p):
        return ('num_input',)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return ('str', p.STRING)
    
    @_('PRINT expr')
    def expr(self, p):
        return ('print', p.expr)

class PPLExecute(object):
    def __init__(self, tree, env, output=print, input_=input):
        # output:
        #  It must be one of these:
        #   1. callable with at least one argument
        #   2. an instance of Python's list
        #  In case 1: The callable is called with output of
        #             execution of print(). Note that 
        #             the return value of the callable is discarded.
        #             The only argument passed to output has a type of 
        #             string.
        #  In case 2: Everytime print() is called, the result
        #             is appended to tail of list.
        # input_:
        #  It must be a callable with argument required.
        #  input_ is called with no arguments and MUST return
        #  a string.

        self.output = output
        if callable(self.output):
            self._out = self.output
        elif isinstance(output, list):
            self._out = self.output.append
        else:
            raise ValueError("output is not callable nor an instance of list")

        if not callable(input_):
            raise ValueError("input_ is not callable")
        self.input_ = input_
        
        self.env = env
        result = self.walk_tree(tree)
        if result is not None and isinstance(result, int):
            self._out(result)
        if isinstance(result, str) and result[0] == '"':
            self._out(result)

    def walk_tree(self, node):
        if isinstance(node, int) or isinstance(node, str) or node is None:
            return node
        if node[0] in [ 'num', 'str' ]:
            return node[1]
        if node[0] == 'raw_input':
            return '"' + self.input_() + '"'
        if node[0] == 'num_input':
            in_ = self.input_()
            if in_.isdigit():
                return int(in_)
            else:
                return 0
        if node[0] == 'if_stmt':
            result = self.walk_tree(node[1])
            if result:
                return self.walk_tree(node[2])
            if node[3]:
                return self.walk_tree(node[3])
        if node[0] == 'condition_eqeq':
            return self.walk_tree(node[1]) == self.walk_tree(node[2])
        if node[0] == 'condition_shomarande':
            return self.walk_tree(node[2]) % self.walk_tree(node[1]) == 0
        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]
        if node[0] == 'fun_call':
            try:
                return self.walk_tree(self.env[node[1]])
            except LookupError:
                self._out(f'undefined function \'{node[1]}\'')
                return 0
        if node[0] == 'addstr':
            return str(self.walk_tree(node[1])) + str(self.walk_tree(node[2]))
        elif node[0] == 'add':
            if type(node[1]) == str and node[1].isdigit():
                return int(self.walk_tree(node[1])) + int(self.walk_tree(node[2]))
            else:
                return 0
        elif node[0] == 'sub':
            if type(node[1]) == str and node[1].isdigit():
                return int(self.walk_tree(node[1])) - int(self.walk_tree(node[2]))
            else:
                return 0
        elif node[0] == 'mul':
            if type(node[1]) == str and node[1].isdigit():
                return int(self.walk_tree(node[1])) * int(self.walk_tree(node[2]))
            else:
                return 0
        elif node[0] == 'div':
            if type(node[1]) == str and node[1].isdigit():
                return int(self.walk_tree(node[1])) // int(self.walk_tree(node[2]))
            else:
                return 0
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walk_tree(node[2])
            return node[1]
        if node[0] == 'var':
            if node[1] in self.env:
                return self.env[node[1]]
            else:
                self._out('undefined variable \'{node[1]}\'')
                return 0
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walk_tree(node[1])
                loop_counter = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]
                for i in range(loop_counter, loop_limit + 1):
                    self.env[loop_setup[0]] = i
                    res = self.walk_tree(node[2])
                    if res is not None:
                        self._out(res)
        if node[0] == 'for_loop_setup':
            return (self.walk_tree(node[1]), self.walk_tree(node[2]))
        if node[0] == 'print':
            result = self.walk_tree(node[1])
            self._out(result)
            return result

if __name__ == '__main__':
    lexer = PPLLexer()
    parser = PPLParser()
    env = {}
    if len(sys.argv) < 2:
        while True:
            terminal = input('فردوسی >>> ')
            if terminal in ("exit", "quit"):
                break
            else:
                tokens = lexer.tokenize(terminal)
                tree = parser.parse(tokens)
                PPLExecute(tree, env)
    else:
        if not os.path.exists(sys.argv[1]):
            print("این فایل وجود ندارد")
            sys.exit(1)
        if os.path.isdir(sys.argv[1]):
            print("این یک پوشه هست و نه فایل")
            sys.exit(1)
        with open(sys.argv[1], encoding="utf-8") as fp:
            line = "# somecomment"
            while line:
                try:
                    tokens = lexer.tokenize(line)
                    tree = parser.parse(tokens)
                    PPLExecute(tree, env)
                    line = fp.readline()
                except:
                    print(f"خطا در خط: {line}")
                    sys.exit(1)
