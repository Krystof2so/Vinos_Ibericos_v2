#!/usr/bin/env zsh

# Aller à la racine du projet
cd "$(dirname "$0")"

# Détecter si un environnement virtuel est activé
if [ -n "$VIRTUAL_ENV" ]; then
  PYTHON="$VIRTUAL_ENV/bin/python"
elif [ -f ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="python3"
fi

"$PYTHON" -m vinos_ibericos.main
