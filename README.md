## `dipy-dti`

This container calculates DTI parameters, based on diffusion MRI data.

Parameters
---------

fdata : str
   The name of a nifti file with preprocessed diffusion data.

fbval : str
   The name of a text-file with b-values in FSL format.

fbvec : str
    The name of a text file with the b-vectors in FSL format.

fmask : str, optional
    The name of a nifti file containing boolean mask of locations to
   analyze. Default: no masking

fit_method: str, optional
    Chooses the algorithm to use in fitting: {"WLS" | "OLS" | "NNLS" |
   "RESTORE"}. Default: "WLS", which uses weighted least-squares (see [1]_ for
   details). Choosing "RESTORE" will use an automated outlier-rejection
   algorithm [2]_

.. [1] Comparison of bootstrap approaches for estimation of uncertainties of
   DTI parameters. S. Chung, Y. Lu, H.G. Roland (2006). Neuroimage 33: 531-541.

.. [2] L.-C. Chang, D.K. Jones, C. Pierpaoli (2005). RESTORE: Robust estimation
   of tensors by outlier rejection. MRM 53: 1088-1095 
   
Metadata
--------
The mounted `input` folder should contain a `metadata.json` file with the following
format:

    {
    "fdata":"HARDI150.nii.gz",
    "fbval":"HARDI150.bval",
    "fbvec":"HARDI150.bvec",
    "fmask":"mask.nii.gz",
    "fit_method":"WLS"
    }

Where `fdata` and `fit_method` are both optional.

Returns
-------
`root_tensor.nii.gz` : file
    A nifti file containing the 6 lower diagonal in the Nifti1 asymm format
    (see `dipy.io.utils` and
    http://nifti.nimh.nih.gov/pub/dist/src/niftilib/nifti1.h)

`root_{fa,md,ad,rd}`: files
   Nifti files containing the FA, Mean, Axial and Radial diffusivity, respectively.

Examples
-------
To run this container use:

    docker run --rm -it -v /path/to/data:/input -v /path/to/output/:/output arokem/dipy-dti

Where the folder `/path/to/data/` should contain the `metadata.json` file,

Notes
-----
This uses the `dipy.reconst.dti` module: http://nipy.org/dipy/reference/dipy.reconst.html#module-dipy.reconst.dti
