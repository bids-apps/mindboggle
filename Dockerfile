FROM ubuntu:vivid
MAINTAINER Mindboggle <anishakeshavan@gmail.com>

# Preparations
RUN ln -snf /bin/bash /bin/sh
ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install the minimal set of tools
RUN apt-get update && \
    apt-get install -y curl \
                       git \
                       xvfb \
                       bzip2 \
                       unzip \
                       apt-utils \
                       gfortran \
                       fusefat \
                       liblapack-dev \
                       libblas-dev \
                       libatlas-dev \
                       libatlas-base-dev \
                       libblas3 \
                       libblas-common \
                       libopenblas-dev \
                       libxml2-dev \
                       libxslt1-dev \
                       libfreetype6-dev \
                       libpng12-dev \
                       libqhull-dev \
                       libxft-dev \
                       libjpeg-dev \
                       libyaml-dev \
                       graphviz




# Enable neurodebian
RUN curl -sSL http://neuro.debian.net/lists/vivid.de-m.full | tee /etc/apt/sources.list.d/neurodebian.sources.list && \
    curl -sSL http://neuro.debian.net/lists/vivid.us-tn.full >> /etc/apt/sources.list.d/neurodebian.sources.list && \
    apt-key adv --recv-keys --keyserver hkp://pgp.mit.edu:80 0xA5D32F012649A5A9 && \
    apt-get update #&& \

# Clear apt cache to reduce image size
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Preparations
RUN ln -snf /bin/bash /bin/sh
WORKDIR /root

# Install miniconda
RUN curl -sSLO https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash Miniconda3-latest-Linux-x86_64.sh -b -p /usr/local/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    echo '#!/bin/bash' >> /etc/profile.d/nipype.sh && \
    echo 'export PATH=/usr/local/miniconda/bin:$PATH' >> /etc/profile.d/nipype.sh

ENV PATH /usr/local/miniconda/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# Add conda-forge channel in conda
RUN conda config --add channels conda-forge

RUN conda install nipype
RUN conda install -c https://conda.anaconda.org/clinicalgraphics vtk cmake
RUN git clone https://github.com/binarybottle/mindboggle
RUN cd mindboggle && \
    python setup.py install

ENV CONDA_PATH "/usr/local/miniconda/"
ENV VTK_DIR "$CONDA_PATH/lib/cmake/vtk-7.0"
ENV vtk_cpp_tools "/root/mindboggle/vtk_cpp_tools/bin"

RUN mkdir $vtk_cpp_tools && \
    cd $vtk_cpp_tools && \
    cmake ../ -DVTK_DIR:STRING=$VTK_DIR && \
    make


RUN mkdir ${HOME}/data

RUN mkdir /code
COPY run.py /code/run.py

RUN echo "export vtk_cpp_tools=$vtk_cpp_tools" >> /etc/profile.d/nipype.sh
RUN echo "export PATH=$vtk_cpp_tools:\$PATH" >> /etc/profile.d/nipype.sh
RUN echo "source /etc/profile.d/nipype.sh" >> /etc/bash.bashrc

ENTRYPOINT ["/code/run.py"]
