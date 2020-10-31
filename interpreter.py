from sys import argv

from libs.sly import Lexer, Parser

class PPLLexer(Lexer):
	tokens = { FROM, DO, RUN, RAW_INPUT, NUM_INPUT, EQEQ, SHOMARANDE, NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, TO, MEANS }
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
	NAME = r'[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+'
	STRING = r'"(""|.)*?"'

	@_(r'\d+')
	def NUMBER(self, t):
		t.value = int(t.value)
		return t

	@_(r'#.*')
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

class PPLExecute(object):
	def __init__(self, tree, env):
		self.env = env
		result = self.walk_tree(tree)
		if result is not None and isinstance(result, int):
			print(result)
		if isinstance(result, str) and result[0] == '"':
			print(result)

	def walk_tree(self, node):
		if isinstance(node, int) or isinstance(node, str) or node is None:
			return node
		if node[0] in [ 'num', 'str' ]:
			return node[1]
		if node[0] == 'raw_input':
			return '"' + input() + '"'
		if node[0] == 'num_input':
			try:
				return int(input())
			except TypeError:
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
				print('undefined function \'%s\'' % node[1])
				return 0
		if node[0] == 'addstr':
			return str(self.walk_tree(node[1])) + str(self.walk_tree(node[2]))
		elif node[0] == 'add':
			try:
				return int(self.walk_tree(node[1])) + int(self.walk_tree(node[2]))
			except TypeError:
				return 0
		elif node[0] == 'sub':
			try:
				return int(self.walk_tree(node[1])) - int(self.walk_tree(node[2]))
			except TypeError:
				return 0
		elif node[0] == 'mul':
			try:
				return int(self.walk_tree(node[1])) * int(self.walk_tree(node[2]))
			except TypeError:
				return 0
		elif node[0] == 'div':
			try:
				return int(self.walk_tree(node[1])) // int(self.walk_tree(node[2]))
			except TypeError:
				return 0
		if node[0] == 'var_assign':
			self.env[node[1]] = self.walk_tree(node[2])
			return node[1]
		if node[0] == 'var':
			try:
				return self.env[node[1]]
			except LookupError:
				print('undefined variable \'%s\'' % node[1])
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
						print(res)
		if node[0] == 'for_loop_setup':
			return (self.walk_tree(node[1]), self.walk_tree(node[2]))

if __name__ == '__main__':
	lexer = PPLLexer()
	parser = PPLParser()
	env = {}
	if len(argv) < 2:
		print('باید آدرس فایل برنامه را به‌عنوان آرگومنت به برنامه بدهید.')
	else :
		with open(argv[1], encoding="utf-8") as f:
			for line in f.read().splitlines():
				tokens = lexer.tokenize(line)
				tree = parser.parse(tokens)
				PPLExecute(tree, env)
