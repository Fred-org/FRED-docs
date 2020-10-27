.. index::  ! HU Calibration

HU Calibration Curve
=================================

TODO

*   info on HU values, CT scans, NMR, PET and such
*   dosimetric procedure for calibration: irradiation of inserts, measurements, TPS calibration
*   HU materials in FRED: properties that can be tuned (rho,composition,Lrad,Ipot)
*   built-in calibration curve based on Schneider-Parodi parametrization
*   how an experimental discrete table (few points) is converted internally in a dense table (one entry of each interger HU value)
*   how to import a CT scan 
*   built-in MrHead for quick tests
*   how to import an HUCal

    *	HU-based materials
    *   lAllowHUClamping
    *	lUseInternalHU2Mat

*   examples of HU calibration curves


.. code-block:: none

	matColumns: HU rho RSP Lrad C Ca H N O P Ti S
	# Units: dimensionless g/cm^3 dimensionless g/cm^2 % % % % % % % %
	mat: -1000 0.00 0.00 36.50 0.01 0 0 75.52 23.17 0 0 1.3
	...
	mat: -608 0.384 0.380 36.508 10.7 0 10.3 3.2 74.6 0.1
	...
	mat: -200 0.800 0.794 36.533 10.951 0 10.306 3.187 74.359 0.199 0 0.996
	...
	mat: 0 1.008 1.011 38.550 32.692 0.011 10.719 2.195 53.619 0.124 0 0.637
	...
	mat: 2000 3.152 2.583 21.975 0.088 39.788 0.218 0.026 41.416 18.455 0 0.006
	...
	mat: 3000 4.506 3.212 16.164 0 0 0 0 0 0 100 0
	

..	index:: uniform HU phantom

.. tip::
	For testing purposes, it could be handy to fill a volume with a uniform HU material. The syntax is the following:

	.. code-block:: none

		region: phantom ; material = HU-400   # fill phantom with HU = -400 values
		
		region: phantom ; material = HU+1250   # fill phantom with HU = +1250 values
