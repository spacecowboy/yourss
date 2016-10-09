FROM python:3.6

RUN apt-get update -qq && \
    apt-get install -qy libav-tools make && \
    rm -rf /var/lib/apt/lists/*

COPY hugo_0.17-64bit.deb /tmp/hugo_0.17-64bit.deb

RUN dpkg -i /tmp/hugo_0.17-64bit.deb

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /work

COPY site /work/site

COPY bin /work/bin

WORKDIR /work

ENTRYPOINT ["bin/run.sh"]
