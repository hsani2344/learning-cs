with import <nixpkgs> {};

let
  jsEnv = nodePackages.http-server;
in mkShell {
  packages = [
    jsEnv
  ];
}