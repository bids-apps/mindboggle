FROM nipy/mindboggle
MAINTAINER Mindboggle <anishakeshavan@gmail.com>
RUN mkdir ~/code
COPY run.py ~/code/run.py
ENTRYPOINT ["~/code/run.py"]
