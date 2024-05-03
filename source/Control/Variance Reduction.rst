Variance Reduction
==================

*New in version 3.70.0*

This module allows to estimate and reduce the statistical error of Monte Carlo (MC) simulations. The strategy applies to the **dose** map in the **phantom**.

The MC simulation is split into a series of subsequent iterations, each tracking a sample of the actual primary particles delivered by the accelerator in the given RTPLAN.
The algorithm estimates the mean dose error in the voxel by acquiring statistical information after each iteration.

Each iteration will produce an estimate :math:`d_{i,n}` of the dose, where  :math:`i` is the voxel index and :math:`n` is the iteration index.

The mean dose :math:`D_i` in the ith voxel out of :math:`n=1,...,N` iterations is defined as

.. math::
        D_i = \frac{1}{N}\sum_{n=1}^{N} d_{i,n}

and the standard deviation :math:`\sigma_i` in the ith voxel is

.. math::
    \sigma_i = \sqrt{\frac{1}{N-1}\sum_{n=1}^{N} (d_{i,n}-D_i)^2}

finally the mean dose error in the voxel is given by

.. math::
    \Delta D_i = \frac{\sigma_i}{\sqrt{N}}

The module computes estimates of the dose mean error for a subset of phantom voxels (see below). By increasing the MC statistics, i.e. the number of traced particles, it is possibile to reduce the statistical MC error below a given threshold.

Using a language borrowed from the gamma-index criterium definition, we define these control parameters

    DCO = dose cut-off (%)
        consider only voxels whose dose is larger than DCO percentage of dose global maximum 

    DD = dose difference or error (%)
        voxels whose dose mean error :math:`\Delta D` is smaller than DD are passing the convergence test

    DDType = GLOBAL/LOCAL
        if GLOBAL, the :math:`DD_i=\Delta D_i/D_{max}` , if LOCAL the :math:`DD_i=\Delta D_i/D_i`
    
    DGRef = Dose Global Reference value (Gy)
        can be used to prescribe a fixed value for DD evaluation using GLOBAL criterium, i.e. :math:`DD_i=\Delta D_i/DGRef`
    
    maxNumIterations
        maximum number of iterations, after which, if convergence has not been reached, the iteration procedure is stopped anyway (default value = see below)

    lStratifiedSampling = (T/F)
        use stratification in pencil beam primary sampling, i.e. the number of primary per PB is proportional to the PB fluence (number of primary particles delivered by the accelerator)

    lWriteDoseMeanError = (T/F)
        output the map of computed dose mean error in ``out/DoseMeanError.mhd``

    lWriteDoseStdev = (T/F)
        output the map of computed dose standard deviation in ``out/DoseStdev.mhd``



The dose error is reported in the output file and logged in the ``out/log/iterations.txt`` file during the iterations.


Three different modes of operations can be used
    1. fixed repeated iterations
    2. recalculation percentage
    3. reduction of dose error until convergence


Fixed repeated iterations
-------------------------

.. code-block::

    varianceReduction: maxNumIterations=10

In this mode, the simulation is repeated a fixed number of times. By default, stratification is off, so the number of primaries per PB is prescribed using ``nprim``. If you want to use stratified sampling, you have to require it explicitly

.. code-block::

    varianceReduction: maxNumIterations=10 ; lStratifiedSampling=t


At the end of iterations, a report on the mean dose error obtained above DCO is given.


Recalculation percentage
------------------------

.. code-block::

    varianceReduction: recalculationPrimaryPercentage = 1

The number of simulated primary particles is a given percentage of the total number of primaries delivered by the accelerator in the RTPLAN.

By default, the simulation is split into 10 iterations, and stratification is applied.


Dose error reduction
--------------------

A goal error using ``DD`` is specified, and FRED keeps on iterating the simulation until the dose mean error reduces below ``DD`` in all the voxels above the ``DCO``.
If convergence is not reached, the iterating procedure is stopped after a ``maxNumIterations``.

.. code-block::

    varianceReduction<
        DD = 1   # 1% dose error
        DCO = 50  # consider voxels above the 50% isodose
        DDType = G # use the GLOBAL criterium as described see above (default)
        maxNumIterations = 100 # default value for this mode
    varianceReduction>



