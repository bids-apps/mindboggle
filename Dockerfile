FROM nipy/mindboggle
# MAINTAINER Mindboggle <anishakeshavan@gmail.com>
USER root
RUN mkdir -p /opt/bids-mindboggle/
COPY run.py /opt/bids-mindboggle/run.py
COPY version /opt/bids-mindboggle/version
ENTRYPOINT ["python", "/opt/bids-mindboggle/run.py"]
