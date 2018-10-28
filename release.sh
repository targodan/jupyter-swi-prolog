#!/bin/bash

rm -rf dist &>/dev/null
python -m pip install --user --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

echo -n "Deploy [N/y]? "
read -n1 yesNo

if [[ "$yesNo" == $(printf "\n\n") ]]; then
    yesNo=n
else
    echo ""
fi

if [[ "$yesNo" == "y" || "$yesNo" == "Y" ]]; then
    twine upload dist/*
fi
