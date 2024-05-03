.. _python_meta_input:

Meta input using Python
=================================

Python syntax can be used in FRED input files to generate very powerful, compact and versatile meta input.
It is possible to define *constants*, *variables*, and  *functions*. You can also use **for**-loops to generate complex input structures. The input file is preparsed by the Python interpreter that generates the actual input file before invoking FRED executable.

.. important::
    
    The Python interpreter is invoked with the following environment:

    .. code-block:: python

        from math import *
        from random import *
        import numpy as np
        from numpy import dot, cross, prod

        # some utility functions 

        def norm(v): # modulus of a vector
            return sqrt(dot(v,v))

        def distance(P,Q): # distance between two points
            return norm(P-Q)

        def mod(m,n): # remainder of integer division
            return m%n

    All the *numpy* features are available for the creation of meta-input.


Hereafter, the implemented directives and control structures.

- **def:**

    constant parameter definition. Syntax:

    .. code-block:: bash

        def: name = value

    Example:

    .. code-block:: bash

        def: N = 5 # number of turns
        def: nspots = 100 # total number of spots
        def: Rmax = 3 # major radius
        def: Rmin =0 # minor radius
        def: Rmean = (Rmax+Rmin)/2

- **func:**

    function definition. Syntax:

    .. code-block:: bash

        func: name(args...) = expression

    Example:

    .. code-block:: bash

        func: Sdisc(r) = pi*r**2 # disc area
        func: Vsphere(r) = 4./3.*pi*r**3 # sphere volume
        func: Vbox(a,b,c) = a*b*c # box volume
        
        func: r(theta) = Rmax-(Rmax-Rmin)*theta/(N*2*pi) # spiraling radius

- **substitution of scalar parameters in normal FRED input**
    
    *scalar* parameters defined using **def:** directive can be inserted in normal input by the Python preparser. Syntax:

    .. code-block:: bash

        $parname

    Example:

    this meta-input 

    .. code-block:: bash

        # how to define the number of voxels for a given spacing

        def: Lx = 8 # cm
        def: Ly = 6 # cm
        def: Lz = 13 # cm

        def: spacing = 0.3 # 3 mm voxels

        def: nx = int(Lx/spacing)
        def: ny = int(Ly/spacing)
        def: nz = int(Lz/spacing)

        region: phantom ; L=[$Lx,$Ly,$Lz] ; voxels = [$nx,$ny,$nz]

    will generate to following input to FRED

    .. code-block:: bash

         region: phantom ; L=[8,6,13] ; voxels = [26,20,43]

- **substitution of vector parameters in normal FRED input**
    
    *vector* parameters defined using **def:** directive and numpy arrays can be inserted in normal input by the python preparser. Syntax:

    .. code-block:: bash

        ${parname}

    For instance, the previous example can be obtained  in a more compact way using numpy arrays

    .. code-block:: bash

        def: L = np.array([8,6,13])
        def: spacing = 0.3

        def: nn = (L/spacing).astype(int)

        region: phantom ; L=${L} ; voxels = ${nn}

- **substitution of expressions in normal FRED input**
    
    expressions are evaluated by the python preparser and placed in FRED input using the following syntax:

    .. code-block:: bash

        ${expression}

    Example:

    this meta-input 

    .. code-block:: bash
        :emphasize-lines: 11

        # how to define a beam with tranverse area equal to half of phantom entry surface

        def: Lx = 8 # cm
        def: Ly = 8 # cm
        def: Lz = 20 # cm

        func: myDiameter(S) = sqrt(4*S/pi) # diameter of a disc with area S

        region: phantom ; L=[$Lx,$Ly,$Lz] ; voxels = [200,200,100]

        pb: 1 0 ; Xsec = disc ; FWHM = ${myDiameter((Lx*Ly)/2)}


    will generate to following input to FRED

    .. code-block:: bash

        region: phantom ; L=[8,8,20] ; voxels = [200,200,100]
        pb: 1 0 ; Xsec = disc ; FWHM = 6.38308


- **for()<...>**

    definition of a multiline loop to be executed by the preparser. Syntax:

    .. code-block:: bash

        for (condition) <
            ...
            ...
            ...
        for>

    For constructs can be nested: indentation level must be preseved as in normal python code.

    Example:

    .. code-block:: bash
        :emphasize-lines: 1,8

        for(th in np.linspace(0,N*2*pi,nspots))<

            def: x = r(th)*cos(th)
            def: y = r(th)*sin(th)
            transform: phantom move_to $x $y 0
            deliver: all

        for>

    (see the complete example :ref:`Spiralling Spots irradiation pattern <spiralling_spots>`)


- **if()<...>**

    conditional execution of a block of code by the preparser. Syntax:

    .. code-block:: bash

        if (condition) <
            ...
            ...
            ...
        for>

    Example: *using* **for** *and* **if** *to produce a chessboard irradiation pattern*

    .. code-block:: bash
        :emphasize-lines: 4,9

        for(ix in range(nspot+1))< # control points in x
            for(iy in range(nspot+1))< # control points in y

                if(mod(ix,2)==mod(iy,2))< # choose alternate squares
                    def: x = -side/2 + ix*spotSpacing
                    def: y = -side/2 + iy*spotSpacing
                    transform: field_0 move_to $x $y -50
                    deliver: all
                if>
            for>
        for>

    (see the complete example :ref:`Chessboard irradiation pattern <chessboard>`)

