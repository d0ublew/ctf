# solution

coordinate: (95, 313)

From [this picture](./snippet.png), after going through debugger, `lParam` has the `x` coordinate, while `SHIWORD(lParam)` has the `y` coordinate
Our `x` coordinate is checked whether it is equal to `dword_412004 % dword_413280`, where the former variable can be found [here](./data.png) while the latter is equal to `741` (max width)
Then, our `y` coordinate is checked again with different value that is `mod` with `641` (max height)
