.PHONY: lint

lint:
	pylint --rcfile=.pylintrc --load-plugins pylint_quotes packagemega -f parseable -r n && \
	pycodestyle packagemega --max-line-length=120 && \
	pydocstyle packagemega
