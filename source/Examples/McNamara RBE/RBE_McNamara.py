#!/usr/bin/env python3
########################################################################
########################################################################
# Fred project
# Mar 2020 aschiavi : compute McNamara RBE and bioDose
# Mar 2024 aschiavi : ported to SimpleITK
########################################################################
########################################################################
import argparse
parser = argparse.ArgumentParser(description='computes RBE and bioDose using McNamara model')
parser.add_argument("dose",help="dose map file",metavar='Dose')
parser.add_argument("LETd",help="LETd map file",metavar='LETd')
args = parser.parse_args()
########################################################################
########################################################################
import SimpleITK as sitk
import numpy as np
from math import *
import os

########################################################################
########################################################################
########################################################################
# compute the RBE and the biological Dose using model and values from the paper:
# McNamara AL, Schuemann J, Paganetti H, 
# A phenomenological relative biological effectiveness (RBE) model for proton therapy based on all published in vitro cell survival data.
# Phys Med Biol. 60 8399-416 (2015)
########################################################################
########################################################################
########################################################################

# photon parameters
alphaX= 0.0722
betaX=  0.0502

# McNamara parameters
p0=     0.99064
p1=     0.35605
p2=     1.1012
p3=     -0.0038703

# load maps
imgDose = sitk.ReadImage(args.dose) or die
imgLETd = sitk.ReadImage(args.LETd) or die
# get arrays
D     = sitk.GetArrayFromImage(imgDose)
LETd  = sitk.GetArrayFromImage(imgLETd)


# compute alpha and beta
abX = alphaX/betaX
alpha = alphaX*(p0+p1/abX*LETd*0.1)
beta = (p2 + p3 * sqrt(abX) * LETd*0.1)*(p2 + p3 * sqrt(abX) * LETd*0.1)*betaX

rbemax = p0 +  p1 / abX * LETd*0.1
rbemin = p2 + p3 * sqrt(abX) * LETd*0.1

alpha=rbemax*alphaX
beta=rbemin*rbemin*betaX


# compute RBE
RBE = (np.sqrt(abX*abX+4*abX*rbemax*D+4*rbemin*rbemin*D*D)-abX)*0.5
Idx = np.where(D>0)
RBE[Idx] /= D[Idx]

# asymptotic expansion for low dose regions
Idx = np.where(D<1e-4)
RBE[Idx] = alpha[Idx]/alphaX + beta[Idx]/alphaX*D[Idx]

# compute biological Dose
bioDose = D*RBE

# clean up arrays
Idx = np.where(D<=0)
alpha[Idx]=0
beta[Idx]=0
RBE[Idx]=0
bioDose[Idx]=0

# output maps
img = sitk.GetImageFromArray(alpha)
img.SetSpacing(imgDose.GetSpacing())
img.SetDirection(imgDose.GetDirection())
img.SetOrigin(imgDose.GetOrigin())
sitk.WriteImage(img,'alpha.mha')

img = sitk.GetImageFromArray(beta)
img.SetSpacing(imgDose.GetSpacing())
img.SetDirection(imgDose.GetDirection())
img.SetOrigin(imgDose.GetOrigin())
sitk.WriteImage(img,'beta.mha')

img = sitk.GetImageFromArray(RBE)
img.SetSpacing(imgDose.GetSpacing())
img.SetDirection(imgDose.GetDirection())
img.SetOrigin(imgDose.GetOrigin())
sitk.WriteImage(img,'RBE.mha')

img = sitk.GetImageFromArray(bioDose)
img.SetSpacing(imgDose.GetSpacing())
img.SetDirection(imgDose.GetDirection())
img.SetOrigin(imgDose.GetOrigin())
sitk.WriteImage(img,'DoseBio.mha')
