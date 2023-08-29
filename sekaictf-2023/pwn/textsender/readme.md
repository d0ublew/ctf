# Note

- off-by-null vuln on `input()` used on `add_message()` and `edit_message()`
- `add_message()`:
  - input for `receiver` allow us to overwrite 1 byte of `message` chunk size metadata

- `edit_message()`:
  - input for new message allow us to overwrite 1 byte of `text` chunk size metadata
