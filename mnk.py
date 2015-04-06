#!/usr/bin/env python
# encoding: utf-8
import os
import re


def tablify(g, w):
	# where g is a list of lists (rows) and w is the additional width of each cell 
	# remove bash colors from string
	def n(q): return re.compile(r'\x1b[^m]*m').sub("", str(q))
	
	# adapt cell content
	def sify(q, p):
		l = (p - len(n(q)))
		return " " * ((l // 2) + (l % 2)) + str(q) + " "*(l // 2)
	
	# standard width of a cell in table = width of largest content in list of rows + additional width
	s = max([len(n(y)) for x in g for y in x])+w

	print "+"+("+".join(["-"*s for x in g[0]]))+"+"
	for row in g:
		print "|"+("|".join([sify(x, s) for x in row]))+"|"
		print "+"+("+".join(["-"*s for x in row]))+"+"

def clear(): os.system(['clear', 'cls'][os.name == 'nt'])


class Game:
	def __init__(self, m, n, k):
		self.tab = {(m * y) + (x + 1): None for x in xrange(m) for y in xrange(n)}
		self.m = m
		self.k = k
		
	def check(self):
	# check if some player has won
		nowin, winner = 1, None
		
		def mod_rval():
			if None not in cl.values():
				return (sum(cl.values()) % self.k), (self.tab[i])
			else:
				return nowin, winner
		
		for i, v in self.tab.iteritems():
			i_isbottom = (i // self.m + (i % self.m > 0)) - self.k >= 0
			i_isright = (i % self.m + ((i % self.m == 0) * self.m)) - self.k >= 0
			i_isleft = (i % self.m + ((i % self.m == 0) * self.m)) + self.k - 1 <= self.m
			# horizontal condition
			if nowin != 0 and i_isright:								
				cl = {i - x: self.tab[i - x] for x in range(self.k)}
				nowin, winner = mod_rval()
				# top_left-bottom_right diagonal condition
				if nowin != 0 and i_isbottom:	
					cl = {i-((x * self.m) + x): self.tab[i - ((x * self.m) + x)] for x in range(self.k) }
					nowin, winner = mod_rval()
			# vertical condition	
			if nowin != 0 and i_isbottom:	
				cl = {i - (self.m * x): self.tab[i - (self.m * x)] for x in range(self.k)}
				nowin, winner = mod_rval()
				# bottom_left-top_right diagonal condition
				if nowin != 0 and i_isleft:
					cl = {i - ((x * self.m) - x): self.tab[i - ((x * self.m) - x)] for x in range(self.k)}
					nowin, winner = mod_rval()
		
		# return is_there_a_winner, who_is_the_winner, what_is_the_last/winning_line 
		return not bool(nowin), winner, cl	
	
	def s(self, a, b=""):
		# turn boolean values to O and X; higlight following value b - X is the first player, linked to the value True
		return ["\033[7m" + b + " X \033[0m", "\033[7m" + b + " O \033[0m"][a]
		
	def iput(self, pl):
		# input routine
		acceptable = [k for k, v in self.tab.iteritems() if v is None]
		if len(acceptable) > 0:
			noinput = True
			print "Make your move, player " + self.s(pl) + "   "
			while noinput and len(acceptable) > 0:
				iput = raw_input("==> ")
				try:
					iput = int(iput)
					if iput in acceptable:
						noinput = False
					else:
						print "The cell is taken or unavailabe. Please choose another one."
				except:
					print "Type a number, please."
			return iput
		else:
			return False

	def oput(self, cl={}):	# cl is the set of highlighted elements 
		def o_select(i, v):
			# return numbers for unselected positions, return value for selected positions, highlight selected positions in cl
			return i if v is None else [self.s(v), self.s(v, "\033[5m")][i in cl.keys()]
		out = [o_select(i, v) for i, v in self.tab.iteritems()]
		# break out into m long tuples and turn those tuple into lists; store lists in out
		out = [list(x) for x in zip(*[iter(out)]*self.m)]
		return tablify(out, 4)
		
	def game(self):
		turn = 0
		end = False
		self.oput()
		while not end:
			pl = (turn % 2)
			mo = self.iput(pl)
			clear()
			if not mo:
				print "The game is over"
				end, val = True, None
			else:
				self.tab[mo] = bool(pl % 2)
				turn += 1
				end, val, cl = self.check()
			self.oput()
		if end:
			if val is None:
				print "Nobody wins"
			else:
				clear()
				print "Player " + str(self.s(val)) + " wins."
				self.oput(cl)


class Sttng:
	def __init__(self):
		print "Please enter N,M and K for your N,M,K game.\n"
		notok = True
		while notok:
			iput = raw_input("Enter N,M,K separated by a comma (or another character to separate your numbers).\nRemember: K must be equal or lesser than N and M.\n")
			nmk = list()
			try:
				sep = 0
				for i in list(iput):
					try:
						nmk.append(int(i))
					except:
						sep += 1
				if (nmk[2] <= nmk[0]) and (nmk[2] <= nmk[1]) and (sep > 1):
					notok = False
					self.nmk = nmk
				else:
					clear()
					msg = "\nNot enough separators. Please, retry." if sep < 2 else "\nWrong numbers. Plase, retry."
					print msg
			except:
				print "\nSomething went wrong. Plase, retry."


def main():
	print "N,M,K GAME\n"
	a = Sttng()
	Game(a.nmk[0], a.nmk[1], a.nmk[2]).game()
	
if __name__ == '__main__':
	try:
		main()
	except:
		print "-----------------------"
		print "Please, run the script in terminal."
