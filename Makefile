.PHONY: help debian install build

SITE=${DESTDIR}/usr/share/yourss/site
BIN=${DESTDIR}/usr/bin/yourss
PYSCRIPTS=$(patsubst bin/%.py,${DESTDIR}/usr/share/yourss/scripts/%.py,$(shell find bin -name '*.py'))
SERVICES=$(patsubst services/%,${DESTDIR}/lib/systemd/system/%,$(shell find services -name '*'))

build: ## does nothing - here for debuild's sake

install: ${PYSCRIPTS} ${SERVICES} ${BIN} ${SITE} ## Install
	echo "INVOKED INSTALL: ${DESTDIR}"

help: ## Print this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

debian: ## Build the debian package
	# Sign it: debuild -b --lintian-opts --profile debian
	debuild -b -uc -us --lintian-opts --profile debian

$(DESTDIR)/usr/share/yourss/scripts/%: bin/%
	mkdir -p $(dir $@)
	cp $< $@

$(DESTDIR)/lib/systemd/system/%: services/%
	mkdir -p $(dir $@)
	cp $< $@

$(DESTDIR)/usr/bin/%: bin/%
	mkdir -p $(dir $@)
	cp $< $@

$(DESTDIR)/usr/share/yourss/site: site
	cp -r $< $@
