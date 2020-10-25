Control Options
=================================

There are many options, that can be used in an input file to control a simulation. In the list below, the default values are given.


Radiobiology
~~~~~~~~~~~~~~~~~~
By default, when an RBE model is activated, FRED writes only the corresponding biological dose map.
For instance, if McNamara RBE model for protons is activated (``lRBE_McNamara=t``), then FRED will save the bio dose in ``out/RBE/DoseBio_McNamara.mhd``. Other maps can be optionally requested for checking and/or post-processing FRED output. These maps are the local alpha and beta parameters, and the RBE computed by the requested model.

    ``lRBE_write_DoseBio = t``
        write biological dose

    ``lRBE_write_Alpha = f``
        write alpha parameter

    ``lRBE_write_Beta = f``
        write beta parameter

    ``lRBE_write_RBE = f``
        write RBE values


Verbosity
~~~~~~~~~~~~~~~~~~
The level of output verbosity can be controlled in many ways, e.g. using a command line option, or an environment variable, or setting it directly in the input file.

The levels are varying from 0 (=minimal) to 5 (=debugging).

The sequence that defines the verbosity level is the following:

#. the level is set to 3 (mid verbosity)
#. level is taken from FRED_VERBOSE env variable (if present)
#. level can then be finely tuned in input file using verbose: directives
#. cmdline option -V0…-V5 override any previous settings 

.. code-block:: python

	# quick and dirty
	verbose: 0

	# equivalent form
	verbose: all 0

	# incremental on multiple lines
	verbose: 0
	verbose: delivery 1
	verbose: geometry source 3

	# oneliner
	verbose: 0 delivery 1 geometry source 3

	# quick oneliner without changing the input file
	export FRED_VERBOSE='0 delivery 1 geometry source 3'


The `verbose:` directive can be used to set the verbosity level separately for each module.
The modules that can be controlled are: `physics, delivery, plugin, source, geometry, environment, input, materials, radiobiology`.

Example of detailed manipulation of verbosity level:

.. code-block:: none

	verbose: all 0
	verbose: physics 3
	verbose: delivery 2
	verbose: plugin 5
	verbose: source 1
	verbose: geometry 3
	verbose: environment 0
	verbose: input 4
	verbose: materials 2
	verbose: radiobiology 5


Other
~~~~~~~~~~~~~~~~~~

lplotray=f
allowOverlapping: gantry phantom
