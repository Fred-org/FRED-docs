import os
import numpy as np
import SimpleITK as sitk
########################################################################
Lx = 200 ; Ly = 200 ; Lz = 200 # extent (mm)
nx = 200 ; ny = 200 ; nz = 200 # voxels
hx = Lx/nx ; hy = Ly/ny ; hz = Lz/nz # spacing

print('extent',Lx,Ly,Lz,'mm')
print('voxels',nx,ny,nz,'#')
print('spacing',hx,hy,hz,'mm')

# center voxel coords
x = np.linspace(-Lx/2,+Lx/2,nx,endpoint=False)+hx/2
y = np.linspace(-Ly/2,+Ly/2,ny,endpoint=False)+hy/2
z = np.linspace(-Lz/2,+Lz/2,nz,endpoint=False)+hz/2

zv, yv, xv = np.meshgrid(z,y,x,indexing='ij')

# CT map corresponding to HU=0 value
CT = np.zeros((nz,ny,nx),dtype=np.int16)
img = sitk.GetImageFromArray(CT)
img.SetSpacing((hx,hy,hz))
img.SetOrigin((x[0],y[0],z[0]))
sitk.WriteImage(img,'CT.mha')

# ROI of a sphere with 8 cm radius
ROI = np.zeros_like(CT)
ROI[xv**2+yv**2+zv**2<80**2]=1
img = sitk.GetImageFromArray(ROI)
img.SetSpacing((hx,hy,hz))
img.SetOrigin((x[0],y[0],z[0]))
sitk.WriteImage(img,'Sphere8cm.mha')

# ROI of a sphere with 7 cm radius
ROI = np.zeros_like(CT)
ROI[xv**2+yv**2+zv**2<70**2]=1
img = sitk.GetImageFromArray(ROI)
img.SetSpacing((hx,hy,hz))
img.SetOrigin((x[0],y[0],z[0]))
sitk.WriteImage(img,'Sphere7cm.mha')
