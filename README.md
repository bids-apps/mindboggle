# mindboggle

[![Build Status](https://circleci.com/gh/BIDS-Apps/mindboggle.png?circle-token=:d4d232bd9d9bcf925155774e1b2d24cdc365bd19)](https://circleci.com/gh/BIDS-Apps/mindboggle)  


This app assumes freesurfer and ants cortical thickness have already run. 
For more instructions, see the [mindboggle website](http://mindboggle.readthedocs.io/en/latest/#preprocessing)

The folder structure of the mindboggle input should look like:
```
bids_dir/
  sub01/
    sess-*/
      anat/
        T1w.nii.gz
      
  derivatives/
    freesurfer/
      sub-*_ses-*_T1w.nii.gz/
        mri/ 
        label/
        surf/
    ants/
      sub-*_ses-*_T1w.nii.gz/
        antsBrainExtractionMask.nii.gz		
        antsSubjectToTemplate0GenericAffine.mat	
        antsTemplateToSubject0Warp.nii.gz
        antsBrainSegmentation.nii.gz		
        antsSubjectToTemplate1Warp.nii.gz	
        antsTemplateToSubject1GenericAffine.mat
```

To build to docker, do

```
docker build -t bids/mindboggle .
```

To run the docker, do

```
 docker run -ti -v /path/to/bids_dir:/root/data bids/mindboggle /root/data /root/data/ participant
```

To use bash:

```
 docker run -ti -v /Users/keshavan/Downloads/mindboggle_input_example/bids:/root/data --entrypoint /bin/bash bids/mindboggle 
```
