# with (import <nixpkgs>{});
# mkShell {
#     buildInputs = [
#         (python3.withPackages (ps: with ps; [
#             gmpy2
#             pycryptodome
#         ]))
#         gdb
#     ];
# }

with (import <nixpkgs>{});
(python3.withPackages (ps: with ps; [
    gmpy2
    pycryptodome
])).env
