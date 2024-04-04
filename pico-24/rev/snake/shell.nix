
with (import <nixpkgs> {});
let
    my-pypkgs = pypkgs: with pypkgs; [
        # pip
    ];
    my-python = python39.withPackages my-pypkgs;
in
mkShell {
    buildInputs = [
        my-python
        # python3Packages.venvShellHook
    ];
    # venvDir = "venv";
}
