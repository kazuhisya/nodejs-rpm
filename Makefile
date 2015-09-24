BASE := node
NAME := $(BASE)js
VERSION := $(shell grep Version: $(NAME).spec | tr -s " "| cut -d " " -f 2)

CC = gcc
GCCVERSION_480 := $(shell expr `gcc -dumpversion | sed -e 's/\.\([0-9][0-9]\)/\1/g' -e 's/\.\([0-9]\)/0\1/g' -e 's/^[0-9]\{3,4\}$$/&00/'` \>= 40800)
PYVERSION_270 := $(shell expr `python --version 2>&1 |cut -c 8- | sed -e 's/\.\([0-9][0-9]\)/\1/g' -e 's/\.\([0-9]\)/0\1/g' -e 's/^[0-9]\{3,4\}$$/&00/'` \>= 20700)

rpm:
ifeq "$(GCCVERSION_480)" "1"
ifeq "$(PYVERSION_270)" "1"
	spectool -g  $(NAME).spec
	mkdir -p dist/{BUILD,RPMS,SPECS,SOURCES,SRPMS,install}
	mv $(BASE)-v*.tar.gz dist/SOURCES/
	cp -pf *.patch dist/SOURCES/
	rpmbuild -ba \
		--define "_topdir $(PWD)/dist" \
		--define "buildroot $(PWD)/dist/install" \
		--clean \
		$(NAME).spec
else
	@echo "Python too old..."
endif
else
	@echo "C++ compiler too old..."
endif
