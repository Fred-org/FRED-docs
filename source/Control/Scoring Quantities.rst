Scoring Quantities
==================

Several quantities can be scored inside the defined regions, e.g. dose, LETd.
Present implementation of scores in Fred is restricted to voxel-based scorers defined *on the same grid* of the referenced region. For instance, when scoring the dose on the phantom region, Fred accumulates the energy deposited in each voxel of the phantom during particle tracking. At the end of the run, the deposited energy is divided by the mass of the voxel and the dose map is saved to disk in mhd format.

Scorers are actived within the definition of each region, :ref:`as reported here <region_scorers>`.

An example of requiring dose and LETd scoring on a CTscan phantom is here below:

.. code-block:: none
    
    region: phantom ; CTscan = MrHead ; score = [dose,LETd]


.. index::  ! Scoring


There are two main ways of scoring quantities at the voxel level: *accumulator* and *influence matrix*.

In *accumulator mode*, the scorer accumulates in the voxel all scoring events for a given simulation, and at the end of the run FRED outputs in the `out/score` folder the final map. Typical example is the total dose delivered by all pencilbeams defined in a given treatment plan. The mode is activated using the ``score`` field in region definition. 

In *influence matrix mode*, FRED computes the scored quantities for each pencilbeam separately. Typical example is the dose influence matrix, also called the Dij matrix, which can be used to perform inverse-planning in a TPS code. The mode is activated using the ``scoreij`` field in region definition.
In order to save space,all pencilbeam maps are zero-suppressed and stored in a single binary file. The output is saved in the `out/scoreij` folder.

The following example shows how to score the total dose and total LETd, and also producing the Dij matrix:

.. code-block:: none
    
    region: phantom ; CTscan = MrHead ; score = [dose,LETd]; scoreij = [dose]

This will generate the file layout

.. code-block:: none
    
    out
    ├── score
    │   ├── Phantom.Dose.mhd
    │   └── Phantom.LETd.mhd
    └── scoreij
        └── Phantom.Dose.bin


Available scorers
-----------------
**Edep** 
    total energy deposited in a voxel

    .. math::
        E_{dep} = \sum_{events} \Delta E

    for each energy deposition event the voxel scorer is incremented by the :math:`\Delta E` energy released in the voxel. This energy is typically due to the collisional stopping power :math:`\frac{dE}{dx}` of the particle in the medium. It also can have contributions from heavy fragments produced in nuclear interactions which, due to very short range, are deposited locally at the production site.

    *Scoring units* = MeV

**dose** 
    total energy deposited in a voxel divided by the mass of the voxel

    .. math::
        \mathrm{Dose} = D = \frac{E_{dep}}{m} = \frac{E_{dep}}{\rho\;V}

    This is equivalent to *dose-to-medium* in dosimetry jargon.

    *Scoring units* = Gy

.. _dosetowater:

**dose-to-water** 
    equivalent dose to water obtained from stopping power conversion

    .. math::
        D_{w} = D \cdot \frac{\rho}{\rho_w} \cdot \frac{\left(\frac{dE}{dx}\right)_w}{\frac{dE}{dx}} = 
        D \cdot \frac{\left(\frac{dE}{ds}\right)_w}{\frac{dE}{ds}} = 
        D / RMSP

    where the dose-to-medium :math:`D` is converted into dose-to-water :math:`D_{w}` using the density ratio and the stopping power ratio. It is equivalent to divide the dose :math:`D` by the relative mass stopping power RMSP.


    *Scoring units* = Gy

**LETd**
    dose-averaged LET according to Eq. 14 in `Polster et al, PMB 2015 <https://doi.org/doi:10.1088/0031-9155/60/13/5053>`_

    .. math::
         \mathrm{LET}_d = 
         \frac{\sum_{events} \frac{dE}{dx} \frac{1}{\rho}\;\Delta E} {\sum_{events} \Delta E} = 
         \frac{\sum_{events} \frac{dE}{ds} \;\Delta E} {\sum_{events} \Delta E}


    *Scoring units* = :math:`\mathrm{\frac{MeV\,cm^2}{g}}`

**activation**
    positron emitting activation of patient tissue. See :ref:`Beta+ activation section <beta_plus_activation>` for details.



