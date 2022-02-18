#/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

from zipfile import ZipFile as zf
from os import path as ph

def ztree(zip_fn):
	lsFiles = []
	if not(ph.isfile(zip_fn)):
		return []
	with zf(zip_fn, "r") as hZip:
		lsFiles = [files.filename for files in hZip.filelist]
		hZip.close()
	return lsFiles

def zunp(zip_fn, in_zip_fn, out_fn):
	with zf(zip_fn, "r") as hZip:
		h_unz = hZip.open(in_zip_fn)
		h_st = open(out_fn, 'wb')
		h_st.write(h_unz.read())
		h_st.close()
		h_unz.close()
		hZip.close()
