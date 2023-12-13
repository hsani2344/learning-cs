{ pkgs ? import <nixpkgs> {} }:

let
  my-python-packages = ps: with ps; [
    sqlalchemy
    flask
    sqlparse
    termcolor
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
