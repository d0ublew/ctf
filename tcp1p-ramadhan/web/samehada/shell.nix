with (import <nixpkgs> {});
let
    my-pypkgs = pypkgs: with pypkgs; [
        pip
        pyjwt
        requests
        pyyaml
    ];
    my-python = python3.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
        # python3Packages.venvShellHook
    ];
    # venvDir = "venv";
}
