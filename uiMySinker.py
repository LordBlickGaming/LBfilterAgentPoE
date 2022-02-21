#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango, GLib
addTick, addIdle, unWatch = GLib.timeout_add, GLib.idle_add, GLib.source_remove

from os import path as ph
H = ph.expanduser('~') # Home dir
hh = lambda s: s.replace(H, '~')
from sys import stdout as sto
_p = lambda _str: sto.write(hh(str(_str)))
debug = (False, True)[1]
def _d(_str):
	if debug: _p(_str)
_l = None

dDialogs = dict(zip(
			'srch files opts'.split(),
			(f"{nm}UI" for nm in 'Search Files Options'.split()),
			))

class DlgProto:
	def __init__(it, ui):
		it.ui = ui
		it.mainWindow = ui.mainWindow
		it.pos = None
		it.dlg = None
		if hasattr(it, '_init') and(callable(it._init)):
			it._init()

	def Connections(it, dlg_discrm):
		handlers = {}
		for hn in (dr[3:] for dr in dir(it) if dr[:3]=='go_'):
			handlers[f"{dlg_discrm}{hn}"] = getattr(it, f"go_{hn}")
		return handlers

	is_visible = lambda it: it.dlg and(hasattr(it.dlg, 'is_visible'))\
		and(it.dlg.is_visible())

class SearchUI(DlgProto):
	def _init(it):
		it.found = None
		it.target_txtview = None
		tsf = Gtk.TextSearchFlags
		it.flags = tsf.TEXT_ONLY | tsf.VISIBLE_ONLY

	def dlgBinds(it):
		ui = it.ui
		dlg = it.dlg = ui.dlgSrch
		ui.Binds('eFind bSrchPrv bSrchNxt bSrchOK', dlg)
		dlg.show_all()
		ui.logView.changed = False # TODO: Implement blocking durring main proceeds, maybe threading?
		it.target_txtview = ui.logView

	def go_SrchUpdate(it, e):
		it.searchFor(e.get_text(), 'interactive')

	def go_SrchPrevious(it, b):
		dlg = it.dlg
		it.searchFor(it.dlg.eFind.get_text(), 'backward')

	def go_SrchNext(it, b):
		dlg = it.dlg
		it.searchFor(it.dlg.eFind.get_text(), 'forward')

	def searchFor(it, srch_txt, srch_type):
		if srch_txt:
			txtBuff = it.target_txtview.get_buffer()
			lastfound = it.found
			found = it.found = it.getFound(txtBuff, srch_type, srch_txt)
			if lastfound and(not(found)):
				found = it.found = it.getFound(txtBuff, srch_type, srch_txt)
			if found:
				it.target_txtview.scroll_to_iter (found[0], .1, False, .5, .5)
				txtBuff.select_range(*found)

	def getFound(it, txtBuff, srch_type, srch_txt):
		dlg = it.dlg
		if it.target_txtview.changed:
			print("skip")
			it.found = None
			it.target_txtview.changed = False
		if it.found:
			if srch_type in ('interactive', 'backward'):
				iterB = it.found[0]
			else:
				iterB = it.found[1]
		else:
			iterB = None
		if not(iterB):
			if srch_type in ('interactive', 'forward'):
				iterB = txtBuff.get_start_iter()
			else:
				iterB = txtBuff.get_end_iter()
		if srch_type in ('interactive', 'forward'):
			return iterB.forward_search(srch_txt, it.flags, None)
		else:
			return iterB.backward_search(srch_txt, it.flags, None)

	def dlgShow(it):
		ui = it.ui
		if it.dlg:
			it.dlg.set_visible(True)
		else:
			it.dlgBinds()
		dlg = it.dlg
		if it.pos:
			dlg.move(*it.pos)
		txtBuff = it.target_txtview.get_buffer()
		sel = txtBuff.get_selection_bounds()
		if sel:
			it.found = sel
			it.dlg.eFind.set_text(txtBuff.get_text(*sel, False))

	def dlgHide(it):
		if it.is_visible():
			dlg = it.dlg
			it.pos = dlg.get_position()
			dlg.set_visible(False)

	go_SrchOK = lambda it, b: it.dlgHide()

class FilesUI(DlgProto):
	def dlgBinds(it):
		ui = it.ui
		dlg = it.dlg = ui.dlgGetFN
		ui.Binds('buttFnOK buttFnCancel', dlg)
		dlg.show_all()

	def get_fn(it, startDir='', startFile='', filters=None, title='', act='file_open'):
		dlg = it.dlg
		if dlg:
			dlg.present()
		else:
			it.dlgBinds()
			dlg = it.dlg
		if not(dlg):
			print("WTF?!")
			print(f"dlg:{dlg},\nit.dlg:{it.dlg},\nui.dlgGetFN:{it.ui.dlgGetFN}")
			return
		fca = Gtk.FileChooserAction
		action = {
			'file_open':  fca.OPEN,
			'file_save':  fca.SAVE,
			'dir_open':   fca.SELECT_FOLDER,
			'dir_create': fca.CREATE_FOLDER,
			}[act]
		dlg.set_action(action)
		for f in dlg.list_filters():
			dlg.remove_filter(f)
		for fnFilter in filters:
			dlg.add_filter(fnFilter)
		allFilter = Gtk.FileFilter()
		allFilter.set_name("All files (*.*)")
		allFilter.add_pattern("*")
		dlg.add_filter(allFilter)
		if startDir:
			dlg.set_current_folder(startDir)
		if startFile:
			if act=='file_save':
				dlg.set_current_name(startFile)
			elif act=='file_open':
				dlg.set_filename(startFile)
		response = dlg.run()
		fn = ''
		if response == Gtk.ResponseType.OK:
			fn = dlg.get_filename()
		dlg.hide()
		if fn:
			return fn

class OptionsUI(DlgProto):
	def _init(it):
		it.lgsCheck = it.PreferencesStore = None
		it.League = it.ModName = it.Style = it.Strictness = ''
		it.lsUpdate = "League ModName Style Strictness".split()

	def dlgBinds(it):
		ui = it.ui
		dlg = it.dlg = ui.dlgOpts
		ui.Binds('bLeaguesOnline lsLeaguesOnline cbLeaguesOnline bCopyLeaguesSelection '\
			'eLeague eModName lsStrictness cbStrictness lsStyle cbStyle bOptsOK bOptsCancel', dlg)
		dlg.show_all()

	def go_GetPrefLeagues(it, b):
		if callable(it.lgsCheck):
			lgs = it.lgsCheck()
		else:
			return
		dlg = it.ui.dlgOpts
		
		dlg.lsLeaguesOnline.clear()
		for lgu in lgs:
			dlg.lsLeaguesOnline.append((lgu, ))
		lg = dlg.eLeague.get_text().replace('-', ' ')
		lgi = lgs.index(lg) if lg in lgs else 4
		dlg.cbLeaguesOnline.set_active(lgi)

	def go_SetSelLeague(it, b):
		dlg = it.ui.dlgOpts
		lgi = dlg.cbLeaguesOnline.get_active()
		print("Selected:%d" % lgi)
		if lgi < 0:
			return
		lgTxt = dlg.lsLeaguesOnline[lgi][0].replace(' ', '-')
		print("New League text:„%s”" % lgTxt)
		dlg.eLeague.set_text(lgTxt)

	def dlgShow(it, Strictneses, Styles, lgsCheck):
		ui = it.ui
		if it.dlg:
			it.dlg.present()
		else:
			it.dlgBinds()
		dlg = it.dlg
		if it.pos:
			dlg.move(*it.pos)
		dlg.eLeague.set_text(it.League)
		if callable(lgsCheck):
			it.lgsCheck = lgsCheck
		dlg.eModName.set_text(it.ModName)

		dlg.lsStrictness.clear()
		for Strictness in Strictneses:
			dlg.lsStrictness.append((Strictness,))
		strk = Strictneses.index(it.Strictness) if it.Strictness in Strictneses else 1
		dlg.cbStrictness.set_active(strk)

		dlg.lsStyle.clear()
		for Style in Styles:
			dlg.lsStyle.append((Style,))
		stl = Styles.index(it.Style) if it.Style in Styles else 0
		dlg.cbStyle.set_active(stl)
		dlg.set_keep_above(True)

	def dlgHide(it, update=False):
		if it.is_visible():
			dlg = it.dlg
			it.pos = dlg.get_position()
			if update:
				it.League = dlg.eLeague.get_text()
				it.ModName = dlg.eModName.get_text()
				strk = dlg.cbStrictness.get_active()
				if strk > -1:
					it.Strictness = dlg.lsStrictness[strk][0]
				stl = dlg.cbStyle.get_active()
				if stl > -1:
					it.Style = dlg.lsStyle[stl][0]
				if callable(it.PreferencesStore):
					it.PreferencesStore()
			dlg.hide()

	go_PrefOK     = lambda it, b: it.dlgHide(update=True)
	go_PrefCancel = lambda it, b: it.dlgHide()


class mySinker_UI:
	def __init__(ui, py_fn=''):
		ui.fontDesc = Pango.FontDescription('Univers,Sans Condensed 7')
		ui.fontColDesc = Pango.FontDescription('Univers Condensed CE 9')
		ui.fontFixedDesc = Pango.FontDescription('Monospace Bold 7')
		grt = Gtk.ResponseType
		ui.rspns = dict(map(lambda s: (int(getattr(grt, s)), f"Gtk.ResponseType.{s}"), sorted(
			filter(lambda a:a==a.upper() and(not(callable(getattr(grt, a)))), dir(grt)),
			key = lambda s: int(getattr(grt, s)), reverse=True)))
		ui.Init(py_fn=py_fn)
		if __name__ == "__main__":
			ui.bld.connect_signals(ui.Connections())
			ui.mainWindow.connect("destroy", lambda w: Gtk.main_quit())
			ui.buttQuit.connect("clicked", lambda w: Gtk.main_quit())
			_p = ui._p
			_p("Any logs appears here...\nThere's no any yet… \n")
			ui.buttConv.connect("clicked", ui.test)
			for _attr in dir(ui.logView):
				tatr = str(_attr)
				if tatr[0:2] == "tg":
					_p("\t%s\n" % tatr)
			ui.Enter()

	Enter = lambda ui: Gtk.main()
	Exit = lambda ui: Gtk.main_quit()
	Bind = lambda ui, w_nm, wgt=None:\
		setattr(wgt, w_nm, ui.bld.get_object(w_nm)) if isinstance(wgt, Gtk.Widget)\
		else setattr(ui, w_nm, ui.bld.get_object(w_nm))

	def Binds(ui, s_bnds, wgt=None):
		for w_nm in s_bnds.split():
			ui.Bind(w_nm, wgt=wgt)

	if __name__ == "__main__":
		def test(ui, butt):
			exampl_fn = '/examplePath/exampleFile.filter'
			_p = ui._p
			for txtslice, cTag in( ("Error in file:", 2), ("'", 0), (exampl_fn, 1),("'\n", 0) ):
				_p(txtslice, tag=(None, 'tgFlNm', 'tg_Err')[cTag])
			for txtslice, cTag in( ("Error in file:", 2), ("'", 0), (exampl_fn, 1),("'\n", 0) ):
				_p(txtslice, tag=(None, 'fnm', 'err')[cTag])
			for txtslice, cTag in( ("Error in file:", 2), ("'", 0), (exampl_fn, 1),("'\n", 0) ):
				_p(txtslice, tag=(None, ui.tgFlNm, ui.tg_Err)[cTag])
			insp_o = ui.tgFlNm
			_p(f"{str(insp_o)}\n")
			for _attr in dir(insp_o):
				r_attr = getattr(insp_o, _attr)
				tatr = str(_attr)
				if callable(r_attr):
					_p("\t")
					_p(f"{tatr}()", 'phr')
					_p(f"\n")
				else:
					_p(f"\t{tatr}\n")

	def Init(ui, py_fn=''):
		if not(py_fn):
			py_fn = ph.realpath(__file__)
		ui.runpath = py_dn = ph.dirname(py_fn)
		if __name__ == "__main__":
			py_fn = py_fn.replace('uiMySinker', 'mySinker')
			ui.cfg = {}
		ui.bld = Gtk.Builder()
		ui_fn = ph.join(py_dn, f"{ph.basename(py_fn).rsplit('.', 1)[0]}.ui")
		ui.bld.add_from_file(ui_fn)
		print(f"UI Filename:„{ui_fn}”")
		ui.Binds('mainWindow logView buttLastRel buttUnZip buttNumFix buttConv buttDiff '\
			'chkDbg buttPreferences toggWrap buttClear buttQuit '\
			'dsplZipFN dsplInFN dsplOutFN dlgOpts dlgGetFN dlgSrch')
		ui.mainWindow.show_all()
		ui.mainWindow.set_keep_above(True)
		global _l, _lp
		_l, _lp = ui._p, ui._lp
		ui.createTxtTags()

		ui.poeFilter = Gtk.FileFilter()
		ui.poeFilter.set_name("PoE item filter script (*.filter)")
		ui.poeFilter.add_pattern("*.filter")
		
		ui.poeFilterZip = Gtk.FileFilter()
		ui.poeFilterZip.set_name("PoE item filter pack by NeverSink (*.zip)")
		ui.poeFilterZip.add_pattern("*.zip")
		ui.txtFN = u'Use „Open” button to browse *.filter file →'

		for ui_attr in dDialogs.keys():
			g = globals()
			dlg_route = dDialogs[ui_attr]
			setattr(ui, ui_attr, g[dlg_route](ui))

	def Connections(ui):
		handlers = {}
		for ui_attr in dDialogs.keys():
			handlers.update( getattr(ui, ui_attr).Connections('dg_') )
		for hn in (dr[3:] for dr in dir(ui) if dr[:3]=='go_'):
			handlers[f"ui_{hn}"] = getattr(ui, f"go_{hn}")
		return handlers

	def createTxtTags(ui):
		logBuff = ui.logView.get_buffer()
		_B = Pango.Weight.BOLD
		ui.tgFlNm = logBuff.create_tag('fnm', weight = _B)
		ui.tgYllw = logBuff.create_tag('ylw', weight = _B)
		ui.tgPhrs = logBuff.create_tag('phr', weight = _B)
		ui.tg_Err = logBuff.create_tag('err', weight = _B)
		ui.tgWarn = logBuff.create_tag('wrn', weight = _B)
		ui.tgEnum = logBuff.create_tag('num', weight = _B)
		ui.tgSmrf = logBuff.create_tag('srf', weight = _B)
		for color_cfg, color_val in(
			('fgFlNm', 'yellow'),
			('fgYllw', '#FF5'),
			('fgPhrs', 'orange'), ('bgPhrs', '#002818'),
			('fg_Err', 'red'),
			('fgEnum', '#0F0'),
			('fgWarn', '#F85'),
			('fgSmrf', '#25E'),):
			tag_name = color_cfg.replace('bg', 'tg').replace('fg', 'tg')
			color = Gdk.color_parse(color_val)
			prop_name = {'bg': 'background-gdk', 'fg': 'foreground-gdk'}[color_cfg[0:2]]
			getattr(ui, tag_name).set_property(prop_name, color)

	go_Clear = lambda ui, *args: ui.logView.get_buffer().set_text('')
	go_Wrap = lambda ui, widget: ui.logView.set_wrap_mode((Gtk.WrapMode.NONE, Gtk.WrapMode.WORD)[widget.get_active()])

	def go_SrchLog(ui, b):
		sVis = not(ui.dlgSrch.is_visible())
		ui.srch.dlgShow() if sVis else ui.srch.dlgHide()

	def go_PhraseIcons(ui, ed, icoPos, sigEvent):
		if icoPos == Gtk.EntryIconPosition.SECONDARY:
			ed.set_text('')

	def _p(ui, txt, tag=None, short_path=False):
		buff = ui.logView.get_buffer()
		end = buff.get_end_iter()
		text = hh(txt) if short_path else txt
		if tag and(isinstance(tag, str)):
			tagTab = buff.get_tag_table()
			tagByNm = tagTab.lookup(tag)
			if tagByNm:
				tag = tagByNm
			elif hasattr(ui, tag):
				tag = getattr(ui, tag)
			else:
				tag = None
		if not(isinstance(tag, Gtk.TextTag)):
			buff.insert(end, text)
			return
		buff.insert_with_tags(end, text, tag)

	def _lp(ui, ls_txt, short_path=True):
		for idx, txt_obj in enumerate(ls_txt):
			if isinstance(txt_obj, str):
				ui._p(txt_obj, short_path=short_path)
			elif isinstance(txt_obj, tuple) and len(txt_obj)==2:
				ui._p(txt_obj[0], tag=txt_obj[1], short_path=short_path)
			else:
				raise TypeError(f"Unknown format in {ls_txt}[{idx}]")

	def restoreGeometry(ui):
		for ui_attr in dDialogs.keys():
			dlg_cfg_nm = f"dlg{ui_attr.capitalize()}Pos"
			if hasattr(ui, ui_attr) and(ui.cfg[dlg_cfg_nm]):
				dlg_inst = getattr(ui, ui_attr)
				dlg_inst.pos =  tuple(int(k) for k in ui.cfg[dlg_cfg_nm].split(','))
		ui.setTxtWinGeometry(ui.mainWindow, ui.cfg['MainWindowGeometry'])

	def storeGeometry(ui):
		for ui_attr in dDialogs.keys():
			if hasattr(ui, ui_attr):
				dlg_inst, dlg_cfg_nm = getattr(ui, ui_attr), f"dlg{ui_attr.capitalize()}Pos"
				if hasattr(dlg_inst, 'dlgHide'): dlg_inst.dlgHide()
				if dlg_inst.pos:
					x, y = dlg_inst.pos
					ui.cfg[dlg_cfg_nm] = f"{x:d},{y:d}"
		ui.cfg['MainWindowGeometry'] = ui.getTxtWinGeometry(ui.mainWindow)


	def getWinGeometry(ui, win):
		pos = win.get_position()
		size = win.get_size()
		return pos.root_x, pos.root_y, size.width, size.height

	def getTxtWinGeometry(ui, win):
		geo = ui.getWinGeometry(win)
		txtGeo = ','.join(map(lambda i: f"{i}", geo))
		dlgName = win.get_title()
		_d(f"Current Window „{dlgName}” geometry: {txtGeo}\n")
		return txtGeo

	def setWinGeometry_timed(ui, win, geo):
		_d(f"Repositioning Window: „{win.get_title()}” to:\n")
		_d(f"pos: x:{geo[0]}, y:{ geo[1]}\n")
		_d(f"size: w:{geo[2]}, h:{geo[3]}\n")
		gdw = win.get_window()
		gdw.move_resize(*geo)
		return False # run only once

	def setWinGeometry(ui, win, geo):
		addIdle(ui.setWinGeometry_timed, win, geo)

	def setTxtWinGeometry(ui, win, txtGeo):
		geo = tuple(map(int, txtGeo.split(','))) if txtGeo else tuple()
		if len(geo)==4:
			ui.setWinGeometry(win, geo)
		else:
			_d(f"Strange geo situation:{geo}\n")

# Entry point
if __name__ == "__main__":
	mySinker_UI()
