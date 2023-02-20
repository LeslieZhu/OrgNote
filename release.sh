for env in "2.7.15" "3.5.6" "3.7.2";
do
    pyenv local $env
    python setup.py bdist
    python setup.py bdist_wheel
    #python setup.py sdist
done

twine upload dist/orgnote-1.0.5*
