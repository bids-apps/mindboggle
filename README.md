# mindboggle

[![Build Status](https://circleci.com/gh/BIDS-Apps/mindboggle.png?circle-token=:d4d232bd9d9bcf925155774e1b2d24cdc365bd19)](https://circleci.com/gh/BIDS-Apps/mindboggle)  


This app assumes the freesurfer BIDS-App has been run. 
For more information on mindboggle, see the [mindboggle website](http://mindboggle.readthedocs.io/en/latest/#preprocessing)

The folder structure of the mindboggle input should look like:
```
bids_dir/
  sub01/
    sess-*/
      anat/
        T1w.nii.gz
      
  derivatives/
    freesurfer/
      sub-*/
        mri/ 
        label/
        surf/
```

To build the docker image, do

```
docker build -t bids/mindboggle .
```

To run the docker, do

```
 docker run -ti -v /path/to/bids_dir:/root/data bids/mindboggle /root/input /root/output/ participant
```

To use bash:

```
 docker run -ti -v /Users/keshavan/Downloads/mindboggle_input_example/bids:/root/data --entrypoint /bin/bash bids/mindboggle 
```
