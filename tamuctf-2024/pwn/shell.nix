with (import <nixpkgs> {});
let
    my-pypkgs = pypkgs: with pypkgs; [
        pwntools
        tqdm
    ];
    my-python = python3.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
        gdb
        pwninit
        one_gadget
        strace
    ];
}
