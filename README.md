# mindboggle

[![Build Status](https://circleci.com/gh/BIDS-Apps/mindboggle.png?circle-token=:d4d232bd9d9bcf925155774e1b2d24cdc365bd19)](https://circleci.com/gh/BIDS-Apps/mindboggle)  

## Description 

The Mindboggle project's mission is to improve the accuracy, precision, and consistency of automated labeling and shape analysis of human brain image data. We promote open science by making all software, data, and documentation freely and openly available. For more information on mindboggle, check out the [mindboggle website](http://mindboggle.readthedocs.io/en/latest/#preprocessing)

## Docker 

To pull the docker image from Docker Hub, do 

```
docker pull bids/mindboggle
```

To run the docker, do:

```
docker run -ti -v $PWD/ds114_test1:/home/jovyan/work/data bids/mindboggle /home/jovyan/work/data /home/jovyan/work/data participant
```

Its important to mount to a directory in `/home/jovyan/` because you are not root in this Docker image.

To use bash:

```
 docker run -ti -v /Users/keshavan/Downloads/mindboggle_input_example/bids:/home/jovyan/work/data --entrypoint /bin/bash bids/mindboggle 
```

For developers, you can make changes to the Dockerfile, and build the docker image, by running

```
docker build -t bids/mindboggle .
```

## Acknowledgements

When using this app, please cite:

```
101 labeled brain images and a consistent human cortical labeling protocol.
Arno Klein, Jason Tourville. 2012. Frontiers in Brain Imaging Methods.
6:171. DOI: 10.3389/fnins.2012.00171
```


## Error Reporting

Please report errors on the Issues page of this repository.
