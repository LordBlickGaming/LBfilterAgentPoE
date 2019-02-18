#!/usr/bin/python2
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

from wgts import gtk, pango, goStr
import wgts as wg
lsFiles = 'Zip In Out'.split()
LO_ROWS = len(lsFiles)+1

class Dialogs:
	def __init__(it, ui, mainWindow):
		it.ui = ui
		it.mainWindow = mainWindow
		#it.textView = textView
		it.lgsCheck = it.dlgPreferences = it.PreferencesStore = it.dlgPrefPos = None
		it.League = it.ModName = it.Style = it.Strictness = ''
		it.lsUpdate = "League ModName Style Strictness".split()

	def dlgPreferencesCreate(it):
		dlg = it.dlgPreferences = gtk.Window(gtk.WINDOW_TOPLEVEL)
		if hasattr(it.ui, 'accGroup'):
			dlg.add_accel_group(it.ui.accGroup)
		dlg.set_border_width(5)
		#dlg.set_size_request(200, 100)
		dlg.set_resizable(False)
		dlg.set_title('Options and preferences')
		dlg.set_modal(True)
		dlg.set_transient_for(it.mainWindow)
		dlg.set_destroy_with_parent(True)
		dlg.set_deletable(False)
		dlg.set_skip_taskbar_hint(False)
		# # # # # # # # # # # # # # # # # # # # # # # # #
		dlgFrame = gtk.Fixed()

		vb = gtk.VBox(False, 10)
		dlg.add(vb)

		hb = gtk.HBox(False, 5)
		l = gtk.Label("Current League name:")
		hb.pack_start(l, True, False, 0)
		e = dlg.eLeague = gtk.Entry()
		hb.pack_start(e, True, True, 0)
		vb.pack_start(hb, True, False, 0)
		hb = gtk.HBox(False, 5)
		bLeaguesOnline = gtk.Button("Load Leagues Online →")
		hb.pack_start(bLeaguesOnline, True, False, 0)
		bLeaguesOnline.connect("clicked", lambda xargs: it.getDlgPrefLeagues())
		dlg.lsLeaguesOnline = gtk.ListStore(goStr,)
		dlg.cbLeaguesOnline = gtk.ComboBox(dlg.lsLeaguesOnline)
		cellRendr = gtk.CellRendererText()
		dlg.cbLeaguesOnline.pack_start(cellRendr)
		dlg.cbLeaguesOnline.set_attributes(cellRendr, text=0)
		hb.pack_start(dlg.cbLeaguesOnline, True, False, 0)
		bCopyLeaguesSelection = gtk.Button("↑Copy↑")
		hb.pack_start(bCopyLeaguesSelection, True, False, 0)
		bCopyLeaguesSelection.connect("clicked", lambda xargs: it.setDlgSelLeague())
		vb.pack_start(hb, True, False, 0)

		hb = gtk.HBox(False, 5)
		l = gtk.Label("Modified filter base name:")
		hb.pack_start(l, True, False, 0)
		e = dlg.eModName = gtk.Entry()
		hb.pack_start(e, True, False, 0)
		vb.pack_start(hb, True, False, 0)

		hb = gtk.HBox(False, 5)
		l = gtk.Label("Select Strictness:")
		hb.pack_start(l, True, False, 0)
		dlg.lsStrictness = gtk.ListStore(goStr, )
		dlg.cbStrictness = gtk.ComboBox(dlg.lsStrictness)
		cellRendr = gtk.CellRendererText()
		dlg.cbStrictness.pack_start(cellRendr)
		dlg.cbStrictness.set_attributes(cellRendr, text=0)
		hb.pack_end(dlg.cbStrictness, True, True, 0)
		vb.pack_start(hb, True, False, 0)

		hb = gtk.HBox(False, 5)
		l = gtk.Label("Select Style:")
		hb.pack_start(l, True, False, 0)
		dlg.lsStyle = gtk.ListStore(goStr, )
		dlg.cbStyle = gtk.ComboBox()
		dlg.cbStyle.set_model(dlg.lsStyle)
		cellRendr = gtk.CellRendererText()
		dlg.cbStyle.pack_start(cellRendr)
		dlg.cbStyle.set_attributes(cellRendr, text=0)
		hb.pack_end(dlg.cbStyle, True, True, 0)
		vb.pack_start(hb, True, False, 0)

		hb = gtk.HBox(False, 5)
		bOK = gtk.Button("OK",)
		bOK.connect("clicked", lambda xargs: it.hideDlgPref(True))
		hb.pack_end(bOK, True, False, 30)
		bCancel = gtk.Button("Cancel")
		bCancel.connect("clicked", lambda xargs: it.hideDlgPref())
		hb.pack_end(bCancel, True, False, 0)
		vb.pack_start(hb, True, False, 0)
		dlg.show_all()

	def getDlgPrefLeagues(it):
		if callable(it.lgsCheck):
			lgs = it.lgsCheck()
		else:
			return
		dlg = it.dlgPreferences
		
		dlg.lsLeaguesOnline.clear()
		for lgu in lgs:
			dlg.lsLeaguesOnline.append((lgu, ))
		lg = dlg.eLeague.get_text().replace('-', ' ')
		lgi = lgs.index(lg) if lg in lgs else 4
		dlg.cbLeaguesOnline.set_active(lgi)

	def setDlgSelLeague(it):
		dlg = it.dlgPreferences
		lgi = dlg.cbLeaguesOnline.get_active()
		print("Selected:%d" % lgi)
		if lgi < 0:
			return
		lgTxt = dlg.lsLeaguesOnline[lgi][0].replace(' ', '-')
		print("New League text:„%s”" % lgTxt)
		dlg.eLeague.set_text(lgTxt)

	def showDlgPref(it, Strictneses, Styles, lgsCheck):
		if it.dlgPreferences:
			it.dlgPreferences.present()
		else:
			it.dlgPreferencesCreate()
		dlg = it.dlgPreferences
		if it.dlgPrefPos:
			dlg.move(*it.dlgPrefPos)
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

	def hideDlgPref(it, update=False):
		dlg = it.dlgPreferences
		if dlg and(dlg.get_property("visible")):
			it.dlgPrefPos = dlg.get_position()
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


class mySinker_UI:
	def __init__(ui):
		ui.fontDesc = pango.FontDescription('Univers,Sans Condensed 7')
		ui.fontColDesc = pango.FontDescription('Univers Condensed CE 9')
		ui.fontFixedDesc = pango.FontDescription('Terminus,Monospace Bold 7')
		ui.uiInit()
		ui.createTxtTags()
		if __name__ == "__main__":
			ui.mainWindow.connect("destroy", lambda w: gtk.main_quit())
			ui.buttonExit.connect("clicked", lambda w: gtk.main_quit())
			_p = ui.logView.insert_end
			_p("Any logs appears here...\nThere's no any yet… \n")
			ui.buttonConvert.connect("clicked", ui.test)
			for _attr in dir(ui.logView):
				tatr = str(_attr)
				if tatr[0:2] == "tg":
					_p("\t%s\n" % tatr)
			ui.uiEnter()

	uiEnter = lambda ui: gtk.main()
	uiExit = lambda ui: gtk.main_quit()

	if __name__ == "__main__":
		def test(ui, butt):
			lv = ui.logView
			_p = lv.insert_end
			for txtslice, cTag in( ("Error in file:", 2), ("'", 0), ('/examplePath/exampleFile.filter', 1),("'\n", 0) ):
				_p(txtslice, tag=(None, 'tgFileName', 'tgErr')[cTag])
			insp_o = lv.tgFileName
			_p("%s\n"% str(insp_o))
			for _attr in dir(insp_o):
				tatr = str(_attr)
				_p("\t%s\n" % tatr)
			for txtslice, cTag in( ("Error in file:", 2), ("'", 0), ('/examplePath/exampleFile.filter', 1),("'\n", 0) ):
				_p(txtslice, tag=(None, lv.tgFileName, lv.tgErr)[cTag])

	def uiInit(ui):
		from os import path as ph
		ui.runpath = ph.dirname(ph.realpath(__file__))
		if __name__ == "__main__":
			ui.cfg = {}
		wg.Height = 25
		ui.title = 'Path Of Exile Loot Filter Customize…'
		ui.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		w, h, ui.hgtLower = (500, 400, wg.Height*(LO_ROWS+1))
		ui.mainWindow.set_geometry_hints(min_width=w, min_height=h)
		ui.mainWindow.set_size_request(w, h)
		ui.mainWindow.set_title(ui.title)
		ui.mainWindow.set_border_width(5)
		ui.accGroup = gtk.AccelGroup()
		ui.mainWindow.add_accel_group(ui.accGroup)
		
		mfm = ui.mnFx = gtk.Fixed()

		ui.logView = wg.TextView(mfm, 5, 5, 0, 0,
			bEditable=False, tabSpace=4, fontDesc = ui.fontFixedDesc)

		ui.txtFN = u'Use „Open” button to browse *.filter file →'
		from wgts import getTxtPixelWidth
		ui.lw = 0
		for select in lsFiles:
			txtLabel = "%s File:" % select
			lb = wg.Label(txtLabel, mfm, 0, 0, 60)
			lw = getTxtPixelWidth(lb, txtLabel, fontDesc=ui.fontDesc)+5
			ui.lw = max(ui.lw, lw)
			lb.set_size_request(lw-2, wg.Height)
			setattr(ui, 'labFilename' + select, lb)
			if __name__ == "__main__":
				print(u"Label „%s” size: %d" % (txtLabel, lw))
				dsplFilename = wg.Butt(ui.txtFN, mfm, 0, 0, 0)
			else:
				dsplFilename = wg.Label(ui.txtFN,
					mfm, 0, 0, 0, xalign=0., selectable=True)
			setattr(ui, 'dsplFilename' + select, dsplFilename)
			bt = wg.Butt(None, mfm, 0, 0, 30, stockID=gtk.STOCK_OPEN) #"Set FileName..."
			setattr(ui, 'buttonFileName' + select, bt)


		ui.buttonUnZip = wg.Butt(None, mfm, 0, 0, 30, fileImage=ph.join(ph.dirname(ph.abspath(__file__)), 'ico/package.svg')) #"Proceed..."
		ui.buttonConvert = wg.Butt(None, mfm, 0, 0, 30, stockID=gtk.STOCK_CONVERT) #"Proceed..."
		ui.buttonDiff = wg.Butt("Diff", mfm, 0,  0, 50)

		ui.chkDbg = wg.Check("Debug", mfm, 0,  0, 50)

		ui.toggWrap = wg.Toggle("Wrap words", mfm, 0,  0, 70)

		ui.buttonPreferences = wg.Butt(None, mfm, 0, 0, 30, stockID=gtk.STOCK_PREFERENCES)

		ui.buttonClear = wg.Butt("Clear", mfm, 0,  0, 50)

		ui.buttonExit = wg.Butt("Exit (Ctrl+Q)", mfm, 0, 0, 80)
		ui.buttonExit.add_accelerator("clicked", ui.accGroup, ord('Q'),
			gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)

		ui.mainWindow.add(mfm)
		ui.mainWindow.show_all()
		ui.mainWindow.set_keep_above(True)
		ui.lastWinSize = None
		ui.buttonClear.connect("clicked", lambda xargs: ui.logView.clear_text())
		ui.mainWindow.connect("configure-event", ui.uiSize)
		ui.toggWrap.connect("toggled", ui.appWrap)
		
		ui.poeFilter = gtk.FileFilter()
		ui.poeFilter.set_name("PoE item filter script (*.filter)")
		ui.poeFilter.add_pattern("*.filter")
		
		ui.poeFilterZip = gtk.FileFilter()
		ui.poeFilterZip.set_name("PoE item filter pack by NeverSink (*.zip)")
		ui.poeFilterZip.add_pattern("*.zip")

		ui.dlgs = Dialogs(ui, ui.mainWindow)

	def createTxtTags(ui):
		lv = ui.logView
		lb = lv.get_buffer()
		lv.tgFileName = lb.create_tag('filename', weight = pango.WEIGHT_BOLD, foreground = 'yellow')
		lv.tgPhrase = lb.create_tag('phrase', weight = pango.WEIGHT_BOLD, foreground = 'orange')
		lv.tgWarn = lb.create_tag('warning', weight = pango.WEIGHT_BOLD, foreground = '#FD0')
		lv.tgErr = lb.create_tag('error', weight = pango.WEIGHT_BOLD, foreground = 'red')
		lv.tgEnum = lb.create_tag('line_number', weight = pango.WEIGHT_BOLD, foreground = '#0F0')

	def uiSize(ui, window, event):
		if event.type==wg.gtk.gdk.CONFIGURE:
			w, h = event.width, event.height
			if ui.lastWinSize==(w, h):
				return True
			ui.lastWinSize = w, h
			wgH = wg.Height
			mfm = ui.mnFx
			ha = h - ui.hgtLower - 10
			ui.logView.size(w-20, ha)
			y = ha + 10
			lw = ui.lw
			for select in lsFiles:
				labFilename = getattr(ui, 'labFilename' + select)
				mfm.move(labFilename, 0, y)
				dsplFilename = getattr(ui, 'dsplFilename' + select)
				dsplFilename.size(w-50-lw, wgH)
				mfm.move(dsplFilename, lw, y)
				bt = getattr(ui, 'buttonFileName' + select)
				mfm.move(bt, w-45, y)
				y += wg.Height+5
			mfm.move(ui.buttonUnZip, 0, y)
			mfm.move(ui.buttonConvert, 35, y)
			mfm.move(ui.buttonDiff, 70, y)
			mfm.move(ui.chkDbg, 125, y)
			mfm.move(ui.buttonPreferences, w-270, y)
			mfm.move(ui.toggWrap, w-225, y)
			mfm.move(ui.buttonClear, w-150, y)
			mfm.move(ui.buttonExit, w-95, y)
			return True

	def appWrap(ui, widget):
		ui.logView.set_wrap_mode((gtk.WRAP_NONE, gtk.WRAP_WORD)[widget.get_active()])

	def restoreGeometry(ui):
		if hasattr(ui, 'dlgs') and(ui.cfg['dlgPrefPos']):
			ui.dlgs.dlgPrefPos =  tuple(map(lambda k: int(k), ui.cfg['dlgPrefPos'].split(',')))
		ui.rGeo(ui.mainWindow, 'MainWindowGeometry')

	def storeGeometry(ui):
		if hasattr(ui, 'dlgs'):
			dlgs = ui.dlgs
			dlgs.hideDlgPref()
			if dlgs.dlgPrefPos:
				ui.cfg['dlgPrefPos'] = "%i,%i" % dlgs.dlgPrefPos
		ui.cfg['MainWindowGeometry'] = ui.sGeo(ui.mainWindow)

# Entry point
if __name__ == "__main__":
	mySinker_UI()
