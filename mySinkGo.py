#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

#ver: 8.5.0b

from clFilterPoE import nvrsnkSections, Rule, _dv, _range

def sinkConvert(fn_in, fn_out, dbg, _p, _d):
	inFS = nvrsnkSections(logger=_p, debug=dbg)
	ssUp = ( (6002, 'Hide All known Section'), (4804, 'Show All unknown Section') )
	inFS.load(fn_in, ssPromotes=ssUp)
	if not(inFS.load_fn):
		return
	def tfs(slice_, old, new, noMatchErr=False):
			for rule in slice_:
				rule.tuneFontSize(old, new, noMatchErr)
	############################################################################################################################################
	#Oni-Goroshi Farm
	sect = inFS.getSectionById(100, "Global overriding rules")
	if sect:
		txtRule = '\nShow # Goldrim chance base on Twilight Strand\n'
		txtRule += 'Class "Helmets"\nBaseType "Leather Cap"\n'
		txtRule += 'Rarity Normal\n'
		txtRule += 'ItemLevel 3\n'
		txtRule += 'SetFontSize 40\n'
		txtRule += 'SetTextColor 255 255 255\n'
		txtRule += 'SetBorderColor 0 200 0 190\n'
		txtRule += 'SetBackgroundColor  80 170 100 128\n'
		txtRule += '\n'
		linesRule =  tuple(line.strip() for line in txtRule.splitlines())
		opDiv = sect.div0()
		newRule = Rule(opDiv)
		acquired = newRule.load(linesRule)
		opDiv.insert(0, newRule)
		#
		txtRule = '\nShow # Show quality evasion Shields\n'
		txtRule += 'Class "Shields"\nBaseType "Buckler"\n'
		txtRule += 'Rarity Normal\n'
		txtRule += 'Quality >= 15\n'
		txtRule += 'SetFontSize 30\n'
		txtRule += 'SetTextColor 255 255 255\n'
		txtRule += 'SetBorderColor 0 200 0 190\n'
		txtRule += 'SetBackgroundColor  80 170 100 128\n'
		txtRule += '\n'
		linesRule =  tuple(line.strip() for line in txtRule.splitlines())
		newRule = Rule(opDiv)
		acquired = newRule.load(linesRule)
		opDiv.insert(1, newRule)
	#manipulate chisel recipe
	ssect = inFS.getSubsecttionById(1000, 1006, "Chisel Recipes")
	if ssect:
		rules = ssect[0].rules()
		if len(rules):
			for rule in rules:
				q = rule.get_cond_args('Quality_Hi')
				r = rule.get_cond_args('Rarity_Hi')#[0]
				if q==('>', '17') and(r) and(r[0]=='Magic'):
					rule.activate()
				elif not(q) and(r) and(r[0]=='Normal'):
					rule.Conditions['Quality'] = (True, ('>=', '5'), 0, '')
					rule.activate()
	#lower Font Size
	# Gems
	ssect = inFS.getSubsecttionById(2700, 2703, "High Quality and Leveled Gems")
	if ssect:
		ssect.tuneFontByBase(35, 34, "Vaal")
		ssect.tuneFontByCmt(40, 34, "$tier->lt4")
		ssect.tuneFontByCmt(40, 34, "%H2")
		ssect.tuneFontByCmt(45, 34, "$tier->firstzone")
		#ssect.tuneFontByCmt(40, 32, "%D5")
		# Quality gems, Size OK, but frame…
		for cmt in "qt3 qt4".split():
			rule = ssect.srch_rule_comments(cmt)[0]
			if rule:
				rule.setColor("SetBorderColor", 255, 255, 255, 200)
	sect = inFS.getSectionById(1200, "Endgame Flasks")
	if sect:
		sect.tuneFontSize(35, 30)
		sect.tuneFontSize(40, 33)
		sect.tuneFontSize(45, 36)
		rules = sect.srch_rule_txtype("Quicksilver Flask", True)
		for rule in rules:
			rule.Actions.deactivate('PlayAlertSound')
	ssect = inFS.getSubsecttionById(3300, 3302, "Scarabs")
	if ssect:
		#ssect.tuneFontByCmt(45, , "$tier->t1")
		ssect.tuneFontByCmt(45, 42, "$tier->t2")
		ssect.tuneFontByCmt(45, 40, "$tier->t3")
		ssect.tuneFontByCmt(45, 38, "$tier->t4")
		ssect.tuneFontByCmt(45, 36, "$tier->restex")
	ssect = inFS.getSubsecttionById(3300, 3303, "Regular Fragment Tiering")
	if ssect:
		#ssect.tuneFontByCmt(45, , "$tier->t1")
		ssect.tuneFontByCmt(45, 42, "$tier->t2")
		ssect.tuneFontByCmt(45, 40, "$tier->t3")
		ssect.tuneFontByCmt(45, 38, "$tier->t4")
		ssect.tuneFontByCmt(45, 36, "$tier->restex")
	'''
	inFS.tuneSectionFontById(45, , "", )
	'''
	ssect = inFS.getSubsecttionById(3500, 4702, "Supplies: High Stacking") #funny mistake of someone
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$tier->t2")
		ssect.tuneFontByCmt(45, 40, "$tier->t3")
	ssect = inFS.getSubsecttionById(3500, 3501, "Supplies: Low Stacking")
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$tier->t2")
		ssect.tuneFontByCmt(45, 40, "$tier->t3")
	ssect = inFS.getSubsecttionById(3500, 3502, "Supplies: Portal Stacking")
	if ssect:
		ssect.tuneFontByCmt(45, 40, "$tier->t2")
		ssect.tuneFontByCmt(40, 35, "$tier->t3")
	ssect = inFS.getSubsecttionById(3500, 3503, "Supplies: Wisdom Stacking")
	if ssect:
		ssect.tuneFontByCmt(45, 40, "$tier->t2")
		ssect.tuneFontByCmt(40, 35, "$tier->t3")
	inFS.tuneSubsectionFontByIdDiv0(45, 38, 3500, 3507, "Heist Coins")
	#inFS.tuneSectionFontById( 45, 35, 3400, "Currency - Exceptions - Leveling Currencies")
	sect = inFS.getSectionById(3600, "Currency - Regular Currency Tiering")
	if sect:
		ssect = sect[0]
		ssect.tuneFontByCmt(45, 42, "$tier->t3")
		ssect.tuneFontByCmt(45, 40, "$tier->t4")
		ssect.tuneFontByCmt(45, 40, "$tier->t5")
		ssect.tuneFontByCmt(45, 38, "$tier->t6chrom")
		ssect.tuneFontByCmt(45, 38, "$tier->t7chance", ("SetBackgroundColor", 190, 178, 0, 255))
		ssect.tuneFontByCmt(45, 36, "$tier->t8trans")
		ssect.tuneFontByCmt(40, 32, "$tier->t9armour")
		# "Portal Scroll"
		ssect.tuneFontByCmt(40, 32, "$tier->tportal")
		#  "Scroll of Wisdom"
		ssect.tuneFontByCmt(40, 32, "$tier->twisdom")
		# bye bye Silver Coin…
	ssect = inFS.getSubsecttionById(3700, 3702, "Delve - Resonators")
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$type->currency->resonator $tier->t1")
		ssect.tuneFontByCmt(45, 40, "$type->currency->resonator $tier->t2")
		#rule_cm = "$type->currency->resonator $tier->t3"
		#ssect.ruleOnByCmt(rule_cm)
		#ssect.tuneFontByCmt(45, 38, rule_cm)
		ssect.tuneFontByCmt(45, 38, " $type->currency->resonator $tier->restex")
	#ssect = inFS.getSubsecttionById(4900, 4905, "Delirium Currency")
	ssect = inFS.getSubsecttionById(3700, 3703, "Delve - Fossils")
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$type->currency->fossil $tier->t2")
		ssect.tuneFontByCmt(45, 40, "$type->currency->fossil $tier->t3")
		ssect.tuneFontByCmt(45, 38, "$type->currency->fossil $tier->t4")
		ssect.tuneFontByCmt(45, 36, " $type->currency->fossil $tier->restex")
	ssect = inFS.getSubsecttionById(3700, 3704, "Blight - Oils")
	if ssect:
		#ssect.ruleOnByCmt(          "$type->currency->oil $tier->t1")
		ssect.tuneFontByCmt(45, 42, "$type->currency->oil $tier->t2")
		ssect.tuneFontByCmt(45, 40, "$type->currency->oil $tier->t3")
		ssect.tuneFontByCmt(45, 38, "$type->currency->oil $tier->t4")
		ssect.tuneFontByCmt(45, 36, "$type->currency->oil $tier->restex")
	ssect = inFS.getSubsecttionById(3700, 3705, "Expedition Currencies")
	ssect = inFS.getSubsecttionById(3700, 3706, "Essences")
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$type->currency->essence $tier->t2")
		ssect.tuneFontByCmt(45, 40, "$type->currency->essence $tier->t3")
		ssect.tuneFontByCmt(45, 38, "$type->currency->essence $tier->t4")
		ssect.tuneFontByCmt(45, 36, "$type->currency->essence $tier->t5")
		ssect.tuneFontByCmt(45, 34, "$type->currency->essence $tier->t6")
	ssect = inFS.getSubsecttionById(3700, 3707, "Incubators")
	if ssect:
		#ssect.ruleOnByCmt(          "$type->currency->incubators $tier->t1")
		ssect.tuneFontByCmt(45, 42, "$type->currency->incubators $tier->t2")
		ssect.tuneFontByCmt(45, 40, "$type->currency->incubators $tier->t3")
		ssect.tuneFontByCmt(45, 38, "$type->currency->incubators $tier->t4")
		ssect.tuneFontByCmt(45, 36, "$type->currency->incubators $tier->restex")
	#ssect = inFS.getSubsecttionById(3700, 3708, "Archnemesis Mods") Somebody misses new secton
	if ssect:
		#ssect.ruleOnByCmt(          "$type->exotic->archnemesis $tier->reagents")
		ssect.tuneFontByCmt(45, 42, "$type->exotic->archnemesis $tier->special")
		ssect.tuneFontByCmt(45, 40, "$type->exotic->archnemesis $tier->results")
		ssect.tuneFontByCmt(45, 38, "$type->exotic->archnemesis $tier->restex")
	ssect = inFS.getSubsecttionById(3700, 3708, "Others")
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$type->currency->others $tier->harbinger")
		ssect.tuneFontByCmt(45, 42, "$type->currency->others $tier->misc")
	ssect = inFS.getSubsecttionById(3800, 5112, "Breach and Legion Splinters") # !sid→ssid WAT?!
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$type->currency->splinter $tier->t2")
		ssect.tuneFontByCmt(40, 38, "$type->currency->splinter $tier->t3")
	ssect = inFS.getSubsecttionById(3800, 3801, "Simulacrum Splinters")
	if ssect:
		ssect.tuneFontByCmt(45, 42, "$type->currency->splinter->simulacrum $tier->t2")
		ssect.tuneFontByCmt(45, 42, "$type->currency->splinter->simulacrum $tier->t3")
		ssect.tuneFontByCmt(45, 40, "$type->currency->splinter->simulacrum $tier->t4")
		ssect.tuneFontByCmt(45, 38, "$type->currency->splinter->simulacrum $tier->t5")
	sect = inFS.getSectionById(3900, "Divination Cards")
	if sect:
		ssect = sect[0] # default no name
		ssect.tuneFontByCmt(45, 42, "$type->divination $tier->t2")
		ssect.tuneFontByCmt(45, 42, "$type->divination $tier->t3")
		ssect.tuneFontByCmt(45, 40, "%H5 $type->divination $tier->t4c")
		ssect.tuneFontByCmt(45, 38, "%H3 $type->divination $tier->t5c")
		ssect.tuneFontByCmt(45, 40, "%HS3 $type->divination $tier->t4")
		ssect.tuneFontByCmt(35, 38, "%H1 $type->divination $tier->t5")
		ssect.tuneFontByCmt(45, 36, "$type->divination $tier->restex")

	#sect = inFS.getSecttionById(4500, "Hide outdated flasks")
	#show highest tiers of mana/life flasks
	ssect = inFS.getSubsecttionById(4600, 6002, "Utility Flasks")
	if ssect:
		for rule in ssect[0]:
			if isinstance(rule, Rule):
				rule.Actions.del_cmd('PlayAlertSound')
				rule.Actions.del_cmd('PlayEffect')
				rule.Actions.del_cmd('MinimapIcon')
		ssect.tuneFontByCmt(45, 40, "$type->leveling->flasks->utility $tier->quicksilver")
	inFS.tuneSectionFontByIdDiv0( 45, 42, 5700, "Quest Items and Event Items")
	dv = inFS.getSectionByIdDiv0(6000, "Leveling - Merged Rules")
	if dv:
		dv.tuneFontSize(45, 35, True)
		for rule in dv:
			rule.Actions.del_cmd('PlayAlertSound')
	dv = inFS.getSectionByIdDiv0(6100, "Leveling - RGB Recipes")
	if dv:
		tfs(dv[0:2], 45, 40)
		tfs(dv[2:4], 36, 32)
		w = dv[1].get_cond_args('Width_Hi')
		if w==('<=', '1'):
			dv[1].replace_cond_args('Width_Hi', ('1',))
		dv[2].new_cond_args('AreaLevel_Hi', ('<=', '67'), 41, ' No respect for huge chromatic orb on maps')
	dv = inFS.getSubsectionByIdDiv0(6200, 6201, "Leveling rares - specific items")
	if dv:
		dv.tuneFontSize(45, 34, True)
		for rule in dv:
			rule.Actions.del_cmd('PlayAlertSound')
	dv = inFS.getSubsectionByIdDiv0(6200, 6203, "Leveling rares - Caster")
	if dv:
		dv[0].tuneFontSize(45, 34, True)
		dv[1].tuneFontSize(40, 32, True)
	dv = inFS.getSubsectionByIdDiv0(6200, 6204, "Leveling rares - Melee Weapons")
	if dv:
		tfs(dv[:2], 45, 34, True)
		tfs(dv[2:], 40, 32, True)
	dv = inFS.getSubsectionByIdDiv0(6200, 6205, "Leveling rares - Ranged")
	if dv:
		tfs(dv[:2], 45, 34, True)
		tfs(dv[2:], 40, 32, True)
	dv = inFS.getSubsectionByIdDiv0(6200, 6206, "Leveling rares - Quivers")
	if dv:
		dv[0].tuneFontSize(45, 34, True)
		dv[1].tuneFontSize(40, 32, True)
	inFS.tuneSubsectionFontByIdDiv0(36, 32, 6200, 6207, "Leveling rares - remaining rules")
	#lower Font Size of unsorted by level 4L
	#ssect = inFS.getSubsecttionById(6300, 6301, "Linked gear - 4links")
	dv = inFS.getSubsectionByIdDiv0(6300, 6301, "Linked gear - 4links")
	if dv:
		dv.tuneFontSize(45, 36, True)
		for rule in dv:
			rule.Actions.del_cmd('PlayAlertSound')
	#lower Font Size of unsorted by level 3L
	dv = inFS.getSubsectionByIdDiv0(6300, 6302, "Linked gear - 3links")
	if dv:
		dv[0].tuneFontSize(36, 32, True)
	dv = inFS.getSubsectionByIdDiv0(6300, 6303, "Act1")
	if dv:
		tfs(dv[:3], 45, 36, True)
		dv[3].tuneFontSize(40, 34, True)
		dv[4].tuneFontSize(36, 32, True)
	#summoner recipe shield
	ssect = inFS.getSubsecttionById(6300, 6306, "Optional Recipes")
	if ssect:
		ssect.activate()
	# quality, lvl, nonmf
	ssect = inFS.getSubsecttionById(6300, 6307, "20% quality items for those strange people who want them")
	if ssect:
		ssect.activate()
	#enable lvl, small
	ssect = inFS.getSubsecttionById(6500, 6503, "Vendor Normal items - Until level 3 (Remaining)")
	if ssect:
		ssect.activate()
	# Show Magic jewelery for Regal→Scouring recipe
	bScourRecipe = 1
	if bScourRecipe:
		def ruleVendScour(rule):
			rgba_Brdr = "SetBorderColor", 0, 200, 0, 190
			rgba_Bkg = "SetBackgroundColor", 80, 170, 100, 128
			rl_cmt = "Regal/Scouring candidates"
			rule.recomment(rl_cmt)
			rule.replace_cond_args('Mirrore', ('False',))
			rule.replace_cond_args('Corrupted', ('False',))
			rule.del_cond('ItemLevel')
			rule.setColor(*rgba_Brdr)
			rule.setColor(*rgba_Bkg)
		dv = inFS.getSectionByIdDiv0(3000,"HIDE LAYER 1 - MAGIC AND NORMAL ITEMS")
		if dv:
			rule = dv[0]
			rule.replace_cond_args('Rarity_Hi', ('Normal',))
			rule = rule.duplicate()
			rule.replace_cond_args('Rarity_Hi', ('Magic',))
			for bt in "Amulets Rings Belts Boots Gloves Helmets One_Hand Shields Claws Daggers Rune_Dagger Wand".split():
				rule.del_txtype(bt.replace('_', ' '), 'Class')
			rule = rule.duplicate()
			rule.replace_cond_args('Class', ('"One Hand"',))
			rule.new_cond_args('Width_Hi', ('2',))
			rule = rule.duplicate()
			rule.del_cond('Width_Hi')
			rule.new_cond_args('Height_Hi', ('>=', '3'))
			rule.replace_cond_args('Class', ('Shields',))
		dv = inFS.getSubsectionByIdDiv0(6600, 6603, "Vendor Magic items - Jewellery")
		if dv and(len(dv)>=2):
			rule = dv[1].copy()
			ruleVendScour(rule)
			dv.insert(-1, rule)
		dv = inFS.getSubsectionByIdDiv0(6600, 6604, "Vendor Magic items - Until 24")
		if dv:
			rule = dv[1]
			ruleVendScour(rule)
			rule.replace_cond_args('Width_Hi', ('2',))
			rule.replace_cond_args('Height_Hi', ('2',))
			rule = dv[0].duplicate()
			ruleVendScour(rule)
			rule.replace_cond_args('Width_Hi', ('1',))
			rule.replace_cond_args('Height_Hi', ('3',))
	# show, tune font, insert rule from text
	sect = inFS.getSectionById(6700, "HIDE LAYER 5 - Remaining Items")
	for sect in inFS:
		for ssect in sect:
			for div in ssect:
				for rule in div.rules():
					if rule.get_cond_args('LinkedSockets_Hi')[-1]=='4':
						rule.Actions.del_cmd('PlayAlertSound')
	############################################################################################################################################
	inFS.store(fn_out)
