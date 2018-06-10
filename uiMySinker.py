#!/usr/bin/python2
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

from wgts import gtk, pango
import wgts as wg
lsFiles = 'Prev In Out'.split()
LO_ROWS = len(lsFiles)+1
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
				#if tatr.startswith("tg"):
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
		#ui.dcSize = {}
		ui.lw = 0
		for select in lsFiles:
			txtLabel = "%s File:" % select
			lb = wg.Label(txtLabel, mfm, 0, 0, 60)
			lw = getTxtPixelWidth(lb, txtLabel, fontDesc=ui.fontDesc)+5
			ui.lw = max(ui.lw, lw)
			lb.set_size_request(lw-2, wg.Height)
			setattr(ui, 'labFilename' + select, lb)
			#ui.dcSize[select] = lw
			if __name__ == "__main__":
				print(u"Label „%s” size: %d" % (txtLabel, lw))
				dsplFilename = wg.Butt(ui.txtFN, mfm, 0, 0, 0)
			else:
				dsplFilename = wg.Label(ui.txtFN,
					mfm, 0, 0, 0, xalign=0., selectable=True)
			setattr(ui, 'dsplFilename' + select, dsplFilename)
			bt = wg.Butt(None, mfm, 0, 0, 30, stockID=gtk.STOCK_OPEN) #"Set FileName..."
			setattr(ui, 'buttonFileName' + select, bt)


		ui.buttonConvert = wg.Butt(None, mfm, 0, 0, 30, stockID=gtk.STOCK_CONVERT) #"Proceed..."
		ui.buttonDiff = wg.Butt("Diff", mfm, 0,  0, 50)

		ui.chkDbg = wg.Check("Debug", mfm, 0,  0, 50)

		ui.toggWrap = wg.Toggle("Wrap words", mfm, 0,  0, 70)

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
				#lw = ui.dcSize[select]
				labFilename = getattr(ui, 'labFilename' + select)
				mfm.move(labFilename, 0, y)
				dsplFilename = getattr(ui, 'dsplFilename' + select)
				dsplFilename.size(w-50-lw, wgH)
				mfm.move(dsplFilename, lw, y)
				bt = getattr(ui, 'buttonFileName' + select)
				mfm.move(bt, w-45, y)
				y += wg.Height+5
			mfm.move(ui.buttonConvert, 0, y)
			mfm.move(ui.buttonDiff, 25, y)
			mfm.move(ui.chkDbg, 80, y)
			mfm.move(ui.toggWrap, w-225, y)
			mfm.move(ui.buttonClear, w-150, y)
			mfm.move(ui.buttonExit, w-95, y)
			return True

	def appWrap(ui, widget):
		ui.logView.set_wrap_mode((gtk.WRAP_NONE, gtk.WRAP_WORD)[widget.get_active()])

	def restoreGeometry(ui):
		if hasattr(ui, 'stv') and(ui.cfg['dlgSrchPos']):
			ui.stv.dlgSrchPos =  tuple(map(lambda k: int(k), ui.cfg['dlgSrchPos'].split(',')))
		ui.rGeo(ui.mainWindow, 'MainWindowGeometry')

	def storeGeometry(ui):
		if hasattr(ui, 'stv'):
			stv = ui.stv
			stv.hideDlgSrch()
			if stv.dlgSrchPos:
				ui.cfg['dlgSrchPos'] = "%i,%i" % stv.dlgSrchPos
		ui.cfg['MainWindowGeometry'] = ui.sGeo(ui.mainWindow)

# Entry point
if __name__ == "__main__":
	mySinker_UI()
