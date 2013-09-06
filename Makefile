all:
	sphinx-build -n . _html

.PHONY: all

clean:
	rm -rf _html


