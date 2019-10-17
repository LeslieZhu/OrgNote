for env in "2.7.15" "3.5.2";
do
    pyenv local $env
    python setup.py bdist
    python setup.py bdist_wheel
    python setup.py sdist
done

twine upload dist/orgnote-0.5.5*
