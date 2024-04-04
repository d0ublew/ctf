with (import <nixpkgs> {});
mkShell {
    buildInputs = [
        pypy310
    ];
}
