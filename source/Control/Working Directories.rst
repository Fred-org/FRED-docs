Working Directories
=================================

Typical working directory layout for a FRED simulation::

./fred.inp
./inp/
./plugin/
./out/

fred.inp file
    An input file is always needed. The default name is *fred.inp*.

inp folder
    An optional directory *inp* can be present containing auxiliary files (e.g. DICOM files, user-defined HU calibration curves, treatment plan files, etc.).

out folder
    The *out* directory is populated by output files and results produced by FRED.

    .. Caution:: This directory is completely erased each time a simulation is run.

plugin fonder
    A *plugin* directory can contain user-written code in the form of a dynamically loaded pluginx that expand the capability of FRED code.
