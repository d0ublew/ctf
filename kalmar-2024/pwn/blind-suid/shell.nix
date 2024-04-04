with (import <nixpkgs> {});
let
    my-pypkgs = pypkgs: with pypkgs; [
        pwntools
        angr
    ];
    my-python = python3.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
        gdb
        hashcash
        strace
        ltrace
    ];
}
