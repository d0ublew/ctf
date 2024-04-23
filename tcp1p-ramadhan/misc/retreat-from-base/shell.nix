with (import <nixpkgs> {});
mkShell {
    buildInputs = [
        python3Packages.venvShellHook
    ];
    venvDir = "venv";
}
