# Given code
my_string = "My_Strings"
my_result = ""

for i in range(0, len(my_string), 2):
    my_first_letter = ord(my_string[i]) << 8
    my_second_letter = ord(my_string[i + 1])
    my_final = chr(my_first_letter + my_second_letter)
    my_result += my_final

print(my_result)

# My code
# the random characters given from the chall description
# based on trial-and-error, I found out that when `chr()` is given number
# bigger than normal ascii range (utf-8) it tries to encode it with
# different encoding and from the code above it basically combines two
# ascii character into one so it becomes a 16-byte character, hence utf-16
my_string = "杯桵湩歬㈰㈳筎ㅣ敟剥癥牳ㅮ杽".encode('utf-16')

# notice that there are extra bytes identifier like \xff and \xfe for utf-16
flag = my_string.replace(b"\xff", b"").replace(b"\xfe", b"")
final_flag = bytearray()

# rearrange back
for i in range(0, len(flag), 2):
    final_flag.append(flag[i + 1])
    final_flag.append(flag[i])

print(bytes(final_flag))
