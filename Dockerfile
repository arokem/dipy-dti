FROM arokem/dipy

RUN apt-get update
RUN apt-get install -y ipython ipython-notebook
RUN luarocks install itorch

ADD /input /input
ADD /output /output
WORKDIR /workspace
ADD dti.py /dti.py
RUN chmod a+x /dti.py

CMD ["/dti.py"]

