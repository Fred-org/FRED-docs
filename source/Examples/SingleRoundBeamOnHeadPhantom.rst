Round beam on a head phantom
=================================

Import the built-in CT scan of an anthropomorphic phantom and deliver a round beam of 100 MeV protons.

Input file:

.. code-block:: python

	# geometry definition
	region<
	 ID=phantom ; CTscan=MrHead ; lWriteCTHU=t ; score = Dose ; lWriteLETd_parts =t; 
	 pivot=[.5,.5,.5] ; O = [0,0,20]
	region>

	lUseInternalHU2Mat= t # use built-in HU calibration curves based on Schneider 1996/2000
	lAllowHUClamping=t # clamp HU values outside defined range


	# source definition
	pbXsec=disc # round cross section with uniform distribution
	pbFWHM=5 # diameter of the beam
	pbE = 100 # energy of beam[MeV] 

	nprim=1e5 # no of primary protons to deliver


.. tip::
    `MrHead` is a built-in CT scan at low resolution (2x2x2 mm) of an anthropomorphic phantom that you can use to explore FRED capabilities in tracking particles through a heterogeneous phantom.

Results:

.. figure:: MrHead/Dose_Phantom_overlay.png
    :alt: Dose-Phantom overlay
    :align: center
    :width: 90%

    Dose-Phantom overlay
