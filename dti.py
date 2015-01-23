import os.path as op
import json

import numpy as np
import nibabel as nib
import dipy.reconst.dti as dti
from dipy.io.utils import nifti1_symmat
import dipy.core.gradients as grad

def dipysave(img, filename):
    """Some DTI/tools require the qform code to be 1. We set the affine, qform,
    and sfrom to be the same for maximum portability.
    """
    affine = img.get_affine()
    img.set_sform(affine, 1)
    img.set_qform(affine, 1)
    nib.save(img, filename)


#fmetadata = "/input/metadata.json"
fmetadata = "/Users/arokem/tmp/metadata.json"

# Fetch metadata:
metadata = json.load(open(fmetadata))
fdata, fbval, fbvec = [metadata[k] for k in ["fdata", "fbval", "fbvec"]]

# Load the data:
img = nib.load(str(fdata))
gtab = grad.gradient_table(str(fbval), str(fbvec))
data = img.get_data()
affine = img.get_affine()

# Fit the model:
tenmodel = dti.TensorModel(gtab)
tenfit = tenmodel.fit(data)

# Extract the nifti convention parameters:
lower_triangular = tenfit.lower_triangular()
lower_triangular = lower_triangular.astype('float32')
tensor_img = nifti1_symmat(lower_triangular, affine)

root = op.join("/output/")

# Save to file:
dipysave(tensor_img, root+'_tensor.nii.gz')
dipysave(nib.Nifti1Image(ten.ad.astype("float32"), affine), root+'_ad.nii.gz')
dipysave(nib.Nifti1Image(ten.rd.astype("float32"), affine), root+'_rd.nii.gz')
dipysave(nib.Nifti1Image(ten.md.astype("float32"), affine), root+'_md.nii.gz')
dipysave(nib.Nifti1Image(ten.fa.astype("float32"), affine), root+'_fa.nii.gz')


FA = fractional_anisotropy(tenfit.evals)
FA[np.isnan(FA)] = 0
fa_img = nib.Nifti1Image(FA.astype(np.float32), img.get_affine())
nib.save(fa_img, 'tensor_fa.nii.gz')
evecs_img = nib.Nifti1Image(tenfit.evecs.astype(np.float32),
                            img.get_affine())
nib.save(evecs_img, 'tensor_evecs.nii.gz')
MD = tenfit.md
nib.save(nib.Nifti1Image(MD.astype(np.float32),
                         img.get_affine()), 'tensors_md.nii.gz')

