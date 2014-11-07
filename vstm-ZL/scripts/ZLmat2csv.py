from scipy import io as sio
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description="Converts raw .mat outputs to csv.  Looks for .mat extension in folder")
parser.add_argument('fold', type=str, help='folder containing .mat files')
parser.add_argument('out', type=str, help='output folder name')
args = parser.parse_args()

def mat2csv(matfile, outfile, N):
    """Saves parts of mat file to csv.  Uses certain predefined hdr values."""
    M = sio.loadmat(matfile)
    base, ext = os.path.splitext(matfile)
    fname = os.path.split(base)[1]
    hdr = ['probedcolor', 'binResponse', 'setsize']
    M_out = np.array([M['data'][ii][0][0].flatten()[:N] for ii in hdr]).T
    outf = os.path.join('data/csv', fname)
    np.savetxt(outf, M_out,'%i, %i, %i')

fold = args.fold
out = args.out
for fname in os.listdir(fold):
    print fname
    if fname[-4:] == '.mat': mat2csv(os.path.join(fold, fname), os.path.join(out, fname), N = 300)
