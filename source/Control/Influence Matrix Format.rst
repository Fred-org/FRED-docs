.. _influenceMatrixDescription:

Influence Matrix File Format
============================

.. index::  ! Influence Matrix File Format

FRED uses a binary file format to store the influence matrix in a sparse format, describing the influence of each pencil beam on each voxel in the patient. By default, the influence of each pencil beam is stored per primary but the user can ask for the results to be stored per given number of primaries, depending on the weights in the rtplan. i.e. in the same way as the cumulative scorer is saved (see :ref:`lWriteIJPerPrim<Other_control_options>` control option). Any quantity can be stored in the influence matrix, such as dose, fluence, LET, etc, which can be controlled by the ``scoreij`` directive in the :ref:`region definition<region_scorers>`. Usually, an influence matrix contains a single component (e.g. dose, dose-to-water) but it can contain multiple components (e.g. numerator and denominator of LETd). The influence matrix is stored in a binary file with the extension ``.bin`` in various versions, defined by the user with the :ref:`ijFormatVersion<Other_control_options>` control option. The description below shows the structure of the binary files. The methods for reading and manipulating the influence matrix files are implemented in the `FREDtools <https://fredtools.ifj.edu.pl/>`_ package (from v. 0.8.11) in the ``fredtools.inm_io`` and ``fredtools.inmManipulate`` modules.

Influence Matrix v. 2.0
-----------------------


The format is designed to be as compact as possible. The file is divided into two parts: image header and data for each pencil beam. The data for each pencil beam is stored in a separate block, with the pencil beam tag, the number of voxels influenced by the pencil beam, the list of voxel indices, and the list of values.

- image header (48B):
    - **file version** (int32 : 4B)
        Version of the file in the integer format (20 for this file version).
    - **[X,Y,Z] size** (3 x int32 : 3 x 4B)
        Size of the image.
    - **[X,Y,Z] voxel spacing** (3 x float32 : 3 x 4B)
        Voxel spacing of the image in cm.
    - **[X,Y,Z] voxel offset** (3 x float32 : 3 x 4B)
        voxel offset of the image in cm.
    - **components no.** (int32 : 4B)
        Number of components saved in the data, e.g. 1 for dose, 2 for LETd, N for spectra with N bins.
    - **pencil beams no.** (int32 : 4B)
        Number of pencil beams saved in data.
- data for pencil beams (pencil beams no. * (4B + 4B + number of voxels x 4B+  number of voxels x components no. x 4B)):
    - **pencil beam tag** (int32 : 4B)
        Tag of the pencil beam (PBTag) describing field ID (FID = PBTag // 1000000) and pencil beam ID (PBID = PBTag % 1000000).
    - **number of voxels** (int32 : 4B)
        Number of voxels influenced by the pencil beam.
    - **voxel indices** (number of voxels x int32 : number of voxels x 4B)
        List of voxel indices of the voxels influenced by the pencil beam.
    - **voxel values** (number of voxels x components no. x float32 : number of voxels x components no. x 4B)
        List of values in form [data1Component1, data1Component2, ..., data2Component1, data2Component2, ...].

Influence Matrix v. 3.0
-----------------------

The format occupies more disk space than the v. 2.0, however it was aligned to the scipy/cupy sparse matrix format, allowing for much faster reading of the files in python, directly to the sparse matrix, including direct reading to GPU.

The file is divided into three parts: image header, data header, and data for each component. The data for each component is stored in the compressed sparse row (CSR) format, where the indices of the pencil beams and voxels are stored in separate arrays, and the values are stored in a single array.

- image header (48B):
    - **file version** (int32 : 4B)
        Version of the file in the integer format (30 for this file version).
    - **[X,Y,Z] size** (3 x int32 : 3 x 4B)
        Size of the image.
    - **[X,Y,Z] voxel spacing** (3 x float32 : 3 x 4B)
        Voxel spacing of the image in cm.
    - **[X,Y,Z] voxel offset** (3 x float32 : 3 x 4B)
        voxel offset of the image in cm.
    - **components no.** (int32 : 4B)
        Number of components saved in the data, e.g. 1 for dose, 2 for LETd, N for spectra with N bins.
    - **pencil beams no.** (int32 : 4B)
        Number of pencil beams saved in data.
- data header (pencil beams no. x 12B + components no. * 4B)
    - **pencil beam mapping** (pencil beams no. x 12B)
        Mapping of the pencil beam index (PBidx) to field ID (FID) and pencil beam ID (PBID). :
            - PBidx, FID, PBID (3 x uint32 : 3 x 4B)
            - …
    - **components data size** (components no. x 4B)
        Size of the data for each component.
            - component 1 data size (uint32 : 4B)
            - component 2 data size (uint32 : 4B)
            - …
- data for components (3 x component 1 data size x 4B) + (3 x component 2 data size x 4B) + …):
    - component 1 (3 * component 1 data size * 4B), for each PB:
        - list of PB indices in form [PBidx1, PBidx1, … PBidx2, … PBidx3, …] 
            (component 1 data size x uint32 : component 1 data size x 4B)
        - list of voxel indices in form [VoxelIdx1, VoxelIdx2, VoxelIdx2, VoxelIdx4, …] 
            (component 1 data size x uint32 : component 1 data size x 4B)
        - list of values in form [data1, data2, data3, data4, …] 
            (component 1 data size x float32 : component 1 data size x 4B)
    - component 2 (3 * component 2 data size * 4B), for each PB:
        - list of PB indices in form [PBidx1, PBidx1, … PBidx2, … PBidx3, …] 
            (component 2 data size x uint32 : component 2 data size x 4B)
        - list of voxel indices in form [VoxelIdx1, VoxelIdx2, VoxelIdx2, VoxelIdx4, …] 
            (component 2 data size x uint32 : component 2 data size x 4B)
        - list of values in form [data1, data2, data3, data4, …] 
            (component 2 data size x float32 : component 2 data size x 4B)
    - …