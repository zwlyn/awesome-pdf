pyfpdf: FPDF for Python
=======================

This is a fork of the PyFPDF library and fixes unicode issues. It allows usage
of non-latin-1 characters (e.g. Euro sign €) in Python 3. This is possible
by internally using a bytearray output buffer instead of a string (and should
also be more efficient). This library is used by
`reportbro-lib <https://github.com/jobsta/reportbro-lib>`_
(see also `ReportBro <https://www.reportbro.com/>`_).

PyFPDF is a library for PDF document generation under Python, ported from PHP
(see `FPDF <http://www.fpdf.org/>`_: "Free"-PDF, a well-known
PDFlib-extension replacement with many examples, scripts and
derivatives).

Compared with other PDF libraries, PyFPDF is simple, small and versatile, with
advanced capabilities, and is easy to learn, extend and maintain.

Features:
---------

 - Python 2.7 and 3.5+ support
 - Unicode (UTF-8) TrueType font subset embedding
 - Barcode I2of5 and code39, QR code coming soon ...
 - PNG, GIF and JPG support (including transparency and alpha channel)
 - Templates with a visual designer & basic html2pdf
 - Exceptions support, other minor fixes, improvements and PEP8 code cleanups

Installation Instructions:
--------------------------

You can install PyFPDF from PyPI, with easyinstall or from Windows
installers. For example, using pip:

.. code:: shell

   pip install reportbro-fpdf

To get the latest development version you can download the source code running:

.. code:: shell

   git clone https://github.com/jobsta/pyfpdf.git
   cd pyfpdf
   python setup.py install


