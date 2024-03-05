with (import <nixpkgs> {});
let
    my-pypkgs = pypkgs: with pypkgs; [
        pip
    ];
    my-python = python3.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
        python3Packages.venvShellHook
        # jq
        # solc
        # fx
        # jless
    ];
    venvDir = "venv";
}
