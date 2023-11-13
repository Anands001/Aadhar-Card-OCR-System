#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pytesseract
import tesseract_ocr

start = time.time()
for i in xrange(100):
    tesseract_ocr.text_for_filename('tests/code.tiff')
print time.time() - start
