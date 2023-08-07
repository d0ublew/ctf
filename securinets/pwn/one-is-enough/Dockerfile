FROM ubuntu AS app

RUN useradd -p ctf ctf
RUN echo "ctf:ctf" | chpasswd

RUN mkdir /app
WORKDIR /app

COPY main .
COPY ynetd .
COPY flag.txt .

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y gdb

COPY run.sh .

USER ctf
CMD ./ynetd -p 5000 ./run.sh
