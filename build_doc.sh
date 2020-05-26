#!/bin/bash


cp CHANGELOG.md docs/docs
cp code_of_conduct.md docs/docs
python3 docs/generate.py
cd docs && mkdocs build
