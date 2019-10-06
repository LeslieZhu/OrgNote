for env in "2.7.15" "3.5.2";
do
    pyenv local $env
    python setup.py bdist
    python setup.py bdist_wheel
done

twine upload dist/orgnote-*
