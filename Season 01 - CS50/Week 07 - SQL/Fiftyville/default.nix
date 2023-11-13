with import <nixpkgs> {};

let
  sqlEnv = sqlite;
in mkShell {
  packages = [
    sqlEnv
  ];
}
