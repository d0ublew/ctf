FROM ubuntu@sha256:0bced47fffa3361afa981854fcabcd4577cd43cebbb808cea2b1f33a3dd7f508

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
WORKDIR /home/ctf

COPY services .
COPY flag .

COPY libseccomp.so.2 .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .

RUN mkdir ./chat
COPY chat ./chat

COPY ynetd .

RUN chmod 777 ./ynetd
RUN chown -R ctf:ctf /home/ctf

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y gdb ruby
RUN gem install one_gadget
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y wget python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y binutils file
RUN wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/py && echo source ~/.gdbinit-gef.py >> ~/.gdbinit

USER ctf
CMD ./ynetd -p 1234 ./services 2>/dev/null
