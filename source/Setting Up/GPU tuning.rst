GPU tuning
=================================

GPU cards come with very different hardware capabilities and performance. It is possible to fine-tune the GPU performance using a few parameters that control the execution of the particle tracking kernel.

.. tip::

    You can check the GPUs installed on your system using ``fred -gpusetup`` 
    and then use the provided information to configure your environment using ``fred -config``.



Available environment variables and their default values:

.. code-block:: bash

    export FGE_PRIMARY_MAX_BATCH=1000000
    export FGE_SECONDARY_MULT_FACTOR=1
    export FGE_CL_NQUEUEDEV=6


.. index::  ! FGE_PRIMARY_MAX_BATCH

FGE_PRIMARY_MAX_BATCH
    Set the number of primary particles sent to GPU for each kernel invocation.

    A large enough buffer will reduce the number of kernel invocations and the communication times between CPU and GPU.

.. index::  ! FGE_SECONDARY_MULT_FACTOR

FGE_SECONDARY_MULT_FACTOR
    Increase the particle buffer by this *integer* multiplication factor.

    For a proton beam, the number of secondary produced is always less than the primary number, so by default, FGE_SECONDARY_MULT_FACTOR is set to 1.
    For a carbon beam, the number of secondary fragments per primary ion is up to 3.5 in the therapeutic range, so FGE_SECONDARY_MULT_FACTOR = 4 is typically requested.

.. note::
    FRED will quietly signal the occurrence of a particle buffer overflow at the end of a simulation. In that case, try to understand the problem and readjust the buffer size using FGE_SECONDARY_MULT_FACTOR.

.. index::  ! FGE_CL_NQUEUEDEV

FGE_CL_NQUEUEDEV
    Set the number of independent execution queues on each device. 

    A number >=2 is required for hiding memory transfer latency between CPU and GPU. 
    A number 4-6 of queues is required to increase performance in generating the dose influence matrix Dij.

.. tip::
    In case of memory shortage on the GPU, the variables FGE_PRIMARY_MAX_BATCH, FGE_SECONDARY_MULT_FACTOR, and FGE_CL_NQUEUEDEV can be used to reduce the memory needed by the GPU kernel.

    Try changing the values depending on the type of simulation you want to run. 

    Check the relative performance using for instance :code:`fred -benchmark 1e7`.

    Once you find a satisfactory set of parameters, you can add the envvars to the FRED configuration file (.fredrc in Linux or Registry in Windows).
