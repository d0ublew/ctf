# Note

there is a bug on `send_mail`, where the length value for `FROM` tag uses the
mail recipient username length but the data itself uses the mail sender username

```c
    print_tlv(TAG_INPUT_REQ, "username");
    read_taglen(stdin, &tl);
    unsigned long t1 = tl.len;
    if (tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "invalid username input");
        return;
    }
    fread(tmpbuf, 1, tl.len, stdin);

    ... // code is abbreviated for brevity

    // tl.len = len(recipient)
    pack_taglen(TAG_STR_FROM, tl.len, tmpbuf + USERPASS_LEN);
    // writes FROM tag to recipient file
    fwrite(tmpbuf + USERPASS_LEN, 1, 12, fp); // !!!
    // writes username to recipient file
    fwrite(tmpbuf, 1, t1, fp); // t1 = len(username)
    // Mismatch, the tag uses the `recipient` length but it writes `username`
    // length bytes of data
```

## Getting Memory Leak

Let the recipient username length be `x` and sender username length be `y`
If `x > y`, when `view_mail` parses the data, it reads `x` bytes and then
expect a `MESSAGE` tag. After it reads `x` bytes, due to `x > y`, the pointer is
now in the middle of the message data. Thus, if we carefully craft our message
such that inside the message contains another message `taglen_t`, this tag would
be used to read the next data.

If this `taglen_t` is crafted such that the length field is `0x400`, this would
cause the program to leak memory data. We could only do maximum of `0x400`
since there is still validation check to not exceed `USERPASS_LEN + MESSAGE_LEN`

Let our original message is of length `z` and `z = 0x3ff`. If our pointer has
passed through `n = 0x80` bytes of our original message data, this means for
subsequent bytes of `z - n = 0x3ff - 0x80 = 0x37f` is our message data and the
program would leak out `0x400 - 0x37f` bytes of data.

## Buffer Overflow

Let us invert our previous scenario. Instead of the recipient username length
(`x`) is bigger than the sender username length (`y`), let us see the scenario
when `x < y`.

When `view_mail` parses the data, it would read `x` bytes of data and then
expect a `MESSAGE` tag. However, since `x < y`, the next bytes are still the
sender username data. Thus, we could embed a fake `MESSAGE` data inside the
sender username.

```c
    // Parse the sender data
    read_taglen(fp, &tl);
    if (feof(fp)) {
        print_tlv(TAG_RES_MSG, "no mail");
        return;
    }
    // t1 is the recipient username length (`x`)
    unsigned long t1 = tl.len;
    if (tl.tag != TAG_STR_FROM || t1 >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "mail invalid from");
        return;
    }
    memcpy(tmpbuf, "from: ", 6);
    fread(tmpbuf + 6, 1, t1, fp);
    tmpbuf[6 + t1] = '\n';

    // Parse the message data
    read_taglen(fp, &tl);
    // t2 is the message data length
    unsigned long t2 = tl.len;
    if (tl.tag != TAG_STR_MESSAGE || (t1 + t2) >= USERPASS_LEN + MESSAGE_LEN) {
        print_tlv(TAG_RES_ERROR, "mail invalid message");
        return;
    }
    memcpy(tmpbuf + 6 + t1 + 1, "message: ", 9);
    fread(tmpbuf + 6 + t1 + 1 + 9, 1, t2, fp);
```

Notice that when viewing mail, the message length is validated together with
the recipient username length. Since we have control over `t1` and `t2`,
if we make `t1` as small as possible, i.e., `1`, we could have a fake message
length of `0xffffffffffffffff`, such that when it is added, it overflows into
`0` and `0` is less than `USERPASS_LEN + MESSAGE_LEN`, thus passes the check.

With a very large `t2` value, the following `fread(buf, 1 t2, fp)` would
try to populate `buf` with as many bytes as possible from the `fp` stream.
Since `buf` is a variable on the stack, we could get buffer overflow.
