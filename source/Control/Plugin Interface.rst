Plugin Interface
=================================

Plugin API
----------


- Plugin initialisation

    .. c:function:: extern "C" int UserHook_init(const char *vers)

       Initialises the plugin.

       :param vers: current version of calling Fred executable
       :type vers: const char *
       :return: error code (0=OK)
       :rtype: int


- Plugin final call

    .. c:function:: extern "C" int UserHook_close()

       The plugin can do postprocessing, bookkeeping, writing a summary report, etc. before the simulation is ended.

       :return: error code (0=OK)
       :rtype: int



- Step-by-step control of particle tracking

    These functions allow the user to monitor and/or alter the propagation of a given particle at the level of a single step.
    They are called just before and just after the internal routines that advance the particle by a step.

    .. c:function:: extern "C" int  UserHook_step_bfr(Step *stp)

        Control is given to the plugin **before** taking the step.

        :param stp: current step structure
        :type stp: Step *
        :return: APPLY/SKIP
        :rtype: int

        If APPLY is returned, Fred internal *step routines* will executed, hence the plugin acts as a diagnostic tool, not changing the particle evolution.

        If instead `SKIP` is returned, then internal step routines are bypassed, and the plugin is taking complete control of the stepping procedure.

    .. c:function:: extern "C" void  UserHook_step_aft(Step *stp)

        Control is given to the plugin **after** taking the step. The plugin can monitor the stepping procedure and score quantities at the step level.

        :param stp: current step structure
        :type stp: Step *
        :return: none


- Plugin runtime and execution options

    .. c:function:: extern "C" bool isPluginThreadSafe()

       Tell Fred that the plugin can be executed in parallel on many threads. It is reponsability of the developer to check that data race conditions are not occurring during multi-thread execution. By default, Fred assumes that plugin code is **not thread-safe** and switches to serial, i.e. single-thread, execution.

       Semaphore control functions are provided for enforcing atomic operations on shared data.

       :return: true if plugin is thread-safe
       :rtype: bool

- Boundary crossing

    .. c:function:: extern "C" void UserHook_domain_boundary_crossing(Step * stp,bool entering)

        ...

        :param stp: current step structure
        :type stp: Step *

        :param bool entering:


        :return: none


Getting input parameters for the plugin
---------------------------------------

Input parameters for the plugin can be written in the main input file (e.g. ``fred.inp``) and queried using plugin parsing routines.

    .. important::
    
        User-defined parameters must be enclosed in a multiline **plugin<...plugin>** directive as in the following example:

        .. code-block::
            :emphasize-lines: 1,7

            plugin<
                myInt = 374
                myBool = false
                myString = 'profile.dat'
                myFloat = -1.234e-12
                myVec = [1,4,3]
            plugin>


    .. c:function:: bool getBoolParam(const char *pname,bool defVal)

        :param pname: parameter name
        :type pname: const char *

        :param bool defVal:  default value returned if parameter not found in the input file


        :return: the value of the specified parameter
        :rtype: bool

        ::

            bool verbose = getBoolParam("lPluginVerbose",false);
            if (verbose) cout<<"Plugin verbose mode is switched on."<<endl;

    .. c:function:: int     getIntParam(const char *pname,int defVal)

        :param pname: parameter name
        :type pname: const char *

        :param int defVal:  default value returned if parameter not found in the input file


        :return: the value of the specified parameter
        :rtype: int

        ::

            int nfrac = getIntParam("numFractions",1);
            cout<<"Number of planned fractions: "<<nfrac<<endl;

    .. c:function:: float64 getFloatParam(const char *pname,float64 defVal)

        :param pname: parameter name
        :type pname: const char *

        :param float64 defVal:  default value returned if parameter not found in the input file


        :return: the value of the specified parameter
        :rtype: float64

        ::

            float64 fac = getFloatParam("energyRescaleFactor",1);
            cout<<"Energy rescaling factor: "<<fac<<endl;

    .. c:function:: char *  getStringParam(const char *pname,const char* defStr)

        :param pname: parameter name
        :type pname: const char *

        :param defStr:  default string returned if parameter not found in the input file
        :type pname: const char *


        :return: the string for the specified parameter
        :rtype: char *

        ::

            char * fname = getStringParam("tableFile","");
            if(strlen(fname)) cout<<"Path to table file: "<<fname<<endl;

    .. c:function:: void getVec3dRT(const char *pname,vec3dRT &vec, vec3dRT defVec)

        :param pname: parameter name
        :type pname: const char *

        :param vec:  vector that will be filled with parsed x,y,z components
        :type vec: vec3dRT &


        :param defVec:  default vector if parameter not found in the input file
        :type defVec: vec3dRT


        :return: none

        ::

            vec3dRT psource_position;
            getVec3dRT("sourcePos", &psource_position, vec3dRT(0,0,5));

            cout<<"Point source position: "<<psource_position<<endl;




Step functions
--------------

This class of functions can be used to access particle and medium properties via the opaque structure ``Step`` passed by Fred to the plugin.

- Particle properties

    .. c:function:: void    getPosition_A(Step *stp, vec3dRT &pos)

        returns in ``pos`` the particle position at the beginning of the step

        :param stp: current step structure
        :type stp: Step *

        :param pos:
        :type pos: vec3dRT &

        :return: none

    .. c:function:: void    getPosition_B(Step *stp, vec3dRT &pos)

        returns in ``pos`` the particle position at the end of the step

        :param stp: current step structure
        :type stp: Step *

        :param pos:
        :type pos: vec3dRT &

        :return: none

    .. c:function:: void    getDirection_A(Step *stp, vec3dRT &vel)

        returns in ``vel`` the particle direction at the beginning of the step

        :param stp: current step structure
        :type stp: Step *

        :param vel:
        :type vel: vec3dRT &

        :return: none

    .. c:function:: void    getDirection_B(Step *stp, vec3dRT &vel)

        returns in ``vel`` the particle direction at the end of the step

        :param stp: current step structure
        :type stp: Step *

        :param vel:
        :type vel: vec3dRT &

        :return: none

    .. c:function:: void    setDirection_B(Step *stp, vec3dRT vel)

        sets the particle direction to ``vel`` at the end point `B`

        :param stp: current step structure
        :type stp: Step *

        :param vel:
        :type vel: vec3dRT

        :return: none


    .. c:function:: float64 getKineticEnergy_A(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle kinetic energy in MeV at the initial point `A`
        :rtype: float64


    .. c:function:: float64 getKineticEnergy_B(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle kinetic energy in MeV at the end point `B`
        :rtype: float64

    .. c:function:: void setKineticEnergy_B(Step *stp, float64 T)

        :param stp: current step structure
        :type stp: Step *

        :param float64 T: particle kinetic energy in MeV at point `B`

        :return: none

    .. c:function:: float64 getMomentum_A(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle linear momentum in MeV/c at point `A`
        :rtype: float64

    .. c:function:: float64 getMomentum_B(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle linear momentum in MeV/c at point `B`
        :rtype: float64

    .. c:function:: void setMomentum_B(Step *stp, float64 p)

        :param stp: current step structure
        :type stp: Step *

        :param float64 p: particle linear momentum in MeV/c at point `B`

        :return: none


    .. c:function:: int32 getType(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle numerical ID based on PDG 2006 particle codes, e.g. PROTON = 2212

    .. c:function:: float32 getParticle_m(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle rest mass (MeV/c^2)

    .. c:function:: float32 getParticle_Z(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: electric charge number or atomic number, i.e. number of protons (P)

    .. c:function:: float32 getParticle_A(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: mass number, i.e. number of nucleons (P+N)

....

- Particle family tree

    .. c:function:: int32 getUID(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: particle UID (unique identifier): this number labels each and every particle produced and tracked

    .. c:function:: int32 getParentUID(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: parent UID, i.e. previous generation

    .. c:function:: int32 getAncestorUID(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: ancestor UID, i.e. first generation in the particle family tree


    .. c:function:: int32 getGeneration(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: get particle generation: 1 = primary, 2 = secondary ,...

....

- Step properties

    .. c:function:: float32 getStepLength(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: length of trajectory connecting point A and B of the step

    .. c:function:: float32 getRangeStep(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: column density (g/cm^2) corresponding to current step

    .. c:function:: float32 getMassDensity(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: local mass density of the material in which current step is taken


....

- Random generators attached to current particle

    *to be used if you want a simulation to be reproducible by setting* ``randSeedRoot`` *in the input file*

    .. c:function:: float32 getRandUnif(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: random floating point number uniformly distributed in [0,1)

    .. c:function:: float32 getRandGauss(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: random floating point number sampled from a normal distribution (i.e. average=0, stdev=1)


....

- Energy loss properties of current step

    .. c:function:: float32 get_dEds(Step *stp, float32 T)

        :param stp: current step structure
        :type stp: Step *

        :param float32 T: particle kinetic energy in MeV

        :return: mass stopping power for the particle with kinetic energy T in the current material

    .. c:function:: float32 get_TrackingCutoffEnergy(Step *stp)

        .. versionadded:: 3.0.25

        :param stp: current step structure
        :type stp: Step *

        :return: kinetic cut-off energy for particle transport in the current material


Material properties
-------------------

    The mean properties of a material are queried using:

    .. c:function:: int getImat_A(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: get material index at initial point A
        :rtype: int32

    .. c:function:: int getImat_B(Step *stp)

        :param stp: current step structure
        :type stp: Step *

        :return: get material index at initial point B
        :rtype: int32

    .. c:function:: string getMatID(int imat)

        .. versionadded:: 3.0.24

        :param imat: material index
        :type stp: int32

        :return: material ID, i.e. a string representing its name
        :rtype: string


    .. c:function:: float32 getMat_Zmean(int imat)

        :param imat: material index
        :type stp: int32

        :return: average atomic number <Z>  of the material
        :rtype: float32


    .. c:function:: float32 getMat_Amean(int imat)

        :param imat: material index
        :type stp: int32

        :return: average mass number <A> (g/mol) of the material
        :rtype: float32


    .. c:function:: float32 getMat_RelStopPow(int imat)

        :param imat: material index
        :type stp: int32

        :return: relative stopping power of the material
        :rtype: float32


    .. c:function:: float32 getMat_Lrad(int imat)

        :param imat: material index
        :type stp: int32

        :return: radiation length (g/cm^2) of the material
        :rtype: float32

    .. c:function:: int16 getHU(int imat)

        :param imat: material index
        :type stp: int32

        :param int32 iel: index of element in the material

        :return: HU value of the material (if not defined, returns -10000)
        :rtype: int16



Elemental composition
---------------------

    Query functions for elemental composition:

    .. c:function:: int32 getMatNumElements(int imat)

        :param imat: material index
        :type stp: int32

        :return: number of elements in the material
        :rtype: int32

        single elements in the material are indexed from 0

    .. c:function:: float32 getMat_Z(int imat, int32 iel)

        :param imat: material index
        :type stp: int32

        :param int32 iel: index of element in the material

        :return: num of protons in element nucleus (P)
        :rtype: float32

    .. c:function:: float32 getMat_A(int imat, int32 iel)

        :param imat: material index
        :type stp: int32

        :param int32 iel: index of element in the material

        :return: num of nucleons in element nucleus (N+P)
        :rtype: float32

    .. c:function:: float32 getMat_m(int imat, int32 iel)

        :param imat: material index
        :type stp: int32

        :param int32 iel: index of element in the material

        :return: mass of element nucleus (MeV/c^2)
        :rtype: float32

    .. c:function:: float32 getMat_w(int imat, int32 iel)

        :param imat: material index
        :type stp: int32

        :param int32 iel: index of element in the material

        :return: weight fraction of element in the material
        :rtype: float32

    .. c:function:: float32 getMat_x(int imat, int32 iel)

        :param imat: material index
        :type stp: int32

        :param int32 iel: index of element in the material

        :return: number fraction of element in the material
        :rtype: float32


    Example:

    ::

        int imat = getImat_A(stp);
        int nel = getMatNumElements(imat);
        cout<<endl<<"Number of elements in the material:  "<<nel<<endl;
        for(int iel=0;iel<nel;iel++)
            cout<<iel<<' '<<getMat_Z(imat,iel)<<' '<<getMat_A(imat,iel)<<' '<<getMat_w(imat,iel)<<' '<<getMat_x(imat,iel)<<endl;
        cout<<endl;

Environment subroutines
-----------------------

    .. c:function:: string getInputDirectory()

        :return: path to the current input directory
        :rtype: string


    .. c:function:: string getOutputDirectory()

        :return: path to the current output directory
        :rtype: string

    .. c:function:: string getPluginDirectory()

        :return: path to the directory containing the plugin
        :rtype: string

