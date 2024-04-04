FROM ubuntu:22.04

WORKDIR /chall
ADD game .

RUN apt-get update
RUN apt-get install -y gdbserver gcc-multilib
