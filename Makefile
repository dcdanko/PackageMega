.PHONY: lint

lint:
    pylint --rcfile=.pylintrc --load-plugins pylint_quotes moduleultra -f parseable -r n && \
    pycodestyle moduleultra --max-line-length=120 && \
    pydocstyle moduleultra
