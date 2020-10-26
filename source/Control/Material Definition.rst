.. index::  ! Material

Material Definition
=================================

Material directive allows to fine-tune an already defined material (e.g. water or PMMA), or to define a completely new material. A new material is described by a set of mandatory parameters:

    ID = materialID
        Name identifying the material

    rho = `(float)`
        Density of the material [g/cm\ :sup:`3`]

    Ipot = `(float)`
        Mean ionization potential [eV]

    Lrad = `(float)`
        Radiation length (g/cm\ :sup:`2`)

    composition = [`element_1,element_2,...`]
        Elemental composition of the material given as a list the short names of the elements. For instance, for water it would be [H,O].

    fractions = [`frac_1,frac_2,...`]
        Relative number fraction of elements given in the composition. For instance for water it would be [0.667,0.333].

    weights = [`frac_1,frac_2,...`]
        Relative weight fraction of elements given in the composition. For instance for water it would be [0.112,0.888].


To define a material based on other material, simply define:

    basedOn = `materialName`
        Clause used to import parameters from a predefined material.

In this case, the mandatory parameters are becoming optional and can be used to change properties with respect to predefined material. Note that the chemical composition cannot be changed when defining a material based on the other material.

Currently, the predefined materials in FRED are Vacuum, BlackHole, Water, Air, PMMA, Al, Ti, Cu, Ni, Si and LEXAN.

.. tip ::
    Run the command ``fred -materials`` to get detailed information on the predefined materials.

Example of material definition
----------------------------------------------------------
Multi-line definition of modified PMMA material for a range shifter:

.. code-block:: python

    material<
        ID=pmmaRS
        basedOn=pmma
        rho=1.16
        Ipot=74
        Lrad=45.822
    material>


Single line definition of modified water:

.. code-block:: python

    material:  myWater ; basedOn = water ; rho=0.97 ; Ipot = 76.2

Single line definition of graphite:

.. code-block:: python

    material:  Graphite ; rho=1.644 ; composition=[C]; Ipot = 78 ; Lrad =42.7
