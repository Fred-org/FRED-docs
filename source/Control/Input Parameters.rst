Input Parameters
=================================

The input consists of an ASCII file containing the parameters and the directives needed to define and control a simulation.
The default input file is **fred.inp** and is automatically read. Any file extension can be used (txt, ascii, etc), however, it is recommended to use **.inp** extension for all the input files.
If you want to use a different name, you supply the path to the input file using the command line option::

    fred -f path/to/my/inputfile


Input structure
------------------------------------------------------

The order of input lines is usually not important, with the exception of directives parsed by the delivery manager.
It is possible to split an input file into many files with the directive:

.. code-block:: python

    include: path_to_file

All the files set in the **include** directives will be merged in the first stage of the simulation and the merged version will be saved in the **out/log/run.inp** file. The input parser will digest the whole buffer and mirror the interpreted structures into **out/log/parsed.inp**. You can check and correct input errors using those two files.

For instance we can put all definition of materials properties into a single **materials.inp** file and include the file in multiple simulations:

.. code-block:: python

    include: path_to_dir/materials.inp

Then we can group all region definitions into a **regions.inp** file, containing for instance the gantry structures and range shifters for a particular treatment room in a facility.

.. code-block:: python

    include: path_to_dir/regions.inp

Finally the patient-specific information, such as CT scans, field configuration and related pencil beam information can be stored into an **rtplan.inp** which is changing for each irradiation.

.. code-block:: python

    include: rtplan.inp

The included files can also contain other **include:** directives. The parser will make sure that any recursive or circular inclusion chains are not present.

An example of a more complex input structure for a three fields irradiation to be delivered into ROOM1 could look like this::

    fred.inp
        │
        ├── materials.inp
        │         |
        │         ├────mat1.inp
        │         |
        │         ├────mat2.inp
        │         |
        │         └────mat3.inp
        │
        ├── regions_ROOM1.inp
        │         |
        │         ├────gantry.inp
        │         |
        │         ├────range_shifters.inp
        │         |
        │         └────energy_degraders.inp
        │
        └── rtplan.inp
                  |
                  ├────deliver_field1.inp
                  |
                  ├────deliver_field2.inp
                  |
                  └────deliver_field3.inp


The input structure is merged into a single sequential file, which is saved to ``out/log/run.inp``. The input parser will digest the whole buffer and mirror the interpreted structures into ``out/log/parsed.inp``.



Input syntax
------------------------------------------------------

The input files are parsed by FRED using a free format text syntax. Efforts have been made in order to allow the most natural and easy way of writing the input files.

White spaces
````````````````````````````````````````````

In general, white spaces (spaces, tabs, etc.) are ignored and discarded. Exception is the definition of strings (names, paths, etc.) where white space is preserved.


Comments
````````````````````````````````````````````

Comments are parts of the input file that describe the intent and meaning of the setup. The commented text is ignored by FRED. Comments can be also used to quickly exclude parts of an input file without permanently delete them. Comments can be defined using the following single-line prefixes:

.. code-block:: none

    %  <= Matlab style (percent)
    #  <= gnuplot style (hash)
    // <= C++ style (double backslash)
    /  <= FRED style  (single backslash)

Whole multiline blocks can also be commented out using the C style:

.. code-block:: c

    /*
        ...
        ...
    */



Parameters
````````````````````````````````````````````
Parameters can be numeric values, strings or boolean flags.

- The numeric values are parsed as floating point numbers in general format. If the destination parameter is an integer, conversion from floating point to integer is done on the fly.
- The lists can be defined using the python-like syntax **[a,b,c,...]**.
- The string parameters can be given in quotes or without
- The boolean parameters can be given as **t**, **true**, **f** or **false**. The capitals are ignored.

Examples of parameters definition:

.. code-block:: python

    rho = 1.205e-3            # numeric parameter
    nprim = 1.23e4            # on-the-fly conversion (1.23e4 => 12300)
    lTracking_nuc = f         # boolean parameter
    CTscan = patientCT.mhd    # string parameter
    L = [20, 20, 40]          # list of parameters

Complex objects such as regions, fields or pencil beams can be defined using many parameters. The parameters can be grouped on a single line, or distributed for clarity over multiple lines. In general parameter definitions of an object can be separated by semicolons.

The single line definition consists of an object class delimited by a colon **:**. The instance of the class, i.e. the defined object, is identified by a string. Then the semicolon-separated list of parameters follows. Example how to define an object of field in a single line:

.. code-block:: python

    field: f1 ; O = [-50, 0, 0] ; f = [2, 2, 0] ; u = [1, -1, 0]

where:

- **f1** is the ID number or a string that uniquely identifies an instance of an object within the same class. It is used to establish relations between all objects in a particular setup.
- **O = [-50, 0, 0]** defines the origin of the source
- **f = [2, 2, 0]** defines the front vector of the source
- **u = [1, -1, 0]** defines the up vector of the source

The multi-line definition splits the declaration of an object into several lines. The directive starts with the class name followed by **<**, and ends with the same class name followed by **>**, in a similar fashion to html tags. In certain cases it is possible to nest multi-line definitions. The input parser will indicate the allowed or not allowed constructs. For instance, the field declaration above can be written in an equivalent multi-line style as follows:


.. code-block:: python

    field<
        ID = f1
        O = [-50, 0, 0]
        f = [2, 2, 0]
        u = [1, -1, 0]
    field>

Units
````````````````````````````````````````````
FRED is using predefined units for inputs and outputs. In input files FRED is using:

- All dimensional inputs, like region size definition, region translations, etc. are given in [cm].
- All angles, mostly for rotations, are given in [degrees].
- Mean ionisation potential is given in [eV].
- Energy in given in [MeV].
- Lateral beam parameters (point-like source, emittance) are given in [cm].
- All versors are unitless and are normalised internally.
- Density is given in [g/cm\ :sup:`3`].

FRED outputs the simulation results in units:

- Dose, including the RBE-weighted dose are saved in [Gy].
- Dose-averaged LET is saved in [MeV/cm].
- Density  is saved in [g/cm\ :sup:`3`].
- Deposited energy is saved in [MeV].

