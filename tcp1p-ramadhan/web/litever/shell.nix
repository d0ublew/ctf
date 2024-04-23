with (import <nixpkgs>{});
(python3.withPackages (ps: with ps; [
    flask
    sqlite
])).env
