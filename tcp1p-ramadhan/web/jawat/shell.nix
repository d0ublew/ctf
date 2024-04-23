with (import <nixpkgs>{});
let
    my-pypkgs = pypkgs: with pypkgs; [
        pyjwt
    ];
    my-python = python3.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
    ];
}
