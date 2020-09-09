Physics Control
=================================

TODO

IonizPotential=80
stoppowPathlengthCutoff=0.00055

lTracking_nuc_el [t]  enable nuclear elastic interactions
lTracking_nuc_inel [t]  enable nuclear inelastic interactions
lTracking_nuc [t]  enable all nuclear interactions


lTracking_fluc [t]  enable energy straggling

lTracking_mcs [t]  enable MCS

mcsMode [6]  switch MCS mode:
         0 = single gaussian distribution based on Highland's formula (1G-H);
         1 = single gaussian distribution using tabulated values (1G);
         2 = double gaussian distribution using tabulated values (2G);
         3 = triple gaussian distribution using tabulated values (3G);
         4 = gaussian distribution + 2 rutherford-like tails using tabulated values (G2R);
         5 = double gaussian distribution + rutherford-like tail using tabulated values (2GR);
         6 = single effective gaussian distribution: Rossi-Greisen formula + correction a' la Fippel (1G-RGF);
