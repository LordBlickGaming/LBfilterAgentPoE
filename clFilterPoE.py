#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-


from clIniFile_py3 import xlist
from os import path as ph
import re

_n = '\n'
compares = "< > = <= >= <>".split()
reCompares = re.compile(r"^(?:(?:"+r')|(?:'.join(compares)+r"))$", re.U)

#reLstCmpSock = re.compile(r"^(?:(?:"+r')|(?:'.join(compares)+r"))$", re.U)
reLstCmpSock = re.compile(r"^[1-6][ADRGBW]{1,6}$", re.U)

reSectionDeco = re.compile(r"^\s*#\s*\={5,}", re.U)
reSegDeco = re.compile(r"^\s*#\s*\-{5,}", re.U)
#reScSgHdExpand = re.compile(r"^\s*#\s*[^=-]+$", re.U)
reScSgHdExpand = re.compile(r"^\s*#\s*.+$", re.U)

reHead = re.compile(r"^\s*#\s*.*Loot\s+Filter.*$", re.U)
reTOC = re.compile(r"^\s*#\s*\[WELCOME\]\s+TABLE\s+OF\s+CONTENTS\s+\+\s+QUICKJUMP\s+TABLE\s*$", re.U)
reThanks = re.compile(r"^\s*#\s*.*thanks.*$", re.U | re.I)
reGenSect = re.compile(r"^\s*#\s*\[\[(?P<sectID>\d+)\]\]\s*(?P<sectTxt>[\/\w\s\-\+,\(\)\!\:]+)$", re.U)
subGenSect = re.compile(r"^(?P<before_sectID>\s*#\s*\[\[)\d+(?P<after_sectID>\]\]\s*[\/\w\s\-\+,\(\)\!\:]+)$", re.U)

reSubSect = re.compile(r"^\s*#\s*\[(?P<ssectID>\d+)\]\s*(?P<ssectTxt>[\w\s\-\+,\(\)\!\:%\.\/\"#]+)$", re.U)
subSubSect = re.compile(r"^(?P<before_ssectID>\s*#\s*\[)\d+(?P<after_ssectID>\]\s*[\w\s\-\+,\(\)\!\:%\.\/\"#]+)$", re.U)

reDiv = re.compile(r"^\s*#\s*(?P<divTxt>[\w\s\-\+,\(\)\!\:%\.\/\"]+)$", re.U)

Data_pass = "None"

_range = lambda _min, _max: tuple(range(_min, _max+1))
in_range = lambda _val, _min, _max: _val in _range(_min, _max)
_byte = _range(0, 255)
_range100 = _range(1, 100)
_nan_byte = (None,)+_byte # not always needed
_ef_colors =  'Red Green Blue Brown White Yellow'.split
_ef_shapes = 'Circle Diamond Hexagon Square Star Triangle'.split
_ef_temp = (None, 'Temp')
cond_bool             = 1
cond_list             = 2
cond_list_multi       = 3
cond_match_re         = 4
cond_list_cmp_re      = 5
cond_compare_or_space = 6

dcRarity = dict(map(reversed, (enumerate("Normal Magic Rare Unique".split()))))

conditions = (
	("HasSearingExarchImplicit", cond_compare_or_space, (1, 6)),
	("HasEaterOfWorldsImplicit", cond_compare_or_space, (1, 6)),
	("ArchnemesisMod",           cond_list_multi),
	("Scourged",                 cond_bool),
	("BlightedMap",              cond_bool),
	("UberBlightedMap",          cond_bool),
	("ShaperItem",               cond_bool),
	("ElderItem",                cond_bool),
	("FracturedItem",            cond_bool),
	("SynthesisedItem",          cond_bool),
	("AnyEnchantment",           cond_bool),
	("ShapedMap",                cond_bool),
	("Identified",               cond_bool),
	("Corrupted",                cond_bool),
	("CorruptedMods",            cond_compare_or_space, _range(1, 6)),
	("Mirrored",                 cond_bool),
	("AlternateQuality",         cond_bool),
	("Replica",                  cond_bool),
	("LinkedSockets",            cond_list_cmp_re),
	("Sockets",                  cond_list_cmp_re),
	("Mods",                     cond_compare_or_space, _range(1, 8)),
	("MapTier",                  cond_compare_or_space, (1, 20)),
	("Width",                    cond_compare_or_space, (1, 2)),
	("Height",                   cond_compare_or_space, _range(1, 4)),
	("Quality",                  cond_compare_or_space, _range100),
	("HasInfluence",             cond_list),
	("ItemLevel",                cond_compare_or_space, _range100),
	("AreaLevel",                cond_compare_or_space, _range100),
	("DropLevel",                cond_compare_or_space, _range100),
	("BaseDefencePercentile",    cond_compare_or_space, _range100),
	("Rarity",                   cond_compare_or_space, dcRarity),
	("EnchantmentPassiveNum",    cond_compare_or_space, (1, 12)),
	("GemQualityType",           cond_list),
	("GemLevel",                 cond_compare_or_space, (1, 30)),
	("StackSize",                cond_compare_or_space, (1, 1000)),
	("SocketGroup",              cond_list_cmp_re),
	("Class",                    cond_list),
	("BaseType",                 cond_list),
	("ElderMap",                 cond_bool),
	("HasMod",                   cond_list),
	("EnchantmentPassiveNode",   cond_list),
	("Prophecy",                 cond_list),
	("HasEnchantment",           cond_list),
	("HasExplicitMod",           cond_list_multi),
	)
cond_raw = tuple(n[0] for n in conditions)
which_condition = lambda txt: cond_raw.index(txt)+1 if txt in cond_raw else 0
reCondition = re.compile(
	r"^\s*(?P<inactive>#?)\s*(?P<condition>(?:"\
	+r')|(?:'.join(sorted(cond_raw, reverse=True))\
	+r"))(?P<txtArgs>[^#]*)(?P<comment>#.*)?$", re.U)
# It is to avoid split due to reperatable condition names, for example "CorruptedMods" → "Corrupted Mods"
# Unfortunately regex has some limitations

actions = (
	("SetFontSize", _range(18, 45)), #(default: 32)
	#						R		G		B	 Alpha(Default is 255)
	("SetTextColor", _byte, _byte, _byte, _nan_byte),
	("SetBorderColor", _byte, _byte, _byte, _nan_byte),
	("SetBackgroundColor", _byte, _byte, _byte, _nan_byte),
	#						Choice			Volume
	("DisableDropSound",),
	("PlayAlertSound", _range(1, 16), _range(0, 300)),
	('PlayEffect', _ef_colors, _ef_temp),
	("MinimapIcon", _range(0, 2), _ef_colors, _ef_shapes),
	("Continue",),
	)
actn_raw = tuple(n[0] for n in actions)
which_action = lambda txt: actn_raw.index(txt)+1 if txt in actn_raw else 0
reAciton = re.compile(
	r"^\s*(?P<inactive>#?)\s*(?P<action>(?:"\
	+r')|(?:'.join(actn_raw)\
	+r"))(?P<txtArgs>[^#]*)(?P<comment>#.*)?$", re.U)

def _dv(*x, **xx):# Send Debug To Void
	pass

class None_Type(type):
	name = 'None_'
	def __new__(it):
		return type.__new__(it, it.name, (type,), {})

	def __init__(it):
		super(None_Type, it).__init__(it.name, (type,), {})

	def __str__(it):
		return ''

	def __repr__(it):
		return it.name

	def __nonzero__(it):
		return False

	def __bool__(it):
		return False

	def __len__(it):
		return 0

	def __call__(it, *args, **kwargs):
		return None

	def __contains__(it, item):
		return False

	def __getitem__(it, item):
		return None

	def __iter__(it):
		return it

	def next(*args):
		raise StopIteration

None_ = None_Type()

appears = "Hide Show".split()
reAppear = re.compile(
	r"^\s*(?P<inactive>#?)\s*(?P<appear>(?:"\
	+r')|(?:'.join(appears)\
	+r"))(?P<spc>\s*)(?P<comment>#.*)?$", re.I|re.U)

n_rule_ln = lambda s:(s not in cond_raw+actn_raw) and(s.title() not in appears)

def scsgtHeadLine(lines, cLns, ln_idx):
	ln = lines[ln_idx]
	bHeadGo = bool(reScSgHdExpand.match(ln) and(not(
		reSectionDeco.match(ln) or(reSegDeco.match(ln))
		or(reGenSect.match(ln)) or(reSubSect.match(ln)) )))
	return bHeadGo

def divHeadLine(ln, cont=False):
	if cont and(not(ln.strip())):
		return True
	mDiv = reDiv.match(ln)
	if not(mDiv):
		return False
	return n_rule_ln(mDiv.group('divTxt').split()[0]) # ommit hashed rules

class rulePrims(xlist):
	'''
	Extended constant list of rows:
	  (command(str), (activity(bool), args(list), comment_spc, comment))
	 Empty command:
	  (command, None)
	'''
	def __init__(it, commands, name):
		xlist.__init__(it)
		it.name = name
		it.bWarning = True
		it.commands = commands
		for command in commands:
			if name == "Condition" and(it.getCondType(command)==cond_compare_or_space):
				it.append((command+'_Lo', None))
				it.append((command+'_Hi', None))
			elif name == "Condition" and(it.getCondType(command)==cond_list_multi):
				lm = xlist()
				it.append((command+'_M', lm))
			else:
				it.append((command, None))
		#(key, value) = item
		it.keys = tuple(item[0] for item in it)

	# prim_tag in condition, action
	def _ld(it, prim_tag, bActive, txtArgs, comment_spc, comment):
		args = it.argtuple(txtArgs)
		it[prim_tag] = bActive, args, comment_spc, comment

	def copy(it):
		newRP = it.__class__(it.commands, it.name)
		newRP.bWarning = it.bWarning
		newRP.keys = it.keys
		newRP.replace(it)
		return newRP

	def reset_command(it, command):
		name = it.name
		if name == "Condition" and(it.getCondType(command)==cond_compare_or_space):
			it[command+'_Lo'] = None
			it[command+'_Hi'] = None
		elif name == "Condition" and(it.getCondType(command)==cond_list_multi):
			it[command+'_M'] = xlist()
		else:
			it[command] = None

	has_key = lambda it, key: key in it.keys
	get_place = lambda it, key: it.keys.index(key)
	values = lambda it: tuple([it[key] for key in it.keys])
	is_empty = lambda it: not(any(it.values()))

	def __getitem__(it, key):
		if type(key) is int:
			return xlist.__getitem__(it, key)[1] # [0] is key…
		if it.has_key(key):
			return xlist.__getitem__(it, it.get_place(key))[1] # [0] is key…
		if it.has_key(f"{key}_M"):
			return xlist.__getitem__(it, it.get_place(f"{key}_M"))[1] # [0] is key…
		return None

	def __get_cmp_num(it, key):
		if key[-3:] in '_Hi _Lo'.split():
			mkey = key[:-3]
		else:
			mkey = key
		_iterable = it.getCondContainer(mkey)
		val = it[key]
		if val is not None:
			if isinstance(_iterable, dict):
				return _iterable[val[1][-1]]
			elif isinstance(_iterable, tuple):
				return int(val[1][-1])
		return -1

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
				_d( ('\n',) )
				_l( ((f"     Warning! Ugly overwriting {it.name} „{key}” during "\
					"Data Work Status: >{Data_pass}<:\n", 'wrn'),
					(f"        ({', '.join(str(x)for x in it[idx])})\n", 'phr'),
					("      with\n", 'wrn'),
					(f"        ({', '.join(str(x) for x in value)})\n", 'phr')) )
			it[idx] = key, value # call  numeric rewrite
			return
		elif it.has_key(f"{key}_M"):
			key_ = f"{key}_M"
			idx = it.get_place(key_)
			_lm = it[idx]
			#Ugly workaround - usually no need to edit conditions
			_lm.append(value)
			it[idx] = key, _lm # call  numeric rewrite
			return
		elif it.has_key(f"{key}_Hi") and(it.has_key(f"{key}_Lo")):
			c_hi = it.__get_cmp_num(f"{key}_Hi")
			c_lo = it.__get_cmp_num(f"{key}_Lo")
			_iterable = it.getCondContainer(key)
			if isinstance(_iterable, dict):
				c_val = _iterable[value[1][-1]]
			elif isinstance(_iterable, tuple):
				c_val = int(value[1][-1])
			if c_hi==c_lo:
				if c_val<c_lo:
					it.__setkey(key+'_Lo', value)
				elif c_val>c_hi:
					it.__setkey(f"{key}_Hi", value)
			elif c_hi>c_val>c_lo:
				it.__setkey(key+'_Lo', value)
			elif c_val>c_hi>c_lo:
				it.__setkey(key+'_Lo', it[f"{key}_Hi"])
				it.__setkey(f"{key}_Hi", value)
			elif c_hi>c_lo>c_val:
				it.__setkey(f"{key}_Hi", it[key+'_Lo'])
				it.__setkey(key+'_Lo', value)
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
			return None_
		idx = it.leads.index(lead)
		return it[command][idx]

	def mod_lead(it, command, lead, value, new=False):
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
		tmp_command = leading_left + (value, ) + leading_right
		if len(tmp_command)!=4:
			_l( (("Got trouble with mod_lead !\n\tleft:", 'err'),
				(str(leading_left), 'phr'),
				("\n\tright:", 'err'),
				(f" {str(leading_right)}\n", 'phr')) )
			return False
		it[command] = tmp_command
		return True

	get_args = lambda it, command: it.get_lead(command, 'args')#Error catching in get_lead

	def set_args(it, command, arg_tuple):
		if type(arg_tuple) is tuple:
			return it.mod_lead(command, 'args', arg_tuple)
		return False

	def replace_args(it, command, arg_tuple):
		it.bWarning = False
		ret = it.set_args(command, arg_tuple)
		it.bWarning = True
		return ret

	def new_args(it, command, arg_tuple, spc=0, comment=''):
		if not(it.has_key(command)):
			return False
		it[command] = (True, arg_tuple, spc, comment)
		it.activate(command)
		return True

	def del_cmd(it, command):
		it.bWarning = False
		it.reset_command(command)
		it.bWarning = True

	def activate(it, key):
		it.bWarning = False
		it.mod_lead(key, 'activity', True)
		it.bWarning = True

	def deactivate(it, key):
		it.bWarning = False
		it.mod_lead(key, 'activity', False)
		it.bWarning = True

	def _st_ln(it, command, activity, args, comment_spc, comment):
		txt_st = ''
		txt_st += f"{('#', '')[activity]}\t{command}"
		if args:
			txt_st += f" {' '.join(str(x) for x in args)}"
		fill = len(txt_st)
		if comment_spc and(comment):
			spc_left = comment_spc-fill
			if spc_left>0:
				txt_st += ' '*spc_left
			txt_st += f"#{comment}"
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
			elif command[-3:] in "_Lo _Hi".split():
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
	pass

class Rule():
	def __init__(it, parentDiv):
		it.parentDiv = parentDiv
		it.headlines = ()
		it.Appear = ''
		it.active = False
		it.bComment = False
		it.comment = ''
		it.sectName = ''
		it.ssectId = ''
		it.Conditions = ruleConditions(cond_raw, "Condition")
		it.Actions = ruleActions(actn_raw, "Action")

	def load(it, lines, sectName='', ssectId='', ptr=0):
		it.sectName = sectName
		it.ssectId = ssectId
		startLine = ptr+1 # line no = ptr+1
		_d( ((f"      {startLine:4d}: ", 'num'),) )
		_nr = " New Rule"
		ptrBody = None
		bGotAppear = False
		cLns = len(lines)
		ctrl_cx = cLns
		for idx, line in enumerate(lines): #TODO: Continue Incoming…
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
				_d( (_nr, "; body in line:", (f"{ptrBody+1:4d}" , 'num')) )
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
					ctrl_cx -= 1
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
					ctrl_cx -= 1
					continue
				# must be (next - 1) so ptr is OK
				_d( (", last one:", (f"{ptr+idx:4d}\n", 'num')) )
				return idx #return lines acquired
		_="All known catched in continue-s, so if all went fine, we don't reach next code"
		_='All lines searched and no „Show” or „Hide” found…'
		_d( ((_nr, " - without commands, lines count:"), (f"{cLns:4d}", 'num'),
			", last one:", (f"{ptr+cLns:4d}\n", 'num') # must be (next - 1) so ptr is OK
			) )
		if cLns>1 and(bGotAppear):
			_l( (("Strange ruleset with ", 'err'), (f"{cLns} lines", 'num'),
				(" and „Show” or „Hide” detected in section „", 'err'),
				(it.sectName, 'phr'), (f"”:\nidx:{idx}\n", 'err'),
				("Dump:\n", 'err'), (f"{_n.join(lines)}\n", 'phr')) )
		it.headlines = tuple(lines)
		return cLns #return lines acquired

	def _st(it):
		txt_st = ''
		if it.headlines:
			txt_st += f"{_n.join(it.headlines)}{_n}"
		if not(it.Appear):
			return txt_st
		ln_st = f"{('#', '')[it.active]}{it.Appear.title()}"
		if it.bComment:
			ln_st += f" #{it.comment}"
		txt_st += ln_st+'\n'
		txt_st += it.Conditions._st(it.active)
		txt_st += it.Actions._st(it.active)
		return txt_st

	def copy(it):
		newRule = Rule(it.parentDiv)
		newRule.Conditions = it.Conditions.copy()
		newRule.Actions = it.Actions.copy()
		newRule.headlines = tuple(it.headlines)
		newRule.Appear = it.Appear[:]
		newRule.active = it.active
		newRule.bComment = it.bComment
		newRule.comment = it.comment
		newRule.sectName = it.sectName
		newRule.ssectId = it.ssectId
		return newRule

	def duplicate(it):
		pd = it.parentDiv
		idx = pd.index(it)
		ruleCopy = it.copy()
		pd.insert(idx, ruleCopy)
		return ruleCopy

	def show(it, bYes=True):
		it.Appear = appears[int(bYes)]

	hide = lambda it: it.show(False)

	def recomment(it, comment=None):
		it.bComment = bool(comment)
		if it.bComment:
			it.comment = " {comment}"
		else:
			it.comment = ''

	del_comment = lambda it: it.recomment()

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

	get_cond_args = lambda it, txt: it.Conditions.get_args(txt)
	replace_cond_args = lambda it, txt, arg_tuple: it.Conditions.replace_args(txt, arg_tuple)
	new_cond_args = lambda it, txt, arg_tuple, spc=0, comment='': it.Conditions.new_args(txt, arg_tuple, spc, comment)
	del_cond = lambda it, txt: it.Conditions.del_cmd(txt)
	get_act_args = lambda it, txt: it.Actions.get_args(txt)
	replace_act_args = lambda it, txt, arg_tuple: it.Actions.replace_args(txt, arg_tuple)
	del_act = lambda it, txt: it.Actions.del_cmd(txt)

	def srch_in_headlines(it, txt):
		for line in it.headlines:
			if txt in line:
				return True
		return False

	def srch_rule_comments(it, txt, noMatchErr=None, level=-1):
		if txt in it.comment:
			return (it, )
		for row in (it.Conditions+it.Actions):
			comment = row[-1]
			if isinstance(comment, str) and(txt in comment):
				return (it, )
		return None

	del_txtype_s = lambda it, rem: (rem, f'"{rem}"', f"'{rem}'")

	def del_txtype_msg(it, rem, act, txtype='BaseType'):
		_l( (("Search error for {txtype} {act}:", 'err'), (rem, 'phr'),
			(" in section „", 'err'), (it.sectName, 'phr'),
			("” - probably changed…\n", 'err')) )

	def del_txtype(it, rem, txtype='BaseType'):
		args = it.get_cond_args(txtype)# it.Conditions.get_args(txtype)
		for txt in it.del_txtype_s(rem):
			if not (txt in args):
				continue
			dst = list(args)
			dst.remove(txt)
			it.replace_cond_args(txtype, tuple(dst))
			return
		it.del_txtype_msg(rem, 'deletion', txtype)

	def survive_txtype(it, rem, txtype='BaseType'):
		args = list(it.get_cond_args(txtype))# it.Conditions.get_args(txtype)
		for txt in it.del_txtype_s(rem):
			if txt in args:
				it.replace_cond_args(txtype, (txt,))
				return
		it.del_txtype_msg(rem, 'survive')

	def srch_rule_txtype(it, txt, noMatchErr=None, level=-1, txtype='BaseType'):
		args = it.get_cond_args(txtype)
		if args:
			for arg in args:
				if txt in arg:
					return (it, )
		return None

	def setColor(it, actionColor, _r, _g, _b, _a=-1):
		if not(it.Actions.has_lead(actionColor)):
			return
		bActive, args, comment_spc, comment = it.Actions[actionColor]
		if len(args) not in(3, 4):
			return
		_args = ( _r, _g, _b) if  _a<0 else ( _r, _g, _b, _a)
		it.Actions.bWarning = False
		it.Actions[actionColor] = bActive, tuple(str(x) for x in _args), comment_spc, comment
		it.Actions.bWarning = True

	def getFontSize(it):
		rowFontSize = it.Actions['SetFontSize']
		if rowFontSize: #can be None
			_, args, _, _ = rowFontSize
			txtFontSize = args[0]
			if txtFontSize.isdigit():
				return int(txtFontSize)
		return None

	def tuneFontSize(it, old, new, noMatchErr=False, acCrgba=None):
		if it.Conditions.is_empty():
			return False
		rowFontSize = it.Actions['SetFontSize']
		if rowFontSize: #can be None
			bActive, args, comment_spc, comment = rowFontSize
			txtFontSize = args[0]
			if txtFontSize.isdigit() and(int(txtFontSize)==old):
				it.Actions.bWarning = False
				it.Actions['SetFontSize'] = bActive, (str(new), ), comment_spc, comment
				it.Actions.bWarning = True
				if acCrgba:
					it.setColor(*acCrgba)
				return True
		if noMatchErr:
			_l( (("No match search font size ", 'err'), (f"{old:d}", 'num'),
				(" in section „", 'err'), (it.sectName, 'phr'),
				("” and subsection „", 'err'), (f"{it.ssectId:d}", 'phr'),
				("” - probably changed…\n", 'err')) )
		return False

class Eln:
	def __init__(it, parentDiv):
		it.parentDiv = parentDiv

	def load(it, sectName='', ssectId='', idx_ln=0):
		it.sectName = sectName
		it.ssectId = ssectId
		numLine = idx_ln+1 # line no = idx_ln+1
		_d( ((f"      {numLine:4d}: ", 'num'), " New empty line\n") )

	_st = lambda it: _n

	activate = lambda it: None
	deactivate = lambda it: None
	tuneFontSize = lambda it, old, new, noMatchErr=False: None
	setColor = lambda it, *args: None
	srch_rule_txtype = lambda it, txt, noMatchErr=False, level=0: tuple()
	srch_rule_comments = lambda it, txt, noMatchErr=False, level=0: tuple()

class Element(xlist):
	def __init__(it):
		xlist.__init__(it)
		if hasattr(it, '_init') and(callable(it._init)):
			it._init()
		it.desc = ''
		it.name = ''
		it.headlines = ()

	def srch_in_headlines(it, txt): #try to make recurency and return child index or None
		for line in it.headlines:
			if txt in line:
				return True
		return False

	def _st_headlines(it):
		if it.headlines:
			return
		return ''

	def _st(it):
		txt_st = ''
		if it.headlines:
			if hasattr(it, 'regen_headlines'):
				it.regen_headlines()
			txt_st += f"{_n.join(it.headlines)}{_n}"
		for child in it:
			txt_st += child._st()
		return txt_st

	def tuneFontSize(it, old, new, noMatchErr=False):
		for child in it:
			child.tuneFontSize(old, new, noMatchErr)

	def activate(it):
		for child in it:
			child.activate()

	def deactivate(it):
		for child in it:
			child.deactivate()

	def erase(it):
		it.__init__()

	def setColor(it, *args):
		for child in it:
			child.setColor(*args)

	def srch_rule_txtype(it, txt, noMatchErr=False, level=0):
		child_level = level+1
		results = []
		for child in it:
			match_rules = child.srch_rule_txtype(txt, noMatchErr=noMatchErr, level=child_level)
			if match_rules:
				results += match_rules
		if noMatchErr and not(results) and(level==0): # display error only on recurency top
			if isinstance(it, nvrsnkSections):
				sectName = "root"
			elif isinstance(it, Section):
				sectName = it.name
			else:
				sectName = it.sectName
			_l( (("Search error for BaseType:", 'err'), (txt, 'phr'),
				(" in section „", 'err'), (sectName, 'phr'),
				("” - probably changed…\n", 'err')) )
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
			_l( (("Search error for Comment:", 'err'), (txt, 'phr'),
				(" in section „", 'err'), (sectName, 'phr'),
				("” - probably changed…\n", 'err')) )
		return tuple(results)

class Division(Element):
	def _init(it):
		it.ssectId = ''

	rules = lambda it: tuple(filter(lambda pit: isinstance(pit, Rule), it))

	def load(it, headLines, bodyLines, sectName, ssectId, lnFileIdxDiv):
		it.sectName = sectName
		it.ssectId = ssectId
		it.headlines = headLines
		startLine = lnFileIdxDiv+1 # line no = ptr+1
		_d( ((f"    {startLine:4d}: ", 'num'),) )
		bGotHead = True
		if not(headLines):
			bGotHead = False
			#it.name is ''
			_d( (" Assuming default, no name Division",) )
		elif reDiv.match(headLines[0]):
			sGS = reDiv.search(headLines[0])
			it.name = sGS.group('divTxt')
			_d( (" Found Division „", (it.name, 'phr'), "”") )
		else:
			#skip
			_l( (("Unrecognised Division line[", 'err'), (f"{startLine:4d}", 'num'),
				("]:„", 'err'), (headLines[0], 'phr'),( "”", 'err')) )
			if _d==_d:
				_l( (_n,) )
		lsLnIdx = []
		cHds = len(headLines)
		lnFileIdxDivBody = lnFileIdxDiv + cHds
		_d( ("; headlines:", (f"{cHds:4d}", 'num')) )
		cLns = len(bodyLines)
		lnFileIdxDivEnd = lnFileIdxDivBody+cLns
		_d( ("; bodylines:", (f"{cLns:4d}", 'num'), ", last one:",
			(f"{lnFileIdxDivEnd:4d}", 'num'), # must be (next - 1) so ptr is OK
			_n) )
		lnIdxRuleLoop = 0
		while lnFileIdxDivBody<lnFileIdxDivEnd:
			ln = bodyLines[lnIdxRuleLoop]
			if ln.strip()=='':
				newEln = Eln(it)
				newEln.load(sectName, ssectId, lnFileIdxDivBody)
				lnIdxRuleLoop += 1
				lnFileIdxDivBody += 1
				it.append(newEln)
			else:
				newRule = Rule(it)
				cLnAcquired = newRule.load(bodyLines[lnIdxRuleLoop:], sectName, ssectId, lnFileIdxDivBody)
				if cLnAcquired<0:
					break
				lnIdxRuleLoop += cLnAcquired
				lnFileIdxDivBody += cLnAcquired
				it.append(newRule)

class Subsection(Element):
	def _init(it):
		it.Id = None

	def setId(it, Id):
		it.Id = Id

	def load(it, headLines, bodyLines, ownerSect, lnFileIdxSub):
		it.sectName = ownerSect.name
		sectId = ownerSect.Id
		it.headlines = headLines
		startLine = lnFileIdxSub+1 # line no = ptr+1
		_d( ((f"  {startLine:4d}: ", 'num'),) )
		#process default first (empty headlines)
		if not(headLines):
			_d( (" Assuming default, no name Subsection",) )
			it.Id = -1
		elif reSubSect.match(headLines[1]):
			sGS = reSubSect.search(headLines[1])
			it.Id = int(sGS.group('ssectID'))
			it.name = sGS.group('ssectTxt')
			_d( (" Found Subsection „", (it.name, 'phr'),
				"” id: ", (f"{it.Id:04d}", 'num')) )
		else:
			_l( (("Unrecognised Subsection line[", 'err'), (f"{startLine:4d}", 'num'),
				("]:„", 'err'), (lines[1], 'phr'),( "”", 'err')) )
			if _d==_d:
				_l( ('\n',) )
			#skip
			it.Id = -1
		cHds = len(headLines)
		lnFileIdxSubBody = lnFileIdxSub + cHds
		cLns = len(bodyLines)
		_d( ("; headlines:", (f"{cHds:4d}", 'num'), "; bodylines:",
			(f"{cLns:4d}", 'num'), ", last one:",
			(f"{lnFileIdxSubBody+cLns:4d}\n", 'num') # must be (next - 1) so ptr is OK
			) )
		if sectId>=100 and(it.name): # Check only real filters named subsections
			ssids_used = tuple(ss.Id for ss in ownerSect if ss.Id>0)+(sectId,)
			next_ssid = max(ssids_used)+1
			if it.Id//100!=sectId//100:
				_l( (("Warning! ", 'wrn'), ("Subsection „", 'ylw'), (it.name, 'phr'),
					("” Id:[", 'ylw'), (f"{it.Id:04d}", 'num'),
					("] has an unrelated ID to Section Id:[", 'ylw'),
					(f"{sectId:04d}", 'num'),
					("], fix–>[", 'ylw'), (f"{next_ssid:04d}", 'num'),
					("].\n", 'ylw'),) )
				it.missId = it.Id
				it.setId(next_ssid)
			elif it.Id in ssids_used: #logically includes it.Id//100==sectId//100
				_l( (("Warning! ", 'wrn'), ("Subsection „", 'ylw'), (it.name, 'phr'),
					("” Id:[", 'ylw'), (f"{sectId:04d}", 'num'),
					("][", 'ylw'), (f"{it.Id:04d}", 'num'),
					("] has now same ID as „", 'ylw'), (ownerSect.getSubsecttionById(it.Id).name, 'phr'),
					("”, fix–>[", 'ylw'),
					(f"{next_ssid:04d}", 'num'), ("].\n", 'ylw'),) )
				it.missId = it.Id
				it.setId(next_ssid)
		cSkip = 0
		lsLnIdx = []
		for idx, line in enumerate(bodyLines):
			if bool(cSkip):
				cSkip -= 1
				continue
			if divHeadLine(line):
				cSkip = 1
				#treat blank lines and words not covered by the rules as continuation of the header
				while idx+cSkip<cLns and(divHeadLine(bodyLines[idx+cSkip], cont=True)):
					cSkip += 1
				lsLnIdx.append((idx, cSkip)) # idx, hd_lines_div
				continue
		if lsLnIdx and(lsLnIdx[0][0]):# Make sure default division/empty line
			lsLnIdx.insert(0, (0, 0))
		cDivs = len(lsLnIdx)
		maxDiv = cDivs - 1
		if cDivs:
			lnIdxFrstDiv, cHdLns = lsLnIdx[0]
			# check if we got some lines between headlines and first explicit division
			if lnIdxFrstDiv>cHdLns:
				divBodyLines = bodyLines[:lnIdxFrstDiv]
				defaultDiv = Division()
				# default starts without headlines in parent body
				defaultDiv.load((), divBodyLines, it.sectName, it.Id, lnFileIdxSubBody)
				it.append(defaultDiv)
			for idx, (lnIdxDivHd, cHdLns) in enumerate(lsLnIdx):
				newDiv = Division()
				lnIdxDivBd = lnIdxDivHd+cHdLns
				lnFileIdxDivHd = lnFileIdxSubBody+lnIdxDivHd
				if idx<maxDiv:
					newDiv.load(bodyLines[lnIdxDivHd:lnIdxDivBd], bodyLines[lnIdxDivBd:lsLnIdx[idx+1][0]], it.sectName, it.Id, lnFileIdxDivHd)
				else:
					newDiv.load(bodyLines[lnIdxDivHd:lnIdxDivBd], bodyLines[lnIdxDivBd:], it.sectName, it.Id, lnFileIdxDivHd)
				it.append(newDiv)
		#Assume default Division here
		else:
			defaultDiv = Division()
			# default starts without headlines in parent body
			defaultDiv.load((), bodyLines, it.sectName, it.Id, lnFileIdxSubBody)
			it.append(defaultDiv)

	def regen_headlines(it):
		if it.headlines:
			if len(it.headlines)>2:
				if reSubSect.match(it.headlines[1]):
					it.headlines[1] = subSubSect.sub(
						f"\g<before_ssectID>{it.Id:04d}\g<after_ssectID>", it.headlines[1])

	def tuneFontByBase(it, oldFS, newFS, txtBase, acCrgba=None):
		dst = it.srch_rule_txtype(txtBase, True)
		if not(dst):
			return
		if not(dst[0].tuneFontSize(oldFS, newFS, True, acCrgba)):
			_l( (("Above error comes from BaseType search:„", 'err'), (txtBase, 'phr'),
				("” - probably changed…\n", 'err')) )


	def tuneFontByCmt(it, oldFS, newFS, txtComment, acCrgba=None):
		dst = it.srch_rule_comments(txtComment, True)
		if not(dst):
			return
		if not(dst[0].tuneFontSize(oldFS, newFS, True, acCrgba)):
			_l( (("Above error comes from comment search:„", 'err'), (txtComment, 'phr'),
				("” - probably changed…\n", 'err')) )

	def ruleOnByCmt(it, txtComment):
		dst = it.srch_rule_comments(txtComment, True)
		if dst:
			dst[0].activate()

	def ruleOffByCmt(it, txtComment):
		dst = it.srch_rule_comments(txtComment, True)
		if dst:
			dst[0].deactivate()

	def ruleHideByCmt(it, txtComment):
		dst = it.srch_rule_comments(txtComment, True)
		if dst:
			dst[0].hide()

	div = lambda it, num: it[num]
	div0 = lambda it: it[0]

class Section(Element):
	def _init(it):
		it.Id = None

	def load(it, headLines, bodyLines, lnFileIdxSect):
		it.headlines = headLines
		#Check Head
		startLine = lnFileIdxSect+1 # line no = ptr+1
		_d( ((f"  {startLine:4d}: ", 'num'),) )
		sGS = reGenSect.search(headLines[1])
		if reHead.match(headLines[1]):
			it.Id = 0
			it.name = 'Head'
			_d(" Found Head Section")
		elif reTOC.match(headLines[1]):
			it.Id = 1
			it.name = 'ToC'
			_d( (" Found Table Of Contents Section",) )
		elif reThanks.match(headLines[1]):
			it.Id = int(sGS.group('sectID'))
			it.name = 'Thx'
			_d( (" Found Thanks Section(id: ", (f"{it.Id:04d}", 'num')) )
		elif reGenSect.match(headLines[1]):
			it.Id = int(sGS.group('sectID'))
			it.name = sGS.group('sectTxt')
			_d( (" Found Section „", (it.name, 'phr'), "” id:", (f"{it.Id:04d}", 'num')) )
		else:
			_l( (("Unrecognised Section line[", 'err'), (f"{startLine:4d}", 'num'),
				("]:„", 'err'), (headLines[1], 'phr'), ("”\n", 'err')) )
			it.Id = -1
		cHds = len(headLines)
		_d( ("; headlines:", (f"{cHds:4d}", 'num')) )
		lnFileIdxSectBody = lnFileIdxSect + cHds
		cLns = len(bodyLines)
		_d( ("; bodylines:", (f"{cLns:4d}", 'num'), ", last one:",
			(f"{lnFileIdxSectBody+cLns:4d}\n", 'num') # must be (next - 1) so ptr is OK
			) )
		cSkip = 0
		lsLnIdx = []
		# skip explicit search in last 2 bodylines, cause minimum head size is 3
		for idx, line in enumerate(bodyLines):#[:-2]
			if bool(cSkip):
				cSkip -= 1
				continue
			if idx+2==cLns:# Subsection Decoration limit
				break
			if reSubSect.match(bodyLines[idx+1])\
				and(reSegDeco.match(line))\
				and(reSegDeco.match(bodyLines[idx+2])):
				cSkip = 3
				#while idx+cSkip<cLns-2 and(reScSgHdExpand.match(bodyLines[idx+cSkip]) or(not(bodyLines[idx+cSkip]))):
				while idx+cSkip<cLns-2 and(scsgtHeadLine(bodyLines,  cLns, idx+cSkip)):
					cSkip += 1
				lsLnIdx.append((idx, cSkip)) # idx, hd_lines_sub
				continue
		if lsLnIdx and(lsLnIdx[0][0]):# Make sure default subsection/division/empty line
			lsLnIdx.insert(0, (0, 0))
		cSubsect = len(lsLnIdx) # Explicit subsections detected count
		maxSubsect = cSubsect - 1
		if cSubsect:
			lnIdxFrstSsect, cHdLns = lsLnIdx[0]
			# check if we got some lines between headlines and first explicit subsection
			if lnIdxFrstSsect>cHdLns:
				defaultSubsect = Subsection()
				# default starts without headlines in parent body
				defaultSubsect.load((), bodyLines[:lnIdxFrstSsect], it, lnFileIdxSectBody)
				it.append(defaultSubsect)
			for idx, (lnIdxSubHd, cHdLns) in enumerate(lsLnIdx):
				nSs = Subsection()
				lnIdxSubBd = lnIdxSubHd+cHdLns
				lnFileIdxSubHd = lnFileIdxSectBody + lnIdxSubHd
				if idx<maxSubsect:
					nSs.load(bodyLines[lnIdxSubHd:lnIdxSubBd], bodyLines[lnIdxSubBd:lsLnIdx[idx+1][0]], it, lnFileIdxSubHd)
				else:
					nSs.load(bodyLines[lnIdxSubHd:lnIdxSubBd], bodyLines[lnIdxSubBd:], it, lnFileIdxSubHd)
				it.append(nSs)
		#Assume default Subsection here
		else:
			defaultSubsect = Subsection()
			# default starts without headlines in parent body
			defaultSubsect.load((), bodyLines, it, lnFileIdxSectBody)
			it.append(defaultSubsect)

	def regen_headlines(it):
		if it.headlines:
			if len(it.headlines)>2:
				if reGenSect.match(it.headlines[1]):
					it.headlines[1] = subGenSect.sub(
						f"\g<before_sectID>{it.Id:04d}\g<after_sectID>", it.headlines[1])

	def getSubsecttionByAllId(it, Id):
		for idx, ssect in enumerate(it):
			if ssect.Id==Id or(hasattr(ssect, 'missId') and(ssect.missId==Id)):
				return it[idx]
		return None

	def getSubsecttionById(it, Id):
		for ssect in it:
			if ssect.Id==Id:
				return ssect
		return None

	div = lambda it, num: it[0][num]
	div0 = lambda it: it[0][0]

class nvrsnkSections(Element):
	STD_Debit = 2
	def __init__(it, logger=None, debug=False):
		Element.__init__(it)
		global _l, _d
		if logger:
			_l = logger
		else:
			from clIniFile_py3 import _p
			def _l(l_tpl):
				for chnk in l_tpl:
					if isinstance(chnk, str):
						_p(chnk)
					else:# hope it's enough
						_p(chnk[0]) # tag part irrelevant
		_d = _l if debug else _dv
		it.Id = None

	def load(it, load_fn, ssPromotes=tuple()):
		global Data_pass
		Data_pass = "Loading File"
		def ldErr(fn):
			_l( (("Can't open a file:", 'err'), "'",(load_fn, 'fnm'), "'\n") )
		if not(ph.isfile(load_fn)):
			ldErr(load_fn)
			return
		_l( (("Reading a file:", 'phr'), "'",(load_fn, 'fnm'), "'\n") )
		hFile = open(load_fn, 'r')
		if not(hFile):
			ldErr(load_fn)
			return
		data = hFile.read()
		hFile.close()
		it.load_fn = load_fn
		# Make Debit of empty lines
		lines = [line.strip() for line in data.splitlines()]+['',]*it.STD_Debit
		if data[-1]!='\n': lines.append('') # splitines loose last empty line
		_d( (f"Last SplitLine: „{data.splitlines()[-1]}”\n",
			f"Last Line: „{lines[-1]}”\n") )
		cSkip = 0
		lsLnIdx = []
		cLns = len(lines)

		if ssPromotes:
			#Detect early wrongly tagged section as subsection & correct
			LastSectNo = 0
			for idx, line in enumerate(lines[:-2]):
				mSegDeco1 = reSegDeco.match(line)
				mSegDeco2 = reSegDeco.match(lines[idx+2])
				mSubSect  = reSubSect.match(lines[idx+1])
				mGenSect  = reGenSect.match(line)
				if mGenSect:
					LastSectNo = int(mGenSect.group('sectID'))
				if mSegDeco1 and(mSegDeco2) and(mSubSect):
					ssId  = int(mSubSect.group('ssectID'))
					ssTxt = mSubSect.group('ssectTxt')
					if (ssId,  ssTxt) in ssPromotes:
						LastSectNo += 100
						lines[idx+1] = lines[idx+1].replace(
							f"[{ssId:04d}]", f"[[{LastSectNo:04d}]]")
						for cx in (idx, idx+2):
							lines[cx] = lines[cx].replace('-', '=')
						_l( (("Warning! ", 'wrn'),
							("Std Section with name „", 'ylw'),
							(mSubSect.group('ssectTxt'), 'phr'),
							("” and Id:", 'ylw'), (f"{ssId:04d}", 'num'),
							(" decorated as Subsection, let's go back to Id:[[", 'ylw'),
							(f"{LastSectNo:04d}", 'num'),
							("]].\n", 'ylw'),) )
		#
		for idx, line in enumerate(lines):#[:-2]
			if bool(cSkip):
				cSkip -= 1
				continue
			if idx+2==cLns:
				break # There is no more room for typical section with decoration
			if reSectionDeco.match(line)\
				and(reSectionDeco.match(lines[idx+2])):
				cSkip = 3
				while idx+cSkip<cLns and(scsgtHeadLine(lines,  cLns, idx+cSkip)):
					cSkip += 1
				#Detect wrongly tagged subsection & correct
				mSubSect = reSubSect.match(lines[idx+1])
				if mSubSect:
					_l( (("Warning! Subsection with name „", 'wrn'),
						(mSubSect.group('ssectTxt'), 'phr'), ("” and SectionId:", 'wrn'),
						(f"{int(mSubSect.group('ssectID')):04d}", 'num'),
						(" mistakenly decorated as Section, correcting…\n", 'wrn')) )
					for cx in (idx, idx+2):
						lines[cx] = lines[cx].replace('=', '-')
					continue
				lsLnIdx.append((idx, cSkip)) # idx, hd_lines_sec
				continue
		cSect = len(lsLnIdx)
		maxSect = cSect - 1
		for idx, (lnFileIdxSctHd, cHdLns) in enumerate(lsLnIdx):
			newSect = Section()
			lnFileIdxSctBd = lnFileIdxSctHd + cHdLns
			if idx<maxSect:# lnIdxNextHd = lsLnIdx[idx+1][0]
				if reHead.match(lines[lnFileIdxSctHd+1]):
					#lnFileIdxSctBd = lsLnIdx[idx+1][0]-1
					lnFileIdxSctBd = lsLnIdx[idx+1][0]
				newSect.load(lines[lnFileIdxSctHd:lnFileIdxSctBd], lines[lnFileIdxSctBd:lsLnIdx[idx+1][0]], lnFileIdxSctHd)
			else:
				if reHead.match(lines[lnFileIdxSctHd+1]):
					lnFileIdxSctBd = -1
				newSect.load(lines[lnFileIdxSctHd:lnFileIdxSctBd], lines[lnFileIdxSctBd:], lnFileIdxSctHd)
			it.append(newSect)
		_d( (f"Sections total: {len(it)}\n",) )
		Data_pass = "File Loaded"

	def store(it, fnStore):
		_l( (("Writing a file:", 'phr'), "'", (fnStore, 'fnm'), "'\n") )
		hFile = open(fnStore, 'w')
		#repay debit
		storage = it._st()[:-it.STD_Debit-1] # Cut '\n's of debit with credit ;)
		hFile.write(storage)
		hFile.close()
		it.fnStore = fnStore
		print(f"Saved as:„{fnStore}”")

	def getSectionByName(it, name):
		for sect in it:
			if sect.name==name:
				return sect
		_l( (("Check section name „", 'err'), (name, 'phr'),
			("” - probably removed…\n", 'err')) )
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
				_l( (("Section with name „", 'wrn'), (checkName, 'phr'),
					("” has SectionId:", 'wrn'), (f"{sect.Id:04d}", 'num'),
					(" different than expected ", 'wrn'), (f"{Id:04d}", 'num'),
					(" - probably changed…\n", 'wrn')) )
				return sect
		_l( (("Check section Id ", 'err'), (f"{Id:04d}", 'num')) )
		if checkName:
			_l( ((" with name „", 'err'), (checkName, 'phr'), ("”", 'err')) )
		_l( ((" - probably removed…\n", 'err'),) )
		return None

	def getSectionByIdDiv0(it, sectId, ckn=''):
		sect = it.getSectionById(sectId, ckn)
		if sect:
			return sect.div0()

	def tuneSectionFontById(it, oldFS, newFS, Id, ckn=''):
		sect = it.getSectionById(Id, ckn)
		if sect:
			sect.tuneFontSize(oldFS, newFS, True)

	def tuneSectionFontByIdDiv0(it, oldFS, newFS, Id, ckn='', rule=0):
		sect = it.getSectionById(Id, ckn)
		if sect:
			dv = sect.div0()
			if rule:
				dv[rule-1].tuneFontSize(oldFS, newFS, True)
			else:
				dv.tuneFontSize(oldFS, newFS, True)

	def getSubsectionByName(it, name, verbose=True):
		for sect in it:
			for ssect in sect:
				if ssect.name==name:
					return sect.Id, ssect.Id, ssect
		if verbose:
			_l( (("Check subsection name „", 'err'),
				(name, 'phr'), ("” - probably removed…\n", 'err')) )
		return None

	def getSubsectionByIdDiv0(it, sectId, ssectId, ckn=''):
		ssect = it.getSubsecttionById(sectId, ssectId, ckn)
		if ssect:
			return ssect.div0()

	def getSubsecttionById(it, sectId, ssectId, checkName='', allId=True):
		sect = it.getSectionById(sectId)
		if sect:
			if allId:
				ssect = sect.getSubsecttionByAllId(ssectId)
			else:
				sect.getSubsecttionById(ssectId)
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
					_l( (("Subsection with name „", 'wrn'), (checkName, 'phr'),
						("” sId/ssId:", 'wrn'),
						(f"{sectId_n:04d}/{ssectId_n:04d}", 'num'),
						(" is different than expected:", 'wrn'),
						(f"{sectId:04d}/{ssectId:04d}", 'num'),
						(" - probably changed…\n", 'wrn')) )
					return ssect
		_l( (("Check section/subsection Id ", 'err'),
			(f"{sectId:04d}/{ssectId:04d}", 'num')) )
		if checkName:
			_l( ((" with name „", 'err'), (checkName, 'phr'), ("”", 'err')) )
		_l( ((" - probably removed…\n", 'err'),) )
		return None

	def tuneSubsectionFontById(it, oldFS, newFS, sectId, ssectId, ckn=''):
		ssect = it.getSubsecttionById(sectId, ssectId, ckn)
		if ssect:
			ssect.tuneFontSize(oldFS, newFS, True)

	def tuneSubsectionFontByIdDiv0(it, oldFS, newFS, sectId, ssectId, ckn='', rule=0):
		ssect = it.getSubsecttionById(sectId, ssectId, ckn)
		if ssect:
			dv = ssect.div0()
			if rule:
				dv[rule-1].tuneFontSize(oldFS, newFS, True)
			else:
				dv.tuneFontSize(oldFS, newFS, True)

