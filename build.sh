#!/bin/sh
# Gera docs/index.html (documento completo para o GitHub Pages) a partir de index.html (trecho usado no artefato).
set -e
cd "$(dirname "$0")"
mkdir -p docs
{
  printf '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#000000">\n'
  cat index.html
  printf '\n</body>\n</html>\n'
} > docs/index.html
