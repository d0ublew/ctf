FROM i386/alpine:3.21
EXPOSE 3490 
COPY a.out /
COPY flag.txt /
COPY smallxray.jpg /
RUN chmod +x /a.out

CMD ["/a.out"]
