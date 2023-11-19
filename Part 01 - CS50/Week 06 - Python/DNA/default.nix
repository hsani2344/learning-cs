with import <nixpkgs> {};

let
  pythonEnv = python3.withPackages (ps: with ps; [
  # Any python pkgs
  # dbus-python
  ]);
in mkShell {
  packages = [
    pythonEnv
  ];
}
