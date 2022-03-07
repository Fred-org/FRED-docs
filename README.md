# FRED-docs

The FRED documentation is written in reStructuredText format and can be found at [fred-mc.org](http://www.fred-mc.org).

The documentation is build with sphinx in version 4.0.2 using sphinx_rtd_theme template in version 0.5.2.

To install the newest version of sphinx:

    pip3 install -U sphinx

To install the RTD template:

    pip3 install sphinx-rtd-theme

To build the documentation execute:

    make clean
    make html

and open the file `build/html/index.html` in you web browser.
