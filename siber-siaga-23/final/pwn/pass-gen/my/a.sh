docker build -t siber .

docker run -it --rm --entrypoint sh --name pwn siber


docker cp pwn:/lib/x86_64-linux-gnu/libc-2.27.so
