Hardware Requirements and Performance Summary
=============================================

FRED can run on various hardware configurations, from laptops to workstations and HPC clusters.

When we started developing FRED, the goal was to make a Monte Carlo dose engine capable of recalculating a whole patient treatment plan in particle therapy within minutes.
This still is our main objective, and the hardware configuration that fits best performance and budget constraints is a workstation equipped with a good CPU and a powerful GPU card.

The main characteristics that affect FRED performance are:

    **Main CPU memory (RAM):**

        8 GB is the minimum for typical clinical cases to hold patient CT information, material properties, and scored quantities. **16 GB is recommended**, and 32 GB offers enough perspective for scoring-intensive simulations (e.g., spectra, activation, influence matrix, etc.).

    **Local disk space for software installation:**

        The disk footprint of a FRED release is small (typically less than 50 MB). Foreseeing a few versions installed on the system, 200 MB of dedicated disk space is more than enough.

    **Local disk space for simulations:**

        A typical patient recalculation can produce from 500 MB to a few GB, depending on grid resolution and the number of activated scorers. Generating the influence matrix for thousands of pencil beams typically produces tens of GB. A good **SSD of 1 or 2 TB** is a good choice. 

    **Main processor (CPU) (simulation initialization and setup):**

        The CPU performs input file parsing, initialization, and particle start point generation. Many tables are generated at runtime on the CPU: to accomplish this task well, an *exacore* or *octacore* CPU decently fast (> 3 Ghz base clock frequency) is recommended.

    **Main processor (CPU) (particle tracking):**

        FRED can track particles in parallel on the CPU using multicore processor capabilities. The tracking rate of a single core is about :math:`2 \cdot 10^4\,\frac{prim.}{s}`, and the performance scaling is sublinear due to memory bandwidth limitations, thermal protection mechanisms, hyper-threading, and other similar characteristics of modern multicore CPUs. On a high-end processor, one can expect up to :math:`150-200 \cdot 10^3\,\frac{prim.}{s}`.

    **GPU card(s) (particle tracking):**

        FRED achieves maximum particle tracking rate on GPU hardware. Although the tracking kernel is coded in OpenCL, all development machines at Sapienza Univ. and all present FRED users use NVidia hardware. In principle, AMD GPUs could also run FRED, but no testing hardware is currently in operation. Integrated GPUs on Apple Silicon have not been supported since years ago when Apple discontinued OpenCL support in favor of the proprietary API called Metal.

        Hence, the current recommendation is a good **GPU card from NVidia**. Note that FRED can drive multiple GPUs on the same workstation, even of different capabilities, by balancing the workload assigned to each card. Performance scaling is almost perfectly linear with the number of GPUs.

        When choosing a GPU card, look at available RAM (at least 8 GB) and peak performance in *single precision floating point* operation (FP32 TFLOPS). Expensive Quadro and/or Tesla series cards will not necessarily perform better than lower-budget consumer cards of the GeForce series.

        Hereafter is a brief table with the expected tracking rates for FRED benchmark test:

        .. table:: Tracking rate in :math:`\frac{prim.}{s}` for selected GPU cards

            +--------------------------+-------------------------+
            | Card Name                |  Tracking rate          |
            +==========================+=========================+
            |  NVIDIA RTX 2080 Ti      |  :math:`2.5 \cdot 10^6` |
            +--------------------------+-------------------------+
            |  NVIDIA Titan Xp         |  :math:`4 \cdot 10^6`   |
            +--------------------------+-------------------------+
            |  NVIDIA RTX A5000        |  :math:`5.6 \cdot 10^6` |
            +--------------------------+-------------------------+
            |  NVIDIA RTX 3090         |  :math:`7 \cdot 10^6`   |
            +--------------------------+-------------------------+
            |  NVIDIA RTX 4090         |  :math:`14 \cdot 10^6`  |
            +--------------------------+-------------------------+
            


Performance Summary
-------------------
This information is old and out-of-date as soon as it is published: new hardware is coming up, and the performance of CPU and GPU cards is improving steadily. Hence, this table is just an order-of-magnitude summary of the tracking performance one can expect to achieve.

.. figure:: Performance.png
    :alt: typical tracking performance
    :align: center
    :width: 90%

    Comparison of tracking performance and typical simulation times for different hardware 

