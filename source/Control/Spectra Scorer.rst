.. _spectra_scorer:

Spectra Scorers
================

.. index::  ! Spectra Scorer

FRED is capable to score spectra of a given quantity with a predefined binning for each voxel of a voxelized geometry. The results are saved to multicomponent MetaImage files (MHD), where each voxel is a vector of the spectrum values. Additionally, the binning definition and the spectrum unit are saved as `spectrumBins` and `spectrumUnit` private tags, respectively, whereas the bins are defined as the bin edges, with the accordance to the ``numpy.histogram`` definition. To enable the spectrum scorer for a given region, the `spectra` parameter must be set as one of the scorer in the region definition (e.g. score = [Dose, spectra]). The type of the specrum and binning definition can be controlled in a `spectraScorer` multi-line definition with the following parameters:

    spectrumType : obligatory 
        Type of the spectrum to score (e.g. LETMethodC, see the description below)

    binningType : obligatory
        Type of the binning. `lin`` or `log`` for linear or logarithmic binning.

    binningMin : 0 for `lin`, 1E-6 for `log``
        Minimum value of the binning. In case of the logarithmic binning and binningMin=0, the value will be internally set to 1E-6.

    binningMax : 100
        Maximum value of the binning.

    binningStepNo : 100
        Number of bins. The bin size is calculated to evenly distrubute bins between `binningMin` and `binningMax` in linear or logarithmic scale.

The following spectra types are implemented with the symbols used in the formulas:
    - :math:`s` - energy deposition step 
    - :math:`S` - total number of energy deposition steps of a particle in a voxel
    - :math:`\epsilon_s` - deposited energy by the particle during the step :math:`s`
    - :math:`l_s` - length of the step :math:`s`
    - :math:`SP^{el}` - electronic stopping power table

The methods of the LET computation have been implemented and named as methods A, B and C based on the Cortes-Giraldo and Carabe (PMB, 2015, doi:10.1088/0031-9155/60/7/2645) paper.

Kinetic energy
--------------

``spectrumType = EkinIn``

The spectrum of kinetic energy of protons entering a voxel, i.e. :math:`E_{kine}^{in}`. Only the kinetic energy of protons that enter a voxel (primary and secondary) are scored but no secondaries produced in the voxel. 

``spectrumType = EkinInProd``

The spectrum of proton kinetic energy entering a voxel and the initial energy of protons produced in the voxel, i.e. :math:`E_{kine}^{in+prod}`. The kinetic energy of protons that enter a voxel (primary and secondary) are scored, as well as the initial energy of secondary protons produced in the voxel. 

Deposited energy
----------------

``spectrumType = Edep``

The spectrum of the total deposited energy of protons in a voxel. The deposited energy of a single proton in a voxel is calculated as:

.. math::
    E_{dep} = \sum_{s=1}^{S} \epsilon_s \quad .

The deposited energy is summed in a voxel for each proton entering the voxel and produced in the voxel, separately. 

``spectrumType = EkinEdep``

The spectrum of kinetic energy differential in deposited energy, i.e. :math:`E_{kine}(E_{dep})`. This scorer requires a float type of multi-component image. 

Track length
------------

``spectrumType = TrackLength``

The spectrum of the total track length of protons in a voxel. The track length of a single particle in a voxel is calculated as:

.. math::
    L = \sum_{s=1}^{S} l_s \quad . 

The total step lengths are summed in a voxel for each proton entering the voxel and produced in the voxel, separately. 

Linear energy transfer
----------------------

``spectrumType = LETSPEkinIn`` - Electronic stopping power of incoming particles  

The spectrum of LET calculated as the stopping power value of the particle entering a voxel, taken from the SPT. The LET of a single particle is given by:

.. math::
    LET = SP^{el}(E_{kine}^{in}) \quad .


``spectrumType = LETMethodA`` - Method A: averaging over each step

The LET of a single proton is calculated for each step and then averaged by the total energy deposited. The LET of a single particle is given by:

.. math::
    LET = \frac{\sum_{s=1}^{S}\frac{\epsilon_s^2}{l_s}}{\sum_{s=1}^{S} \epsilon_s} \quad .


``spectrumType = LETMethodB`` - Method B: averaging over total track

The LET of a single particle is calculated as the ratio of its total energy deposition to total track length within a voxel, i.e.:

.. math::
    LET = \frac{\sum_{s=1}^{S} \epsilon_s}{\sum_{s=1}^{S} l_s} \quad .

``spectrumType = LETMethodC`` - Method C: averaging stopping power with deposited energy

The spectrum of LET for each step is calculated as the electronic stopping power, :math:`SP^{el}_{s}`, taken from the precomputed electronic stopping power tables, for the arithmetic mean kinetic energy of the values at pre- and post-step points, i.e. :math:`\overline{E}^{s}_{kine} = (E^{A}_{kine} + E^{B}_{kine}) \cdot 0.5`. The LET is then averaged by the total energy deposited, and the LET of a single particle is given by:

.. math::
    LET = \frac{\sum_{s=1}^{S} SP(\overline{E}_{kine}^{s}) \cdot \epsilon_s}{\sum_{s=1}^{S} \epsilon_s} \quad .








