#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

'© Copyrighrt 2015 by LordBlick (at) gmail.com'

import gtk, pango

Height = 30

def getTxtPixelWidth(widget, txt, fontDesc=None):
	pangoLayout = widget.create_pango_layout(txt)
	if fontDesc:
		pangoLayout.set_font_description(fontDesc)
	pangoTxtSpc = pangoLayout.get_pixel_size()[0]
	del(pangoLayout)
	return pangoTxtSpc

def putScroll(hFixed, widget, posX, posY, width, height):
	hScroll = gtk.ScrolledWindow()
	hScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	hScroll.add(widget)
	hScroll.set_size_request(width, height)
	hFixed.put(hScroll, posX, posY)
	return hScroll

def e_clr_text(entry, icoPos, sigEvent):
	if icoPos == gtk.ENTRY_ICON_SECONDARY:
		entry.set_text('')
		entry.grab_focus()

class MvWg:
	"This is abctract class !"
	def __init__(it, *args):
		raise TypeError('MvWg.__init__(): abstract class')

	def move(it, x, y):
		it.hFixed.move(it, x, y)

	size = lambda it, w, h: it.set_size_request(w, h)

class Label(gtk.Label, MvWg):
	__gtype_name__ = 'Label'
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None, xalign=None, selectable=False):
		it.hFixed = hFixed
		super(it.__class__, it).__init__(txtLabel) # gtk.Label
		if fontDesc:
			it.modify_font(fontDesc)
		if type(xalign)==float and(0.<=xalign<=1.):
			yalign = it.get_alignment()[1]
			it.set_alignment(xalign, yalign)
		if type(selectable)==bool:
			it.set_selectable(selectable)
			it.set_can_focus(False)
		it.show()
		if not height:
			height=Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Image(gtk.Image, MvWg):
	__gtype_name__ = 'Image'
	def __init__(it, hFixed, posX, posY, pix=None):
		it.hFixed = hFixed
		super(it.__class__, it).__init__() # gtk.Label
		if isinstance(pix, gtk.gdk.Pixbuf):
			it.set_from_pixbuf(pix)
		hFixed.put(it, posX, posY)

class Butt(gtk.Button, MvWg):
	"""If stockID is set, txtLabel set as True means full stock button,
	non-null string - own Label for stock image,
	in other case - button with only stock image"""
	__gtype_name__ = 'Butt'
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=0, fileImage=None, stockID=None, fontDesc=None):
		it.hFixed = hFixed
		if stockID == None and fileImage == None:
			super(it.__class__, it).__init__(label=txtLabel, use_underline=False)
			if fontDesc:
				btLabel = it.child
				btLabel.modify_font(fontDesc)
		else:
			if type(txtLabel)==int or type(txtLabel)==float or type(txtLabel)==type(None) or (type(txtLabel)==str and txtLabel==''):
				txtLabel = bool(txtLabel)
			if type(txtLabel)==bool and txtLabel==True or type(txtLabel)==str:
				if stockID:
					super(it.__class__, it).__init__(stock=stockID)
				elif fileImage:
					image = gtk.Image()
					image.set_from_file(fileImage)
					super(it.__class__, it).__init__()
					it.add(image)
				if type(txtLabel)==str:
					btLabel = it.get_children()[0].get_children()[0].get_children()[1]
					btLabel.set_text(txtLabel)
					if fontDesc:
						btLabel.modify_font(fontDesc)
			else:
				image = gtk.Image()
				if stockID:
					image.set_from_stock(stockID, gtk.ICON_SIZE_BUTTON)
				elif fileImage:
					image.set_from_file(fileImage)
				super(it.__class__, it).__init__()
				it.add(image)
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Toggle(gtk.ToggleButton, MvWg):
	__gtype_name__ = 'Toggle'
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=0, fontDesc=None):
		super(it.__class__, it).__init__(label=txtLabel, use_underline=False)
		if fontDesc:
			it.child.modify_font(fontDesc)
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Check(gtk.CheckButton, MvWg):
	__gtype_name__ = 'Check'
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=0, fontDesc=None):
		it.hFixed = hFixed
		super(it.__class__, it).__init__(label=txtLabel, use_underline=False)
		if fontDesc:
			it.child.modify_font(fontDesc)
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class ComboBox(gtk.ComboBox):
	__gtype_name__ = 'ComboBox'
	def __init__(it, modelCb, hFixed, posX, posY, width, height=0, fontDesc=None, wrap=None, selTxt=0):
		it.hFixed = hFixed
		super(it.__class__, it).__init__()
		cellRendr = gtk.CellRendererText()
		if fontDesc:
			cellRendr.set_property('font-desc', fontDesc)
		it.pack_start(cellRendr)
		it.set_attributes(cellRendr, text=selTxt)
		if wrap:
			it.set_wrap_width(wrap)
		else:
			cellRendr.set_property('ellipsize', pango.ELLIPSIZE_END)
		it.set_model(modelCb)
		if not height:
			height=Height+4
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY-2)

	move = lambda it, x, y: it.hFixed.move(it, x, y-2)

class Entry(gtk.Entry, MvWg):
	__gtype_name__ = 'Entry'
	def __init__(it, hFixed, posX, posY, width, height=0, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
		def entryIcoClr(ed, icoPos, sigEvent):
			if icoPos == gtk.ENTRY_ICON_SECONDARY:
				ed.set_text('')
		it.hFixed = hFixed
		super(it.__class__, it).__init__()
		if fontDesc:
			it.modify_font(fontDesc)
		if startIco:
			textInput.set_icon_from_pixbuf(0, startIco)
		if clearIco:
			it.set_icon_from_stock(1, gtk.STOCK_CLOSE)
			it.set_icon_tooltip_text (1, 'Clear')
			it.connect("icon-release", entryIcoClr)
		it.set_property("editable", bool(bEditable))
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Num(gtk.SpinButton, MvWg):
	__gtype_name__ = 'Num'
	def __init__(it, numTup, hFixed, posX, posY, width, height=0, partDigits=0, fontDesc=None):
		it.hFixed = hFixed
		numInit, numMin, numMax, numStep = numTup
		hAdj =  gtk.Adjustment(value=numInit, lower=numMin, upper=numMax, step_incr=numStep,
			page_incr=0, page_size=0)
		super(it.__class__, it).__init__(hAdj, 0, partDigits)
		it.set_numeric(True)
		it.set_update_policy(gtk.UPDATE_IF_VALID)
		if fontDesc:
			it.modify_font(fontDesc)
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class MvScrolled:
	"This is abctract class !"
	def reScrollV(it, adjV, scrollV):
		'Scroll to the bottom of the TextView when the adjustment changes.'
		if it.autoscroll:
			adjV.set_value(adjV.upper - adjV.page_size)
			scrollV.set_vadjustment(adjV)
		return

	def setup_scroll(it, x, y, w, h):
		scrollViewport = gtk.ScrolledWindow()
		vadj = scrollViewport.get_vadjustment()
		vadj.connect('changed', it.reScrollV, scrollViewport)
		scrollViewport.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrollViewport.add(it)
		scrollViewport.set_size_request(w, h)
		it.hFixed.put(scrollViewport, x, y)

	def size(it, x, y):
		try:
			parent = it.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			parent.set_size_request(x, y)
		else:
			super(it.__class__, it).set_size_request(x, y)

	def move(it, x, y):
		try:
			parent = it.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			it.hFixed.move(parent, x, y)
		else:
			it.hFixed.move(it, x, y)

from gobject import TYPE_NONE as goNon, TYPE_INT as goInt, TYPE_STRING as goStr,\
	SIGNAL_RUN_LAST as sigRunLast, PARAM_READWRITE as parRW
class CellRendererClickablePixbuf(gtk.CellRendererPixbuf):
	__gsignals__ = {
		'clicked': (sigRunLast, goNon, (goStr,))
		}
	def __init__(pixCR):
		super(CellRendererClickablePixbuf, pixCR).__init__()
		pixCR.set_property('mode', gtk.CELL_RENDERER_MODE_ACTIVATABLE)
	def do_activate(pixCR, event, widget, path, background_area, cell_area, flags):
		pixCR.emit('clicked', path)

class CellRendererPixbufXt(gtk.CellRendererPixbuf):
	"""docstring for CellRendererPixbufXt"""
	__gproperties__ = { 'active-state' :
						(goStr, 'pixmap/active widget state',
						'stock-icon name representing active widget state',
						None, parRW) }
	__gsignals__    = { 'clicked' :
						(sigRunLast, goNon, (goInt,)) , }
	#states = [ None, gtk.STOCK_APPLY, gtk.STOCK_CANCEL ]
	def __init__( it ):
		gtk.CellRendererPixbuf.__init__( it )

	def do_get_property( it, property ):
		"""docstring for do_get_property"""
		if property.name == 'active-state':
			return it.active_state
		else:
			raise AttributeError, 'unknown property %s' % property.name

	def do_set_property( it, property, value ):
		if property.name == 'active-state':
			it.active_state = value
		else: 
			raise AttributeError, 'unknown property %s' % property.name

	def do_activate( it, event, widget, path,  background_area, cell_area, flags ):
		print( "do_activate" )
		if event.type == gtk.gdk.BUTTON_PRESS:
			it.emit('clicked')

class CellRendererDate(gtk.CellRendererText):
	__gtype_name__ = 'CellRendererDate'
	def __init__(it):
		gtk.CellRendererText.__init__(it)
		it.date_format = '%d/%m/%Y'
		it.calendar_window = None
		it.calendar = None

	def _create_calendar(it, treeview):
		it.calendar_window = gtk.Dialog(parent=treeview.get_toplevel())
		it.calendar_window.action_area.hide()
		it.calendar_window.set_decorated(False)
		it.calendar_window.set_property('skip-taskbar-hint', True)

		it.calendar = gtk.Calendar()
		it.calendar.display_options(gtk.CALENDAR_SHOW_DAY_NAMES | gtk.CALENDAR_SHOW_HEADING)
		it.calendar.connect('day-selected-double-click', it._day_selected, None)
		it.calendar.connect('key-press-event', it._day_selected)
		it.calendar.connect('focus-out-event', it._selection_cancelled)
		it.calendar_window.set_transient_for(None) # cancel the modality of dialog
		it.calendar_window.vbox.pack_start(it.calendar)

		# necessary for getting the (width, height) of calendar_window
		it.calendar.show()
		it.calendar_window.realize()

	def do_start_editing(it, event, treeview, path, background_area, cell_area, flags):
		if not it.get_property('editable'):
			return
		if not it.calendar_window:
			it._create_calendar(treeview)
		# select cell's previously stored date if any exists - or today
		if it.get_property('text'):
			date = datetime.datetime.strptime(it.get_property('text'), it.date_format)
		else:
			date = datetime.datetime.today()
			it.calendar.freeze() # prevent flicker
			(year, month, day) = (date.year, date.month - 1, date.day) # datetime's month starts from one
			it.calendar.select_month(int(month), int(year))
			it.calendar.select_day(int(day))
			it.calendar.thaw()
			# position the popup below the edited cell (and try hard to keep the popup within the toplevel window)
			(tree_x, tree_y) = treeview.get_bin_window().get_origin()
			(tree_w, tree_h) = treeview.window.get_geometry()[2:4]
			(calendar_w, calendar_h) = it.calendar_window.window.get_geometry()[2:4]
			x = tree_x + min(cell_area.x, tree_w - calendar_w + treeview.get_visible_rect().x)
			y = tree_y + min(cell_area.y, tree_h - calendar_h + treeview.get_visible_rect().y)
			it.calendar_window.move(x, y)
			response = it.calendar_window.run()
			if response == gtk.RESPONSE_OK:
				(year, month, day) = it.calendar.get_date()
				date = datetime.date(year, month + 1, day).strftime (it.date_format) # gtk.Calendar's month starts from zero
				it.emit('edited', path, date)
				it.calendar_window.hide()
			return None # don't return any editable, our gtk.Dialog did the work already

	def _day_selected(it, calendar, event):
		# event == None for day selected via doubleclick
		if not(event) or(event.type==gtk.gdk.KEY_PRESS) and(gtk.gdk.keyval_name(event.keyval)=='Return'):
			it.calendar_window.response(gtk.RESPONSE_OK)
			return True

	def _selection_cancelled(it, calendar, event):
		it.calendar_window.response(gtk.RESPONSE_CANCEL)
		return True
 
def TreeColumn(txtLabel, colWidth, tCol, dcRendProp, fontDesc=None):
	if txtLabel and not fontDesc:
		tvc = gtk.TreeViewColumn(txtLabel)
	else:
		tvc = gtk.TreeViewColumn()
	tvc.set_alignment(0.5) # Headers Center
	if colWidth:
		tvc.set_min_width(colWidth)
		tvc.set_max_width(colWidth)
	if fontDesc:
		ttcLabel = it.npLabel(txtLabel, fontDesc=fontDesc)
		tvc.set_widget(ttcLabel)
	lsCR = []
	for n in tCol:
		if n[0]=='txt':
			cellRendr = gtk.CellRendererText()
			if fontDesc:
				cellRendr.set_property('font-desc', fontDesc)
			if dcRendProp.has_key('txt'):
				for Prop in dcRendProp['txt']:
					cellRendr.set_property(*Prop)
			tvc.pack_start(cellRendr, True)
			if n[1]!=None:
				if callable(n[1]):
					if len(n)>2:
						tvc.set_cell_data_func(cellRendr, n[1], n[2:])
				elif type(n[1])==int:
					tvc.set_attributes(cellRendr, text=n[1])
		elif n[0] in('pix', 'xpix', 'cpix'):
			cellRendr = {
				'pix':gtk.CellRendererPixbuf,
				'cpix':CellRendererClickablePixbuf,
				'xpix':CellRendererPixbufXt
				}[n[0]]()
			if dcRendProp.has_key(n[0]):
				for Prop in dcRendProp[n[0]]:
					cellRendr.set_property(*Prop)
			tvc.pack_start(cellRendr, True)
			if n[1]!=None:
				if callable(n[1]):
					if len(n)>2:
						tvc.set_cell_data_func(cellRendr, *n[1:])
					else:
						tvc.set_cell_data_func(cellRendr, n[1])
				elif type(n[1])==int:
					tvc.set_attributes(cellRendr, pixbuf=n[1])
				elif type(n[1])==gtk.gdk.Pixbuf:
					tvc.set_attributes(cellRendr, pixbuf=n[1])
		elif n[0]=='togg':
			cellRendr = gtk.CellRendererToggle()
			if dcRendProp.has_key('togg'):
				for Prop in dcRendProp['togg']:
					cellRendr.set_property(*Prop)
			tvc.pack_start(cellRendr, True)
			tvc.set_attributes(cellRendr, active=n[1])
		elif n[0]=='combo':
			cellRendr = gtk.CellRendererCombo()
			if dcRendProp.has_key('combo'):
				for Prop in dcRendProp['combo']:
					cellRendr.set_property(*Prop)
			tvc.pack_start(cellRendr, True)
			if n[1]!=None:
				tvc.set_attributes(cellRendr, text=n[1], model=n[2])
			if len(n)>3:
				tvc.set_attributes(cellRendr, editable=n[3])
		lsCR.append(cellRendr)
	return tvc, lsCR

def TreeTxtColumn(txtLabel, colWidth, nCol, lsRendProp, fontDesc=None):
	if txtLabel and not fontDesc:
		tvc = gtk.TreeViewColumn(txtLabel)
	else:
		tvc = gtk.TreeViewColumn()
	tvc.set_alignment(0.5) # Headers Center
	if colWidth:
		tvc.set_fixed_width(colWidth)
	if fontDesc:
		ttcLabel = gtk.Label(txtLabel)
		ttcLabel.modify_font(fontDesc)
		tvc.set_widget(ttcLabel)
	lscrtxt = []
	for n in nCol:
		crtxt = gtk.CellRendererText()
		if fontDesc:
			crtxt.set_property('font-desc', fontDesc)
		for Prop in lsRendProp:
			crtxt.set_property(*Prop)
		tvc.pack_start(crtxt, True)
		if type(n) in(int, str):
			tvc.set_attributes(crtxt, text=n)
		elif type(n)==tuple:
			if n[0]!=None and(callable(n[0])) and(len(n)>1):
				tvc.set_cell_data_func(crtxt, n[0], n[1:])
		lscrtxt.append(crtxt)
	return tvc, lscrtxt

class TreeView(gtk.TreeView, MvScrolled):
	__gtype_name__ = 'TreeView'
	def __init__(it, model, hFixed, posX=0, posY=0, width=0, height=0):
		super(it.__class__, it).__init__(model)
		it.hFixed = hFixed
		it.autoscroll = True
		it.setup_scroll(posX, posY, width, height)

class TextView(gtk.TextView, MvScrolled):
	__gtype_name__ = 'TextView'
	def __init__(it, hFixed, posX=0, posY=0, width=0, height=0, wrap=False, bEditable=True, tabSpace=2, fontDesc=None):
		super(it.__class__, it).__init__()
		it.hFixed = hFixed
		it.autoscroll = True
		it.changed = False
		it.set_property("editable", bEditable)
		if fontDesc:
			it.modify_font(fontDesc)
			it.setTabSpace(tabSpace, fontDesc=fontDesc)
		it.setup_scroll(posX, posY, width, height)
		if wrap is True:
			it.set_wrap_mode(gtk.WRAP_WORD)
		elif wrap in(gtk.WRAP_NONE, gtk.WRAP_CHAR, gtk.WRAP_WORD):
			it.set_wrap_mode(wrap)

	def set_text(it, txt):
		it.get_buffer().set_text(txt)
		it.changed = True

	clear_text = lambda it: it.set_text('')

	def get_text(it):
		tBuff = it.get_buffer()
		return tBuff.get_text(tBuff.get_start_iter(), tBuff.get_end_iter())
	
	def insert_end(it, txt, tag=None):
		buff = it.get_buffer()
		end = buff.get_end_iter()
		text = txt.encode('utf-8', errors='replace')
		if isinstance(tag, basestring) and(hasattr(it, tag)):
			#print("Found tag %s" % tag)
			buff.insert_with_tags(end, text, getattr(it, tag))
		elif isinstance(tag, gtk.TextTag):
			#print("Found raw tag %s" % str(type(tag)))
			buff.insert_with_tags(end, text, tag)
		else:
			buff.insert(end, text)
		del(end)
		it.changed = True

	def setTabSpace(it, spaces, fontDesc=None):
		pangoTabSpc = getTxtPixelWidth(it, ' '*spaces, fontDesc)
		tabArray =  pango.TabArray(1, True)
		tabArray.set_tab(0, pango.TAB_LEFT, pangoTabSpc)
		it.set_tabs(tabArray)
		return pangoTabSpc

def dialogChooseFile(parent=None, startDir=None, startFile=None, filters=None, title='Select a file...', act='file_open', bShowHidden=False):
	action = {
		'file_open': gtk.FILE_CHOOSER_ACTION_OPEN,
		'file_save': gtk.FILE_CHOOSER_ACTION_SAVE,
		'dir_open': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
		'dir_create': gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
		}[act]
	hDialog = gtk.FileChooserDialog(title=title, parent=parent, action=action,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
	if filters:
		for fnFilter in filters:
			hDialog.add_filter(fnFilter)
		allFilter = gtk.FileFilter()
		allFilter.set_name("All files (*.*)")
		allFilter.add_pattern("*")
		hDialog.add_filter(allFilter)
	hDialog.set_default_response(gtk.RESPONSE_OK)
	hDialog.set_show_hidden(bShowHidden)
	if startDir:
		hDialog.set_current_folder(startDir)
	if startFile:
		if act=='file_save':
			hDialog.set_current_name(startFile)
		elif act=='file_open':
			hDialog.set_filename(startFile)
	respFileName = hDialog.run()
	fileName = None
	if respFileName==gtk.RESPONSE_OK:
		fileName = hDialog.get_filename()
	hDialog.destroy()
	return fileName

'''
rex move replace:
	from:
		{fixed}\.move\((ui\.\w+)\s*,\s+
	to:
		\1.move(
'''
