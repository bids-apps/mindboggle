FROM nipy/mindboggle
MAINTAINER Mindboggle <anishakeshavan@gmail.com>
RUN mkdir ~/code
COPY run.py ~/code/run.py
COPY version ~/code/version
ENTRYPOINT ["~/code/run.py"]
