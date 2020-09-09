Command Line Options
=================================

General options
---------------

.. index::  ! option -h

-h
~~~~~~~~~~~~~~~

    Print minimal help.

    .. code-block:: bash

        $ fred -h


.. index::  ! option -v

-v
~~~~~~~~~~~~~~~

    Print version.

    .. code-block:: bash

        $ fred -v
        fred Version 3.0  (028d8d2c3da) - 2019/10/01

.. index::  ! option -f


-f path
~~~~~~~~~~~~~~~

    use path as main input file instead of default ``fred.inp``

    .. code-block:: bash

        fred -f waterphantom.f


.. index::  ! option -i

-i path
~~~~~~~~~~~~~~~

    Use path as input directory instead of the current working directory.

    .. code-block:: bash

        $ fred -i myInputDir


.. index::  ! option -o

-o path
~~~~~~~~~~~~~~~

    Use path as output directory instead of default **out**.

    .. code-block:: bash

        $ fred -o myOutputDir


.. index::  ! option -benchmark

-benchmark N
~~~~~~~~~~~~~~~

    Run the standard benchmark for **N** primary particles

    .. code-block:: bash

        $ fred -benchmark 1E5


.. index::  ! option -performance

-performance
~~~~~~~~~~~~~~~

    Run the system performance scan both for CPU and GPU.

.. index::  ! option -gpusetup

-gpusetup
~~~~~~~~~~~~~~~

      Run the GPU resource locator.


.. index::  ! option -manage

-manage
~~~~~~~~~~~~~~~

      Manage FRED installed versions: change, delete, move, etc. For system-wide installations it will require root privileges.


.. index::  ! option -listVers

-listVers
~~~~~~~~~~~~~~~

      List available FRED versions installed on the system.


.. index::  ! option -useVers

-useVers fredVersion
~~~~~~~~~~~~~~~

      Switch to **fredVersion** version temporary (only for current simulation).

    .. code-block:: bash

        $ fred -useVers fred_3.0.18


.. index::  ! option -colorOutput

-colorOutput | -C
~~~~~~~~~~~~~~~

      Activate color output for ANSI compatible terminals.






Simulation control
---------------------

.. index::  ! option -n

-n
~~~~~~~~~~~~~~~

    Run simulation in a dry run. No particles will be generated or tracked.


.. index::  ! option -nprim

-nprim N
~~~~~~~~~~~~~~~

    Set number of primary particles per pencil beam. This command overrides any other **nprim** definition in the input files.

    .. code-block:: bash

        $ fred -nprim 1e5


.. index::  ! option -nrep

-nrep N
~~~~~~~~~~~~~~~

    Repeat the simulation **N** times. Every time a statistically independent run is performed, so you can afterwards evaluate the statistical fluctuations in the simulated maps.

    .. code-block:: bash

        $ fred -nrep 5

    .. warning:: In order to have different runs, the **randSeedRoot** must not be defined in the input files or set to 0. In this way the random seed is taken from a high resolution generator connected to the system clock.


    .. tip::
        After 5 repetitions, the simulation folder will look like shown below, with **out** folders for each repetition.

        .. code-block:: bash

            fred.inp
            out000/
            out001/
            out002/
            out003/
            out004/

    .. tip::
        This option can be used in combination with **-o** option to obtain a numbered sequence of output directories. For instance, the command:

        .. code-block:: bash

            $ fred -nrep 4 -o mytest

        will produce:

        .. code-block:: bash

            fred.inp
            mytest000/
            mytest001/
            mytest002/
            mytest003/



.. index::  ! option -repbeg

-repbeg N
~~~~~~~~~~~~~~~
    Index of the first repetition. For instance, to run 4 repetitions starting from index 15:

    .. code-block:: bash

        $ fred -nrep 4 -repbeg 15

    and we get:

    .. code-block:: bash

        fred.inp
        ...
        out015/
        out016/
        out017/
        out018/

.. index::  ! option -rseed

-rseed N
~~~~~~~~~~~~~~~
    Initialize the seed of the random generator. **N** must be a 64-bit unsigned integer (*uint64*). This overrides any other **randSeedRoot** definition in the input files.

    .. code-block:: bash

        $ fred -rseed 4637646287



Execution control
-----------------

.. index::  ! option -serial

-serial
~~~~~~~~~~~~~~~
    Single thread execution on a CPU (sequential non-parallel execution). This is a shortcut for **-numThreads 1** (see below).


.. index::  ! option -nogpu

-nogpu
~~~~~~~~~~~~~~~
    Do not use GPU, if present: run on CPU only.


.. index::  ! option -gpuonly

-gpuonly
~~~~~~~~~~~~~~~
    Require GPU execution. This will fail if no GPU is available.


.. index::  ! option -numThreads

-numThreads N
~~~~~~~~~~~~~
    Run with **N** parallel threads at the CPU level. For instance, if you want to run with 32 threads on the CPU without using any GPU, run:

    .. code-block:: bash

        $ fred -numThreads 32 -nogpu


.. index::  ! option -nspawn

-nspawn N
~~~~~~~~~

    Launch **N** independent copies of the simulation. It is meant to be used in combination with option **-nrep**, to accelerate repetitions by running them in parallel. This is especially needed when running with a plugin that demands for serial execution.

    .. warning:: Use this option with care. It can easily bring a workstation to its knees by using all computing resources, memory and disk space.

    .. tip::
        For instance, if you want to run 1000 repetitions in serial mode (1 thread per simulation) using 10 cores at the same time, you can use:

        .. code-block:: bash

            $ fred -nrep 1000 -serial -nspawn 10


Plugin control
--------------

.. index::  ! option -noplugin

-noplugin
~~~~~~~~~
    Do not load and use any plugin.


.. index::  ! option -pluginonly

-pluginonly
~~~~~~~~~~~
    Run only if at least a plugin is found and loaded.


.. index::  ! option -plugindir

-plugindir path
~~~~~~~~~~~~~~~

    Use path as starting directory to search for plugins.


.. index::  ! option -install-plugin

-install-plugin
~~~~~~~~~~~~~~~

    Create a plugin directory from the built-in template.


    .. code-block:: bash

        $ fred -install-plugin


.. index::  ! option -update-plugin

-update-plugin
~~~~~~~~~~~~~~~

    Make sure that plugin interface library is aligned with current version of FRED executable.

    .. code-block:: bash

        $ fred -update-plugin
