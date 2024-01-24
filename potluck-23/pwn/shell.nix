{ pkgs? import <nixpkgs> {} }:
let
    my-pypkgs = pypkgs: with pypkgs; [
        pwntools
    ];
    my-python = pkgs.python3.withPackages my-pypkgs;
in
pkgs.mkShell {
    buildInputs = [
        my-python
        pkgs.one_gadget
        pkgs.gdb
        pkgs.pwninit
        pkgs.strace
        pkgs.ltrace
    ];
}
