#!/bin/bash
rm -rf dist
python -m build
mkdir -p webgui/dist
cp dist/*.whl webgui/dist/
