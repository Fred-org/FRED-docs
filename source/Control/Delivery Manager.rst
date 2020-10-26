Delivery Manager
=================================

The delivery manager takes care of the steps corresponding to an irradiation plan. There are two main categories of operations: the geometry transformations and the delivery of particles. Each delivery step consists in a preparatory phase, where the geometry is transformed, followed by a series of delivery actions. The directives found in the input file are parsed in sequential order.

.. index::  ! Geometry transformation, transform:

Geometry transformation
-----------------------

These directives allow to move, shift, and rotate regions or groups of regions. By default, all transformations are performed with respect to the *global* (room) frame of reference. You can also specify a different frame of reference (FoR), so for instance you can rotate the phantom around itself, shift it sideways with respect to another region, etc. The general syntax for the **transform:** directive is:

.. code-block:: python

    transform: regionList action parameters [FoR]

where:

    - **regionList**: one or more regions or groups of regions to which the transformation is applied.
    - **action**: transformation operation.
    - **parameters**: definition of the transformation details.
    - **FoR** (optional): frame of reference for the transformation:

        - *global* or *room* : use the global FoR (default)
        - *local* or *self*  : use the FoR of each single region, i.e. transform each region with respect to itself
        - regionID : use the FoR of the indicated region


Available **actions** are:

- **shift_by**

    Shift the region by an offset vector [dx,dy,dz]. Syntax:

    .. code-block:: python

        transform: regionList shift_by dx dy dz [FoR]

    Examples:

    - shift the phantom by 5 cm along global *Z* direction

    .. code-block:: python

        transform: phantom shift_by 0 0 5

    - shift the phantom by 3 cm along its own left direction

    .. code-block:: python

        transform: phantom shift_by 3 0 0 self

    - shift the detector by vector [-1, 3, 7] cm with respect to phantom FoR

    .. code-block:: python

        transform: detector shift_by -1 3 7 phantom



- **move_to**

    Move the region origin to the position [x,y,z] with respect to global (or indicated) FoR. Syntax:

    .. code-block:: python

        transform: regionList move_to x y z [FoR]




- **rotate**

    Rotate the region by angle [degree] around the given axis with respect to global (or indicated) FoR. Syntax:

    .. code-block:: python

        transform: regionList rotate axis angle [FoR]


.. index::  ! Logical operations, group:, set_parent:, activate:, deactivate:

Logical operations
-------------------------------

It is possible to group several regions, so that operations can be applied to a group using a single directive. Regions or groups can be activated or deactivated at each step, determining which are actually present during a delivery phase.

- **group:**

    Defines a group with name *groupID* containing the regions in *regionList*. Syntax:

    .. code-block:: python

        group: groupID regionList

    Example:

    - group all Range Shifter plates into a block

    .. code-block:: python

        group: RSplateGroup Plate01 Plate02 Plate03 Plate04 Plate05


- **set_parent:**

    Region *motherRegionID* is containing the regions in *daughterRegionList*. Syntax:

    .. code-block:: python

        set_parent: motherRegionID daughterRegionList

    Example:

    - the gantry region contains the fields and the NozzleGroup

    .. code-block:: python

        set_parent: gantry fields NozzleGroup


- **activate:**

    Regions in *regionList* are actually present in the setup. Syntax:

    .. code-block:: python

        activate: regionList

    Example:

    - prepare the delivery of field 1 to the phantom with Range Shifter 1 inserted in the beam

    .. code-block:: python

        activate: field_1 RS1 phantom


- **deactivate:**

    Regions in *regionList* are not present in the setup. Syntax:

    .. code-block:: python

        deactivate: regionList

    Examples:

    - reset all regions at the beginning of a delivery step

    .. code-block:: python

        deactivate: all

    - next delivery has no Range Shifter, so deactivate it

    .. code-block:: python

        deactivate: RS


.. index::  ! Managing geometry configurations, save_regions:, restore:

Managing geometry configurations
--------------------------------

There are 10 available slots for saving and restoring geometry configurations. The configurations can be saved and restored at any time of the delivery sequence.


- **save_regions:**

    Save the current setup to a given slot. Syntax:

    .. code-block:: python

        save_regions: slotNum

    Example:

    - Save the initial configuration to slot no. 0

    .. code-block:: python

        save_regions: 0


- **restore:**

    Restore the setup saved in the given slot. Syntax:

    .. code-block:: python

        restore: slotNum

    Example:

    - Recall the configuration saved in slot no. 3

    .. code-block:: python

        restore: 3


.. index::  ! Beam delivery, deliver: 

Beam delivery
--------------------------------

The delivery of the beam into the prepared setup can be managed at two levels. We can deliver a single field, i.e. all the pencil beams belonging to that field. We can also deliver pencil beam by pencil beam, changing eventually the setup from one pencil beam to the next one. The **deliver:** directive defines which fields of pencil beam will be delivered. This directive comes with various syntax:

- deliver all defined fields (this is the default, if no *deliver:* directives are present)

    .. code-block:: python

        deliver: all

- deliver just selected fields

    .. code-block:: python

         deliver: fieldList

    Example:

    - deliver field 1 and field 2

    .. code-block:: python

        deliver: field_1 field_2

- deliver selected single pencil beam from selected field

    .. code-block:: python

        deliver: pb pbNum fieldNum

    Example:

    - deliver pencil beam 1 of field 1 and then pencil beam 33 of field 2

    .. code-block:: python

            deliver: pb 1 1
            deliver: pb 33 2

- deliver multiple selected pencil beams from selected field

    .. code-block:: python

        deliver: pb pbBeg:pbEnd fieldNum

    Example:

    - deliver pencil beams from 1 to 155 (included) of field number 3

    .. code-block:: python

        deliver: pb 1:155 3


.. index::  ! Invoking scripts, run_script:, add_searchpath:, postdelivery_script:

Invoking scripts
--------------------------------

At different times during a delivery is possible to execute external scritps, e.g. for post-processing a step, collecting data, saving disk space by cleaninig unnecessary output, etc.

It is possible also to queue scritps to be executed at the end of a run, after all beam deliveries have been carried out. This is an opportunity to collect data and info from a simulation just before exiting the program.


- **run_script:**

    Invokes the listed scripts in the given order. The number of current delivery step is passed over to the script as first argument. The interpreter to be used is guessed by the script file extension, e.g **.sh**  scripts are executed by **sh**, and **.py** scripts are executed by **python**. Syntax:

    .. code-block:: python

        run_script: scriptList


    Example:

    - deliver field 1 and directly run *getMinMaxDose.py* and then *copyDose.sh* scripts when the delivery finishes. Then do other stuff and deliver field 2 and run the scripts again.

    .. code-block:: python

        ...
        deliver: field_1
        run_script: getMinMaxDose.py copyDose.sh
        ...
        deliver: field_2
        run_script: getMinMaxDose.py copyDose.sh
        ...


- **add_searchpath:**

    Prepends the paths to the list of searched locations. When a script is invoked, the current working directory of the simulation is searched first, then the search paths are followed to find the script. Syntax:

    .. code-block:: python

        add_searchpath: pathList


    Example:

    - Execute the *fieldReport.py* script that is contained in the user repository of FRED scripts */home/user/fred_scripts*

    .. code-block:: python

        ...
        add_searchpath: /home/user/fred_scripts
        ...
        deliver: field_1
        run_script: fieldReport.py
        ...




- **postdelivery_script:**

    Appends the listed scripts to the queue of scritps that will be executed just before exiting the program, after all delivery steps are carried out. Syntax:

    .. code-block:: python

        postdelivery_script: scriptList

    Example:

    - Execute *finalPatientReport.py* script after all delivery

    .. code-block:: python

        ...
        postdelivery_script: finalPatientReport.py

        deliver: field_1
        ...
        deliver: field_2
        ...
        deliver: field_3
        ...
