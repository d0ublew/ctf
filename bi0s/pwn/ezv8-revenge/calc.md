# Calculations

- For array of length `n` with two floating numbers, the final size of the array
elements after conversion is `n * 4 + 2 * 12`.
- The victim array object would be allocated next to the previous array elements
  and the `length` field would be at offset `n*4+2*12+12`
- The new elements will be pushed at offset `(n-1) * 8`

So, `(n-1) * 8 == n * 4 + 36` and `n = 11`


`(n-1) * 8 == n * 4 + (x+1) * 12`
`4n = 12x + 20`

For `n = 5`, `x = 0` (not ideal, need at least one floating numbers)

Solution:
- `n = 8`, `x = 1`
- `n = 11`, `x = 2`
- `n = 14`, `x = 3`
- `n = 17`, `x = 4`
