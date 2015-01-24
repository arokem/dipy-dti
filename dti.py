#!/usr/bin/env python 

import os.path as op
import json

import numpy as np
import nibabel as nib
import dipy.reconst.dti as dti
from dipy.io.utils import nifti1_symmat
import dipy.core.gradients as grad

def dpsave(img, filename):
    """
    Some tools require the qform code to be 1. We set the affine, qform,
    and sfrom to be the same for maximum portability.
    """
    affine = img.get_affine()
    img.set_sform(affine, 1)
    img.set_qform(affine, 1)
    nib.save(img, filename)


if __name__=="__main__":
    fmetadata = "/input/metadata.json"
    # Fetch metadata:
    metadata = json.load(open(fmetadata))
    fdata, fbval, fbvec = [metadata[k] for k in ["fdata", "fbval", "fbvec"]]

    # Load the data:
    img = nib.load(op.join('/input', str(fdata)))
    gtab = grad.gradient_table(op.join('/input', str(fbval)),
                               op.join('/input', str(fbvec)))
    data = img.get_data()
    affine = img.get_affine()

    # Get the optional params:
    if not metadata.haskey('fit_method'):
        fit_method = "WLS"
    else:
        fit_method = metadata['fit_method']

    if not metadata.haskey('fmask'):
        mask = None
    else:
        mask = nib.load(metadata['fmask']).get_data().astype(bool)

    # Fit the model:
    tenmodel = dti.TensorModel(gtab, fit_method=fit_method, mask=mask)
    tenfit = tenmodel.fit(data)

    # Extract the nifti convention parameters:
    lower_triangular = tenfit.lower_triangular()
    lower_triangular = lower_triangular.astype('float32')
    tensor_img = nifti1_symmat(lower_triangular, affine)

    # The output will all have the same basic name as the data file-name:
    root = op.join("/output",
                   op.splitext(op.splitext(op.split(fdata)[-1])[0])[0])
    
    # Save to file:
    dpsave(tensor_img, root + '_tensor.nii.gz')
    for arr, label in zip([tenfit.ad, tenfit.rd, tenfit.md, tenfit.fa],
                          ["_ad", "_rd", "_md", "_fa"]):
        dpsave(nib.Nifti1Image(arr.astype("float32"), affine),
               op.join('/output/', root + '%s.nii.gz'%label))
