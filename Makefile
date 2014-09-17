BASE := node
NAME := $(BASE)js
VERSION := $(shell grep Version: $(NAME).spec | tr -s " "| cut -d " " -f 2)

rpm:
	spectool -g  $(NAME).spec
	mkdir -p dist/{BUILD,RPMS,SPECS,SOURCES,SRPMS,install}
	mv $(BASE)-v*.tar.gz dist/SOURCES/
	cp -pf *.patch dist/SOURCES/
	rpmbuild -ba \
		--define "_topdir $(PWD)/dist" \
		--define "buildroot $(PWD)/dist/install" \
		--clean \
		$(NAME).spec
