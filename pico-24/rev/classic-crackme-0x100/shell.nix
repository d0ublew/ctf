
with (import <nixpkgs> {});
let
    my-pypkgs = pypkgs: with pypkgs; [
        angr
        z3
    ];
    my-python = python3.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
        gdb
    ];
}
