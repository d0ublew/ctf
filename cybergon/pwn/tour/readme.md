# Notes

- ride a plane allow us to invoke function pointer
- this function pointer last byte could be overwritten by `load_luggage` off-by-one error, the check `if x > 8` happens after we copied the 9th byte
- with this, we can overwrite the function pointer from `yangon` address to `mandalay` address since they only differ within 256 byte range
- `mandalay` then calls `thunderstorm` which then calls `ticket_number` which then calls `boarding_pass`
- inside `thunderstorm`, we need to supply a `QWORD` integer value that is not 0 to call `ticket_number`
- inside `ticket_number`, the previous integer value is casted to `DWORD` integer value and if it is 0, it calls `boarding_pass`
- after `boarding_pass` is called, we can attempt to answer questions and earn money to buy a plane, which allow us to fully control the function pointer value
