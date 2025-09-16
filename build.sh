#!/bin/bash
python -m build
mkdir -p webgui/dist
cp dist/*.whl webgui/dist/
