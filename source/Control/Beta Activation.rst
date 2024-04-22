.. _beta_plus_activation:

Beta+ Activation
================

.. index::  ! Beta+ Activation


Nuclear interactions within the patient can produce positron-emitting isotopes, such as C11, N13, and O15, activating the patient. These isotopes emit positrons, which can be used in PET imaging for treatment verification. 
A continuous scoring approach has been implemented, which scores the distribution of isotopes produced by the delivery of the fields [`McNamara, et al. 2022, PMB <https://doi.org/10.1088/1361-6560/aca515>`_]. Scoring of isotopes can be performed in FRED using cross-sections precalculated from Geant4, version 10.6 patch 1, with the QGSP_BIC nuclear interaction model. 

Scoring of isotopes is done by adding “activation” to your scored parameters. e.g.:


.. code-block:: none

   region: phantom ; CTscan = MrHead ; score = [dose, activation]

Settings for the activation scoring can be aligned with the **activation** directive, e.g.:

.. code-block:: none

   activation<
      isotopes = [C10,C11,N13,O14,O15]
      userCSPolicy = only
      userCSPath = /path/to/cs
   activation>

The following options are available, where the default parameters are given:

   isotopes = [C11,N13,O15]
      List of isotopes to score. Cross-sections must exist for at least one reaction pathway for each listed isotope.

   userCSPolicy = no
      The user cross-section policy. It determines if only user-provided cross sections should be used (userCSPolicy = only), the default pre-calculated QGSP_BIC cross sections should be used (userCSPolicy = no), or the user-provided cross sections supplemented with the default cross sections will be used (userCSPolicy = yes). If userCSPolicy is set to "yes" or "only", then userCSPath must be specified. The option “yes” will prioritize the user-provided cross sections when multiple options are present.

   userCSPath = path
      Path containing user-specified cross-sections. Cross sections are read in from files in the path named cs_TARGET_ISOTOPE.txt, where TARGET is an element within the patient geometry, and ISOTOPE is one of the isotopes to be scored, e.g. cs_O_O15.txt. By default, we consider the target elements to be in their natural isotope composition, such that cs_O_O15.txt is a weighted sum of reactions p + O16 -> O15 + X, p + O17 -> O15 + X, and so on. Cross section files should contain two columns: Energy (MeV), and cross section (mbarn).

   outputInterpolatedCS = false
      If true, the interpolated cross-sections used on the GPU during the calculation are saved in the output folder. Note that the cross-sections are sampled at the resolution of 1 MeV.

