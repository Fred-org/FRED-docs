Physics Control
=================================

The implemented physics modules and be activated/deactivated for investigating the relative importance of simulated processes in a given setup.

.. index::  ! lTracking_dEdx,lTracking_fluc,IonizPotential,stoppowPathlengthCutoff,stoppowDTmax

Stopping power module
------------------------------
	lTracking_dEdx = T|f
		activate/deactivate energy loss by ionization

	lTracking_fluc = T|f
		activate/deactivate energy loss fluctuations (a.k.a. energy straggling)


	IonizPotential = (float)
		retune the mean ionization potential [eV] of liquid water

		Default value: 75 eV


	stoppowPathlengthCutoff = (float)
		residual particle pathlength [cm] that is used to define the tracking cut-off energy

		Default value: 0.0010 cm = 10 um

	stoppowDTmax = (float)
		max allowed fractional energy loss in a single step (i.e. the energy step limiter)

		Default value: 0.02 = 2%


.. index::  ! lTracking_nuc_el,lTracking_nuc_inel,lTracking_nuc

Nuclear interaction modules
------------------------------

	lTracking_nuc_el = T|f
		activate/deactivate nuclear *elastic* interactions

	lTracking_nuc_inel = T|f
		activate/deactivate nuclear *inelastic* interactions

	lTracking_nuc = T|f
		activate/deactivate all nuclear interactions (both elastic and inelastic)


.. index::  ! lTracking_mcs,mcsMode

Multiple Scattering module
------------------------------

	lTracking_mcs = T|f 
		activate/deactivate Multiple Coulomb Scattering (elastic scattering)

	mcsMode = (integer)

		0 = single gaussian distribution based on Highland's formula (1G-H)

		1 = single gaussian distribution using tabulated values (1G)

		2 = double gaussian distribution using tabulated values (2G)

		3 = triple gaussian distribution using tabulated values (3G)

		4 = gaussian distribution + 2 Rutherford-like tails using tabulated values (G2R)

		5 = double gaussian distribution + Rutherford-like tail using tabulated values (2GR)

		6 = single effective gaussian distribution: Rossi-Greisen formula + correction a' la Fippel (1G-RGF)

	Default mode: 6 