import numpy as np

from simple_3dviz.renderables import Mesh
from simple_3dviz.behaviours.misc import LightToCamera
from simple_3dviz.window import show

import argparse

parser = argparse.ArgumentParser(description='View *.raw files.')
parser.add_argument('-f', action="store", dest="rawfile", help='*.raw file')
parser.add_argument('-c', action="store", dest="cfgfile", help='*.txt file with size info')
args = parser.parse_args()

if __name__ == "__main__":
    f = open(args.cfgfile, "r")
    first_line = f.readline().split()
    f.close()

    assert(len(first_line) > 3)
    reso = []
    for i in (1,2,3):
        reso.append(int(first_line[i]))
    wx,wy,wz = reso
    longest_axis = max(reso)

    arr_vox = np.fromfile(args.rawfile, dtype=np.uint8).astype(np.bool)
    arr_vox_3d = np.reshape(arr_vox, (wx,wy,wz), order='F')

    # bug in simple_3dviz, the spacing is not uniform if the voxel array is not uniform
    arr_vox_3d = np.concatenate((arr_vox_3d, np.zeros((longest_axis-wx, wy, wz), dtype=np.bool)), axis=0)
    arr_vox_3d = np.concatenate((arr_vox_3d, np.zeros((longest_axis, longest_axis-wy, wz), dtype=np.bool)), axis=1)
    arr_vox_3d = np.concatenate((arr_vox_3d, np.zeros((longest_axis, longest_axis, longest_axis-wz), dtype=np.bool)), axis=2)

    half_edge = ((1/longest_axis)*0.5, (1/longest_axis)*0.5, (1/longest_axis)*0.5)

    show(
        Mesh.from_voxel_grid(voxels=arr_vox_3d, colors=(0.75,0.75,0.75), sizes=half_edge),
        behaviours=[LightToCamera()],
        size=(1024, 1024)
    )