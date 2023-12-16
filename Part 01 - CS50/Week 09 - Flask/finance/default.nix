{ pkgs ? import <nixpkgs> {} }:

let
  my-python-packages = ps: with ps; [
    flask
    flask-session
    pytz
    requests
    sqlalchemy
    sqlparse
    termcolor
    werkzeug
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
