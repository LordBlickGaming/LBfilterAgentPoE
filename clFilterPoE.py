#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-


from clIniFile import xlist, hh
from os import path as ph
import re

compares = "< > = <= >= <>".split()
reCompares = re.compile(r"^(?:(?:"+r')|(?:'.join(compares)+r"))$", re.U)

reSectionDeco = re.compile(r"^\s*#\=+", re.U)
reSegDeco = re.compile(r"^\s*#\-+", re.U)

reHead = re.compile(r"^\s*#\s*.*Loot\s+Filter.*$", re.U)
reTOC = re.compile(r"^\s*#\s*\[WELCOME\]\s+TABLE\s+OF\s+CONTENTS\s+\+\s+QUICKJUMP\s+TABLE\s*$", re.U)
reThanks = re.compile(r"^\s*#\s*.*thanks.*$", re.U | re.I)
reGencSect = re.compile(r"^\s*#\s*\[\[(?P<sectID>\d+)\]\]\s*(?P<sectTxt>[\w\s\-\+,\(\)\!\:]+)$", re.U)

reSubSect = re.compile(r"^\s*#\s*\[(?P<ssectID>\d+)\]\s*(?P<ssectTxt>[\w\s\-\+,\(\)\!\:%\.\/\"]+)$", re.U)

reDiv = re.compile(r"^\s*#\s*(?P<divTxt>[\w\s\-\+,\(\)\!\:%\.\/\"]+)$", re.U)

Data_pass = "None"

_range = lambda _min, _max: tuple(range(_min, _max+1))
in_range = lambda _val, _min, _max: _val in _range(_min, _max)
_byte = _range(0, 255)
_byte = _range(0, 255)
_nan_byte = (None,)+_byte # not always needed
_ef_colors =  'Red Green Blue Brown White Yellow'.split
_ef_shapes = 'Circle Diamond Hexagon Square Star Triangle'.split
_ef_temp = (None, 'Temp')
cond_bool             = 1
cond_list             = 2
cond_list_multi       = 3
cond_match_re         = 4
cond_compare_or_space = 5
dcRarity = dict(map(reversed, (enumerate("Normal Magic Rare Unique".split()))))

conditions = (
	("ShaperItem",       cond_bool),
	("ElderItem",        cond_bool),
	("FracturedItem",    cond_bool),
	("SynthesisedItem",  cond_bool),
	("AnyEnchantment",   cond_bool),
	("ShapedMap",        cond_bool),
	("Corrupted",        cond_bool),
	("Identified",       cond_bool),
	("LinkedSockets",    cond_compare_or_space, _range(1, 6)),
	("Sockets",          cond_compare_or_space, _range(1, 6)),
	("MapTier",          cond_compare_or_space, (1, 20)),
	("Width",            cond_compare_or_space, (1, 2)),
	("Height",           cond_compare_or_space, _range(1, 4)),
	("Quality",          cond_compare_or_space, _range(1, 30)),
	("ItemLevel",        cond_compare_or_space, _range(1, 100)),
	("DropLevel",        cond_compare_or_space, _range(1, 100)),
	("Rarity",           cond_compare_or_space, dcRarity),
	("Class",            cond_list),
	("ElderMap",         cond_bool),
	("BaseType",         cond_list),
	("StackSize",        cond_compare_or_space, (1, 1000)),
	("SocketGroup",      cond_match_re,         r"^[RGBW]{1,6}$"),
	("GemLevel",         cond_compare_or_space, (1, 30)),
	("HasMod",           cond_list),
	("Prophecy",         cond_list),
	("HasEnchantment",   cond_list),
	("HasExplicitMod",   cond_list_multi),
	)
cond_raw = tuple(map(lambda n: n[0], conditions))
which_condition = lambda txt: cond_raw.index(txt)+1 if txt in cond_raw else 0
reCondition = re.compile(
	r"^\s*(?P<inactive>#?)\s*(?P<condition>(?:"\
	+r')|(?:'.join(cond_raw)\
	+r"))(?P<txtArgs>[^#]*)(?P<comment>#.*)?$", re.U)

actions = (
	("SetFontSize", _range(18, 45)), #(default: 32)
	#						R		G		B	 Alpha(Default is 255)
	("SetTextColor", _byte, _byte, _byte, _nan_byte),
	("SetBorderColor", _byte, _byte, _byte, _nan_byte),
	("SetBackgroundColor", _byte, _byte, _byte, _nan_byte),
	#						Choice			Volume
	("PlayAlertSound", _range(1, 16), _range(0, 300)),
	("DisableDropSound",),
	("MinimapIcon", _range(0, 2), _ef_colors, _ef_shapes),
	('PlayEffect', _ef_colors, _ef_temp),
	)
actn_raw = tuple(map(lambda n: n[0], actions))
which_action = lambda txt: actn_raw.index(txt)+1 if txt in actn_raw else 0
reAciton = re.compile(
	r"^\s*(?P<inactive>#?)\s*(?P<action>(?:"\
	+r')|(?:'.join(actn_raw)\
	+r"))(?P<txtArgs>[^#]*)(?P<comment>#.*)?$", re.U)

class rulePrims(xlist):
	'''
	Extended constant list of rows:
	  (command(str), (activity(bool), args(list), comment_spc, comment))
	 Empty command:
	  (command, None)
	'''
	def __init__(it, logger, commands, name, debug=True):
		xlist.__init__(it)
		it._p = logger
		it._d = logger if debug else _d
		it.name = name
		it.bWarning = True
		for command in commands:
			if name == "Condition" and(it.getCondType(command)==cond_compare_or_space):
				it.append((command+'_Hi', None))
				it.append((command+'_Lo', None))
			elif name == "Condition" and(it.getCondType(command)==cond_list_multi):
				lm = xlist()
				it.append((command+'_M', lm))
			else:
				it.append((command, None))
		it.keys =  tuple(map(lambda (key, value): key, it))

	has_key = lambda it, key: key in it.keys
	get_place = lambda it, key: it.keys.index(key)

	def __getitem__(it, key):
		if type(key) is int:
			return xlist.__getitem__(it, key)[1] # [0] is key…
		if it.has_key(key):
			return xlist.__getitem__(it, it.get_place(key))[1] # [0] is key…
		else:
			return None

	def __setkey(it, key, value):
		idx = it.get_place(key)
		it[idx] = key, value # call  numeric rewrite

	#!!! it[idx] = key, value !!!
	def __setitem__(it, key, value):
		# numeric rewrite - must have - not only recurency
		if type(key) is int:
			xlist.__setitem__(it, key, value)
			return
		elif it.has_key(key):
			idx = it.get_place(key)
			if it[idx] and(it.bWarning):
				print(it[idx], str(it.bWarning))
				it._d('\n')
				it._p("     Warning! Ugly overwriting %s „%s” during Data Work Status: >%s<:\n" % (it.name, key, Data_pass), 'tgWarn')
				it._p("        (%s)\n" % (', '.join(map(lambda x: str(x), it[idx]))), 'tgPhrase')
				it._p("      with\n", 'tgWarn')
				it._p("        (%s)\n" % (', '.join(map(lambda x: str(x), value))), 'tgPhrase')
			it[idx] = key, value # call  numeric rewrite
			return
		elif it.has_key(("%s_M" % key)):
			key_ = "%s_M" % key
			idx = it.get_place(key_)
			_lm = it[idx]
			#Ugly workaround - usually no need to edit conditions
			_lm.append(value)
			it[idx] = key, _lm # call  numeric rewrite
			return
		elif it.has_key(("%s_Hi" % key)) and(it.has_key(("%s_Lo" % key))):
			_iterable = it.getCondContainer(key)
			_hi = it[("%s_Hi" % key)]
			if _hi is not None:
				if isinstance(_iterable, dict):
					c_hi = _iterable[_hi[1][-1]]
				elif isinstance(_iterable, tuple):
					c_hi = int(_hi[1][-1])
			else:
					c_hi = -1
			_lo = it[("%s_Lo" % key)]
			if _lo is not None:
				if isinstance(_iterable, dict):
					c_lo = _iterable[_lo[1][-1]]
				elif isinstance(_iterable, tuple):
					c_lo = int(_lo[1][-1])
			else:
					c_lo = -1
			if isinstance(_iterable, dict):
				c_val = _iterable[value[1][-1]]
			elif isinstance(_iterable, tuple):
				c_val = int(value[1][-1])
			if c_hi==c_lo:
				if c_val<c_lo:
					it.__setkey(key+'_Lo', value)
					return
				elif c_val>c_hi:
					it.__setkey(key+'_Hi', value)
					return
				else:
					return
			elif c_hi>c_val>c_lo:
				it.__setkey(key+'_Lo', value)
				return
			elif c_val>c_hi>c_lo:
				it.__setkey(key+'_Lo', it[key+'_Hi'])
				it.__setkey(key+'_Hi', value)
				return
			elif c_hi>c_lo>c_val:
				it.__setkey(key+'_Hi', it[key+_Lo])
				it.__setkey(key+'_Lo', value)
				return
			else:
				return
		else:
			return

	leads = "activity args comment_spc comment".split()

	def has_lead(it, command):
		if not(it.has_key(command)):
			return False
		row = it[command]
		if row and(len(row)==4):
			return True
		return False

	def get_lead(it, command, lead):
		if not(it.has_lead(command)) or lead not in it.leads:
			return -1
		idx = it.leads.index(lead)
		return it[command][idx]

	def set_lead(it, command, lead, value):
		if not(it.has_lead(command)) or lead not in it.leads:
			return False
		idx = it.leads.index(lead)
		if idx==0:
			leading_left = ()
		else:
			leading_left = it[command][:idx]
		if idx==3:
			leading_right = ()
		else:
			leading_right = it[command][idx+1:]
		it[command] = leading_left + (value, ) + leading_right
		if len(it[command])!=4:
			it._p("Got trouble with set_lead !\n\tleft:", 'tgErr')
			it._p(("%s" % str(leading_left)), 'tgPhrase')
			it._p("\n\tright:", 'tgErr')
			it._p((" %s\n" % str(leading_right)), 'tgPhrase')
		return True

	get_args = lambda it, command: it.get_lead(command, 'args')
	set_args = lambda it, command, arg_tuple: it.set_lead(command, 'args', arg_tuple) #need tuple check…

	def replace_args(it, command, arg_tuple):
		it.bWarning = False
		it.set_args(command, arg_tuple)
		it.bWarning = True

	def activate(it, key):
		it.bWarning = False
		it.set_lead(key, 'activity', True)
		it.bWarning = True

	def deactivate(it, key):
		it.bWarning = False
		it.set_lead(key, 'activity', False)
		it.bWarning = True

	def _st_ln(it, command, activity, args, comment_spc, comment):
		txt_st = ''
		txt_st += "%s\t%s " % (('#', '')[activity], command)
		txt_st += "%s" % ' '.join(map(lambda x: str(x), args))
		fill = len(txt_st)
		if comment_spc and(comment):
			spc_left = comment_spc-fill
			if spc_left>0:
				txt_st += ' '*spc_left
			txt_st += "#%s" % comment
		txt_st += '\n'
		return txt_st

	def _st(it, active=True):
		txt_st = ''
		for command in it.keys:
			if not(it[command]):
				continue
			if command[-2:]=='_M':
				for activity, args, comment_spc, comment in it[command]:
					if not(active):
						activity = False
					txt_st += it._st_ln(command[:-2], activity, args, comment_spc, comment)
			elif command[-3:] in "_Hi _Lo".split():
				activity, args, comment_spc, comment = it[command]
				if not(active):
					activity = False
				txt_st += it._st_ln(command[:-3], activity, args, comment_spc, comment)
			else:
				activity, args, comment_spc, comment = it[command]
				if not(active):
					activity = False
				txt_st += it._st_ln(command, activity, args, comment_spc, comment)
		return txt_st

	def argtuple(it, txt):
		from shlex import shlex as shx
		argspt = shx(txt.strip())
		argspt.wordchars += "µΩ!@#$%^&*+-‐=.,;~/()<>[]"
		argspt.commenters = ''
		return tuple(argspt)


class ruleConditions(rulePrims):

	def _ld(it, condition, bActive, txtArgs, comment_spc, comment):
		args = it.argtuple(txtArgs)
		#TODO: Validate args
		it[condition] =  bActive, args, comment_spc, comment

	def getCondContainer(it, condition):
		if not(condition in cond_raw):
			return None
		if it.getCondType(condition)!=cond_compare_or_space:
			return None
		idx = cond_raw.index(condition)
		return conditions[idx][2]

	def getCondType(it, condition):
		if not(condition in cond_raw):
			return None
		idx = cond_raw.index(condition)
		return conditions[idx][1]

class ruleActions(rulePrims):

	def _ld(it, action, bActive, txtArgs, comment_spc, comment):
		from shlex import shlex as shx
		args = it.argtuple(txtArgs)
		#TODO: Validate args
		it[action] = bActive, args, comment_spc, comment

appears = "Show Hide".split()
reAppear = re.compile(
	r"^\s*(?P<inactive>#?)\s*(?P<appear>(?:"\
	+r')|(?:'.join(appears)\
	+r"))(?P<spc>\s*)(?P<comment>#.*)?$", re.I|re.U)

def _d(*x, **xx):
	pass

class Rule():
	def __init__(it, logger, debug=True):
		it._p = logger
		it._d = logger if debug else _d
		it.headlines = ()
		it.Appear = ''
		it.active = False
		it.bComment = False
		it.comment = ''
		it.sectName = ''
		it.ssectId = ''
		it.Conditions = ruleConditions(logger, cond_raw, "Condition", debug=debug)
		it.Actions = ruleActions(logger, actn_raw, "Action", debug=debug)

	def load(it, lines, sectName='', ssectId='', ptr=0):
		it.sectName = sectName
		it.ssectId = ssectId
		startLine = ptr+1 # line no = ptr+1
		it._d(("      %4.d: " % (startLine)), 'tgEnum')
		it._d(u" New Rule")
		ptrBody = None
		bGotAppear = False
		cLines = len(lines)
		for idx, line in enumerate(lines):
			if not(bGotAppear): # Searching for „Show” or „Hide”
				m = reAppear.match(line)
				if not(m):
					continue # maybe in next line…?
				it.active = not(bool(m.group("inactive")))
				it.Appear = m.group("appear")
				comment = m.group("comment")
				it.bComment = bool(comment)
				it.comment = '' if not(bool(comment)) else comment[1:] # Del „#”
				it.headlines = tuple(lines[:idx])
				ptrBody = ptr+idx
				it._d("; body in line:")
				it._d(("%4.d" % (ptrBody+1)), 'tgEnum')
				bGotAppear = True
			else:# „Show” or „Hide” found…
				m = reCondition.match(line)
				if m:
					bActive = not(bool(m.group("inactive")))
					condition = m.group("condition")
					txtArgs = m.group("txtArgs")
					comment_spc = m.start("comment")+int(bActive)
					if comment_spc<0:
						comment_spc = 0
					comment = m.group("comment")
					it.Conditions._ld(
						condition, bActive, txtArgs, comment_spc, '' if not(bool(comment)) else comment[1:])
					continue
				m = reAciton.match(line)
				if m:
					bActive = not(bool(m.group("inactive")))
					action = m.group("action")
					txtArgs = m.group("txtArgs")
					comment_spc = m.start("comment")+int(bActive)
					if comment_spc<0:
						comment_spc = 0
					comment = m.group("comment")
					it.Actions._ld(
						action, bActive, txtArgs, comment_spc, '' if not(bool(comment)) else comment[1:])
					continue
				it._d(", last one:")
				it._d(("%4.d\n" % (ptr+idx)), 'tgEnum') # must be (next - 1) so ptr is OK
				return idx #return lines acquired
		# All lines searched and no „Show” or „Hide” found…
		it._d(u" - without commands, lines count:")
		it._d(("%4.d" % (cLines)), 'tgEnum')
		it._d(", last one:")
		it._d(("%4.d\n" % (ptr+cLines)), 'tgEnum') # must be (next - 1) so ptr is OK
		if cLines>1 and(bGotAppear):
			it._p("Strange ruleset with ", 'tgErr')
			it._p("%d lines"% cLines, 'tgEnum')
			it._p(" and „Show” or „Hide” detected", 'tgErr')
			it._p(" in section „", 'tgErr')
			it._p("%s" % it.sectName, 'tgPhrase')
			it._p("”:\n", 'tgErr')
			it._p("idx:%d\n" % idx, 'tgErr')
			it._p("Dump:\n", 'tgErr')
			it._p("%s\n" % '\n'.join(lines), 'tgPhrase')
		it.headlines = tuple(lines)
		return cLines #return lines acquired

	def _st(it):
		txt_st = '\n'.join(it.headlines)+'\n'
		if not(it.Appear):
			return txt_st
		ln_st = "%s%s" % (('#', '')[it.active], it.Appear.title())
		if it.bComment:
			ln_st += " #%s" % it.comment
		txt_st += ln_st+'\n'
		txt_st += it.Conditions._st(it.active)
		txt_st += it.Actions._st(it.active)
		return txt_st

	def show(it, bYes):
		it.Appear = ('Hide', 'Show')[int(bYes)]

	def activate(it):
		it.active = True
		for condition_key in it.Conditions.keys:
			it.Conditions.activate(condition_key)
		for action_key in it.Actions.keys:
			it.Actions.activate(action_key)

	def deactivate(it):
		it.active = False
		for condition_key in it.Conditions.keys:
			it.Conditions.deactivate(condition_key)
		for aciion_key in it.Actions.keys:
			it.Actions.deactivate(aciion_key)

	def setColor(it, actionColor, _r, _g, _b, _a=-1):
		if not(it.Actions.has_lead(actionColor)):
			return
		bActive, args, comment_spc, comment = it.Actions[actionColor]
		if len(args) not in(3, 4):
			return
		_args = ( _r, _g, _b) if  _a<0 else ( _r, _g, _b, _a)
		it.Actions.bWarning = False
		it.Actions[actionColor] = bActive, tuple(map(lambda x: str(x), _args)), comment_spc, comment
		it.Actions.bWarning = True

	def tuneFontSize(it, old, new, noMatchErr=False):
		rowFontSize = it.Actions['SetFontSize']
		if rowFontSize: #can be None
			bActive, args, comment_spc, comment = rowFontSize
			txtFontSize = args[0]
			if txtFontSize.isdigit() and(int(txtFontSize)==old):
				it.Actions.bWarning = False
				it.Actions['SetFontSize'] = bActive, (str(new), ), comment_spc, comment
				it.Actions.bWarning = True
				return
		if noMatchErr:
			it._p("No match search font size ", 'tgErr')
			it._p("%d"% old, 'tgEnum')
			it._p(" in section „", 'tgErr')
			it._p("%s" % it.sectName, 'tgPhrase')
			it._p("” and subsection „", 'tgErr')
			it._p("%s" % it.ssectId, 'tgPhrase')
			it._p("” - probably NeverSink has changed this…\n", 'tgErr')

	def srch_in_headlines(it, txt):
		for line in it.headlines:
			if txt in line:
				return True
		return False

	def get_condition_args(it, txt):
		row = it.Conditions[txt]
		print(txt, '→', row)
		if row and(len(row)==4):
			_, args, _, _ = row
			return args
		else:
			return None

	def srch_rule_comments(it, txt, noMatchErr=None, level=-1):
		if txt in it.comment:
			return (it, )
		for row in (it.Conditions+it.Actions):
			comment = row[-1]
			if isinstance(comment, basestring) and(txt in comment):
				return (it, )
		return None

	def srch_rule_basetype(it, txt, noMatchErr=None, level=-1):
		baseRow = it.Conditions['BaseType']
		if baseRow and(len(baseRow)==4):
			_, args, _, _ = baseRow
			for arg in args:
				if txt in arg:
					return (it, )
		return None

class Element(xlist):
	def __init__(it, logger, debug=True):
		xlist.__init__(it)
		if hasattr(it, '_init'):
			it._init()
		it._p = logger
		it._d = logger if debug else _d
		it.desc = ''
		it.name = ''
		it.headlines = ()

	def srch_in_headlines(it, txt): #try to make recurency and return child index or None
		for line in it.headlines:
			if txt in line:
				return True
		return False

	def _st(it):
		txt_st = '\n'.join(it.headlines)
		if txt_st:
			txt_st += '\n'
		for child in it:
			txt_st += child._st()
		return txt_st

	def tuneFontSize(it, old, new, noMatchErr=False):
		for child in it:
			child.tuneFontSize(old, new, noMatchErr=False)

	def activate(it):
		for child in it:
			child.activate()

	def deactivate(it):
		for child in it:
			child.deactivate()

	def erase(it):
		it.__init__(it._p)

	def setColor(it, *args):
		for child in it:
			child.setColor(*args)

	def srch_rule_basetype(it, txt, noMatchErr=False, level=0):
		child_level = level+1
		results = []
		for child in it:
			match_rules = child.srch_rule_basetype(txt, noMatchErr=noMatchErr, level=child_level)
			if match_rules:
				results += match_rules
		if noMatchErr and not(results) and(level==0): # display error only on recurency top
			if isinstance(it, nvrsnkSections):
				sectName = "root"
			elif isinstance(it, Section):
				sectName = it.name
			else:
				sectName = it.sectName
			it._p("Search error for BaseType:", 'tgErr')
			it._p("%s" % txt, 'tgPhrase')
			it._p(" in section „", 'tgErr')
			it._p("%s" % sectName, 'tgPhrase')
			it._p("” - probably NeverSink has changed this…\n", 'tgErr')
		return tuple(results)

	def srch_rule_comments(it, txt, noMatchErr=False, level=0):
		child_level = level+1
		results = []
		for child in it:
			match_rules = child.srch_rule_comments(txt, noMatchErr=noMatchErr, level=child_level)
			if match_rules:
				results += match_rules
		if noMatchErr and not(results) and(level==0): # display error only on recurency top
			if isinstance(it, nvrsnkSections):
				sectName = "root"
			elif isinstance(it, Section):
				sectName = it.name
			else:
				sectName = it.sectName
			it._p("Search error for Comment:", 'tgErr')
			it._p("%s" % txt, 'tgPhrase')
			it._p(" in section „", 'tgErr')
			it._p("%s" % sectName, 'tgPhrase')
			it._p("” - probably NeverSink has changed this…\n", 'tgErr')
		return tuple(results)

class Division(Element):
	def __init__(it, logger, debug):
		Element.__init__(it, logger, debug)
		it.ssectId = ''

	def load(it, headLines, bodyLines, sectName, ssectId, ptrDiv):
		it.sectName = sectName
		it.ssectId = ssectId
		it.headlines = headLines
		startLine = ptrDiv+1 # line no = ptr+1
		it._d(("    %4.d: " % (startLine)), 'tgEnum')
		bGotHead = True
		if not(headLines):
			bGotHead = False
			#it.name still ''
			it._d(u" Assuming default, no name Division")
		elif reDiv.match(headLines[1]):
			sGS = reDiv.search(headLines[1])
			it.name = sGS.group('divTxt')
			it._d(u" Found Division „")
			it._d(it.name, 'tgPhrase')
			it._d(u"”")
		else:
			#skip
			it._p(u"Unrecognised Division line[", 'tgErr')
			it._p((u"%4.d" % (startLine)), 'tgEnum')
			it._p("]:„", 'tgErr')
			it._p(u"Unrecognised Division line:„", 'tgErr')
			it._p(unicode(headLines[1]), 'tgPhrase')
			it._p(u"”", 'tgErr')
			if it._d==_d:
				it._p('\n')
		ptrDivisionBody = ptrDiv + int(bGotHead)*3
		lsB = []
		cLines = len(bodyLines)
		ptrDivisionEnd = ptrDivisionBody+cLines
		it._d("; body lines count:")
		it._d(("%4.d" % (cLines)), 'tgEnum')
		it._d(", last one:")
		it._d(("%4.d\n" % (ptrDivisionEnd)), 'tgEnum') # must be (next - 1) so ptr is OK
		ptr = ptrDivisionBody
		slc = 0
		while ptr<ptrDivisionEnd:
			newRule = Rule(it._p, debug=not(it._d==_d))
			acquired = newRule.load(bodyLines[slc:], sectName, ssectId, ptr)
			slc += acquired
			ptr += acquired
			it.append(newRule)

class Subsection(Element):
	def _init(it):
		it.Id = None

	def load(it, headLines, bodyLines, sectName, ptrSub):
		it.sectName = sectName
		it.headlines = headLines
		startLine = ptrSub+1 # line no = ptr+1
		it._d(("  %4.d: " % (startLine)), 'tgEnum')
		#process default first (empty headlines)
		bGotHead = True
		if not(headLines):
			it._d(u" Assuming default, no name Subsection")
			bGotHead = False
			it.Id = -1
		elif reSubSect.match(headLines[1]):
			sGS = reSubSect.search(headLines[1])
			it.Id = int(sGS.group('ssectID'))
			it.name = sGS.group('ssectTxt')
			it._d(u" Found Subsection „")
			it._d(it.name, 'tgPhrase')
			it._d(u"” id: ")
			it._d("%04d" % it.Id, 'tgEnum')
		else:
			it._p(u"Unrecognised Subsection line[", 'tgErr')
			it._p((u"%4.d" % (startLine)), 'tgEnum')
			it._p("]:„", 'tgErr')
			it._p(unicode(lines[1]), 'tgPhrase')
			it._p(u"”", 'tgErr')
			if it._d==_d:
				it._p('\n')
			#skip
			it.Id = -1
		cSkip = 0
		ptrSubBody = ptrSub + int(bGotHead)*3
		lsB = []
		cLines = len(bodyLines)
		it._d("; body lines count:")
		it._d(("%4.d" % (cLines)), 'tgEnum')
		it._d(", last one:")
		it._d(("%4.d\n" % (ptrSubBody+cLines)), 'tgEnum') # must be (next - 1) so ptr is OK
		if bodyLines[-1]!='' and(sectName!="Head"):
			it._d('\n')
			it._p("Warning! Added empty line (currently not present) at the end of subsection „%s”[" % (it.name), 'tgWarn')
			it._p("%04d" % (it.Id), 'tgEnum')
			it._p("],\n in section „%s”, source file line number:" % (sectName), 'tgWarn')
			it._p(("%4.d\n\n" % (ptrSubBody+cLines+1)), 'tgEnum')
			bodyLines.append('')
		for idx, line in enumerate(bodyLines):
			if cLines-idx<2:
				continue
			if bool(cSkip):
				cSkip -= 1
				continue
			if reDiv.match(bodyLines[idx+1])\
				and(reSegDeco.match(line))\
				and(reSegDeco.match(bodyLines[idx+2])):
				lsB.append(idx)
				cSkip = 3
				continue
		cDivis = len(lsB)
		maxDiv = cDivis - 1
		if cDivis:
			if lsB[0]>0:
				divBodyLines = bodyLines[:lsB[0]]
				defaultDiv = Division(it._p, debug=not(it._d==_d))
				defaultDiv.load((), divBodyLines, sectName, it.Id, ptrSubBody)
				it.append(defaultDiv)
			for idx, pB in enumerate(lsB):
				newDiv = Division(it._p, debug=not(it._d==_d))
				ptrSubBody = ptrSub + pB + int(bGotHead)*3
				if idx<maxDiv:
					newDiv.load(bodyLines[pB:pB+3], bodyLines[pB+3:lsB[idx+1]], sectName, it.Id, ptrSubBody)
				else:
					newDiv.load(bodyLines[pB:pB+3], bodyLines[pB+3:], sectName, it.Id, ptrSubBody)
				it.append(newDiv)
		#Assume default Division here
		else:
			defaultDiv = Division(it._p, debug=not(it._d==_d))
			defaultDiv.load((), bodyLines, sectName, it.Id, ptrSubBody)
			it.append(defaultDiv)

class Section(Element):
	def _init(it):
		it.Id = None

	def load(it, headLines, bodyLines, ptrSect):
		it.headlines = headLines
		#Check Head
		startLine = ptrSect+1 # line no = ptr+1
		it._d(("\n%4.d: " % (startLine)), 'tgEnum')
		sGS = reGencSect.search(headLines[1])
		if reHead.match(headLines[1]):
			it.Id = 0
			it.name = 'Head'
			it._d(" Found Head Section")
		elif reTOC.match(headLines[1]):
			it.Id = 1
			it.name = 'ToC'
			it._d(" Found Table Of Contents Section")
		elif reThanks.match(headLines[1]):
			it.Id = int(sGS.group('sectID'))
			it.name = 'Thx'
			it._d(" Found Thanks Section(id: ")
			it._d("%04d" % it.Id, 'tgEnum')
		elif reGencSect.match(headLines[1]):
			it.Id = int(sGS.group('sectID'))
			it.name = sGS.group('sectTxt')
			it._d(u" Found Section „")
			it._d(it.name, 'tgPhrase')
			it._d(u"” id: ")
			it._d("%04d" % it.Id, 'tgEnum')
		else:
			it._p(u"Unrecognised Section line[", 'tgErr')
			it._p((u"%4.d" % (startLine)), 'tgEnum')
			it._p("]:„", 'tgErr')
			it._p(unicode(headLines[1]), 'tgPhrase')
			it._p(u"”", 'tgErr')
			it.Id = -1
		cSkip = 0
		ptrSectBody = ptrSect + 3
		lsB = []
		cLines = len(bodyLines)
		it._d("; body lines count:")
		it._d(("%4.d" % (cLines)), 'tgEnum')
		it._d(", last one:")
		it._d(("%4.d\n" % (ptrSectBody+cLines)), 'tgEnum') # must be (next - 1) so ptr is OK
		for idx, line in enumerate(bodyLines):
			if cLines-idx<2:
				continue
			if bool(cSkip):
				cSkip -= 1
				continue
			if reSubSect.match(bodyLines[idx+1])\
				and(reSegDeco.match(line))\
				and(reSegDeco.match(bodyLines[idx+2])):
				lsB.append(idx)
				cSkip = 3
				continue
		cSubsect = len(lsB)
		maxSubsect = cSubsect - 1
		if cSubsect:
			if lsB[0]>0:
				defaultSubsect = Subsection(it._p, debug=not(it._d==_d))
				defaultSubsect.load((), bodyLines[:lsB[0]], it.name, ptrSectBody)
				it.append(defaultSubsect)
			for idx, pB in enumerate(lsB):
				newSubsect = Subsection(it._p, debug=not(it._d==_d))
				ptrSectBody = ptrSect + pB + 3
				if idx<maxSubsect:
					newSubsect.load(bodyLines[pB:pB+3], bodyLines[pB+3:lsB[idx+1]], it.name, ptrSectBody)
				else:
					newSubsect.load(bodyLines[pB:pB+3], bodyLines[pB+3:], it.name, ptrSectBody)
				it.append(newSubsect)
		#Assume default Subsection here
		else:
			defaultSubsect = Subsection(it._p, debug=not(it._d==_d))
			defaultSubsect.load((), bodyLines, it.name, ptrSectBody)
			it.append(defaultSubsect)

	def getSubsecttionById(it, Id):
		for idx, ssect in enumerate(it):
			if ssect.Id==Id:
				return it[idx]
		return None

class nvrsnkSections(Element):

	def load(it, fnLoad):
		global Data_pass
		Data_pass = "Loading File"
		def ldErr(fn):
			for txtslice, cTag in( ("Can't open a file:", 2), ("'", 0), (hh(fnLoad), 1),("'\n", 0) ):
				it._p(txtslice, tag=(None, 'tgFileName', 'tgFindErr')[cTag])
		if not(ph.isfile(fnLoad)):
			ldErr(fnLoad)
			return
		for txtslice, cTag in( ("Reading a file:", 2), ("'", 0), (hh(fnLoad), 1),("'\n", 0) ):
			it._p(txtslice, tag=(None, 'tgFileName', 'tgPhrase')[cTag])
		hFile = open(fnLoad, 'r')
		if not(hFile):
			ldErr(fnLoad)
			return
		data = hFile.read()
		hFile.close()
		it.fnLoad = fnLoad
		lines = map(lambda line: line.strip(), data.splitlines())
		cSkip = 0
		lsB = []
		cLines = len(lines)
		for idx, line in enumerate(lines):
			if bool(cSkip):
				cSkip -= 1
				continue
			if reSectionDeco.match(line)\
				and(reSectionDeco.match(lines[idx+2])):
				lsB.append(idx)
				cSkip = 3
				continue
		cSect = len(lsB)
		maxSect = cSect - 1
		for idx, pB in enumerate(lsB):
			newSect = Section(it._p, debug=not(it._d==_d))
			if idx<maxSect:
				newSect.load(lines[pB:pB+3], lines[pB+3:lsB[idx+1]], pB)
			else:
				newSect.load(lines[pB:pB+3], lines[pB+3:], pB)
			it.append(newSect)
		it._d("Sections total: %d\n" % len(it))
		Data_pass = "File Loaded"

	def store(it, fnStore):
		for txtslice, cTag in( ("Writing a file:", 2), ("'", 0), (hh(fnStore), 1),("'\n", 0) ):
			it._p(txtslice, tag=(None, 'tgFileName', 'tgPhrase')[cTag])
		hFile = open(fnStore, 'w')
		hFile.write(it._st())
		hFile.close()
		it.fnStore = fnStore

	def getSectionByName(it, name):
		for sect in it:
			if sect.name==name:
				return sect
		it._p("Check section name „", 'tgErr')
		it._p("%s" % name, 'tgPhrase')
		it._p("” - probably removed…\n", 'tgErr')
		return None

	def getSectionById(it, Id, checkName=''):
		for sect in it:
			if sect.Id==Id:
				if checkName:
					if sect.name==checkName:
						return sect
				else:
					return sect
		if checkName:
			sect = it.getSectionByName(checkName)
			if sect:
				it._p("Section with name „", 'tgWarn')
				it._p("%s" % checkName, 'tgPhrase')
				it._p("” has section Id ", 'tgWarn')
				it._p("%d"% sect.Id, 'tgEnum')
				it._p(" different than expected ", 'tgWarn')
				it._p("%d" % Id, 'tgEnum')
				it._p(" - probably changed…\n", 'tgWarn')
				return sect
		it._p("Check section Id ", 'tgErr')
		it._p("%d"% Id, 'tgEnum')
		if checkName:
			it._p(" with name „", 'tgErr')
			it._p("%s" % checkName, 'tgPhrase')
			it._p("”", 'tgErr')
		it._p(" - probably removed…\n", 'tgErr')
		return None

	def getSubsectionByName(it, name, verbose=True):
		for sect in it:
			for ssect in sect:
				if ssect.name==name:
					return sect.Id, ssect.Id, ssect
		if verbose:
			it._p("Check subsection name „", 'tgErr')
			it._p("%s" % name, 'tgPhrase')
			it._p("” - probably removed…\n", 'tgErr')
		return None

	def getSubsecttionById(it, sectId, ssectId, checkName=''):
		sect = it.getSectionById(sectId)
		if sect:
			ssect = sect.getSubsecttionById(ssectId)
			if ssect:
				if checkName:
					if ssect.name==checkName:
						return ssect
				else:
					return ssect
			if checkName:
				tst = it.getSubsectionByName(checkName, verbose=False)
				if tst and(type(tst)==tuple) and(len(tst)==3):
					sectId_n, ssectId_n, ssect = tst
					it._p("Subsection with name „", 'tgWarn')
					it._p("%s" % checkName, 'tgPhrase')
					it._p("” SectionId/subsectionId:", 'tgWarn')
					it._p("%d/%d" % (sectId_n, ssectId_n), 'tgEnum')
					it._p(" is different than expected:", 'tgWarn')
					it._p("%d/%d" % (sectId, ssectId), 'tgEnum')
					it._p(" - probably changed…\n", 'tgWarn')
					return ssect
		it._p("Check section/subsection Id ", 'tgErr')
		it._p("%d/%d" % (sectId, ssectId), 'tgEnum')
		if checkName:
			it._p(" with name „", 'tgErr')
			it._p("%s" % checkName, 'tgPhrase')
			it._p("”", 'tgErr')
		it._p(" - probably removed…\n", 'tgErr')
		return None

