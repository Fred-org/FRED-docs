.. _Installation:

Installation
=================================

Once you have a self-extracting compressed archive of FRED distribution, namely fred_3.*.*.run, make it executable:

.. code-block:: bash

    $ chmod +x fred_3.*.*.run

and run the installer:

.. code-block:: bash

    $ sh fred_3.*.*.run

and follow the instructions. You can install FRED wherever you like on your system. Typical options are:

- single-user: everything is installed in the user file tree below the $HOME folder
- server-wide: the distribution will be installed on the server so that all users can see and use the same version of FRED. You need admin privileges to run this installation.

You can always go back to the script that manages the installed distributions present on your system using:

.. code-block:: bash

    $ fred -manage

Python environment
------------------------------------------------------
FRED needs an elementary Python installation for running, namely Python >=3.0 is required. Check your current version with:

.. code-block:: bash

    $ python -v

If you want to use the Python scripts that come with FRED distribution for quick visualization and post-processing of 3D maps, you have to install the *numpy* and *matplotlib* packages.

Environment variables
------------------------------------------------------
In Unix-like operating systems (e.g. Linux or MacOSX), setup customization is achieved via environment variables. These variables are usually contained in a resource file. The FRED resource file is hidden in the user home folder *.fredrc*, which can be edited to change or fine-tune the installation manually.


In Windows, the same functionality is achieved using the System Registry. The environment variables are stored as subkeys of the key ``HKEY_LOCAL_MACHINE\SOFTWARE\Fred-MC\fred``. These values can be visualized and changed using, for instance, the **Registry Editor** application.

.. note::
    You could edit environment variables also using a simple GUI:

    .. code-block:: bash

        fred -config

    *New in version 3.60 : work in progress!*

Environment variables define a default setup, and command line options can overwrite their effect. Example of a typical *.fredrc* file:

.. code-block:: bash

    export FRED_GPU_AVAILABLE=1
    export FGE_CL_PLATFORM=0
    export FGE_CL_GPULIST=0,1
    export FRED_MAX_THREADS=12
    export FRED_SEARCHPATH=~/fred/myPlugins:/usr/local/shared/fredScripts
    export FRED_VERBOSE=0

Available options are:

.. index::  ! FRED_MAX_THREADS

FRED_MAX_THREADS = N
    Set the number of POSIX threads to be used for CPU execution. This is the typical number of threads used for particle tracking. Other parts of the code can use fewer threads to accomplish their tasks.

.. index::  ! FRED_GPU_AVAILABLE

FRED_GPU_AVAILABLE = 1|0
    - If 1, tell FRED that one or more GPUs are available for calculation.
    - If 0, no GPU available, or do not use any GPU, even if installed on the system.

.. index::  ! FGE_CL_PLATFORM

FGE_CL_PLATFORM = N
    Tell FRED GPU Engine (FGE) to use OpenCL platform N for GPU computation.

.. index::  ! FGE_CL_GPULIST

FGE_CL_GPULIST = dev0, dev1, …, devN
    Specify a list of GPU devices that can be used for computation

.. tip::
    On a system with 4 installed GPUs, use devices: 0, 1 and 3:

    .. code-block:: bash

        export FGE_CL_GPULIST=0,1,3

.. index::  ! FRED_SEARCHPATH

FRED_SEARCHPATH = dirList
    Specify a list of directories where files are looked for. A colon separates the paths as in the standard shell variable *$PATH*.

.. tip::
    Add to the search path a directory containing a series of plugins and a local repository of scripts:

    .. code-block:: bash

        export FRED_SEARCHPATH=~/myFredPlugins:/usr/local/shared/fredScripts

.. index::  ! FRED_VERBOSE

FRED_VERBOSE = {0..5} (def. 3)
    Specifies the global verbosity level, i.e. the amount of information displayed in the terminal and saved to a log file during a simulation.

.. tip::
    This can be overwritten in the input file:

    .. code-block:: bash

        verbose: all {0..5}

.. index::  ! FRED_ANSI_COLORS

FRED_ANSI_COLORS = t|true
    Tell FRED to pretty-color the output to the terminal. By default, coloring is off and can be turned on using this environment variable. The command line option `-C` can also be used on a run-by-run basis.

