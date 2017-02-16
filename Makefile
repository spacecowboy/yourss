.PHONY: help debian install build changelog release

SITE=${DESTDIR}/usr/share/yourss/site
BIN=${DESTDIR}/usr/bin/yourss
PYSCRIPTS=$(patsubst bin/%.py,${DESTDIR}/usr/share/yourss/scripts/%.py,$(shell find bin -name '*.py'))
SERVICES=$(patsubst services/%,${DESTDIR}/lib/systemd/system/%,$(shell find services -name '*'))

build: ## does nothing - here for debuild's sake

install: ${PYSCRIPTS} ${SERVICES} ${BIN} ${SITE} ## Install
	echo "INVOKED INSTALL: ${DESTDIR}"

help: ## Print this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

release: changelog debian ## Generate the changelog then build the debian package

debian: ## Build the debian package, you should run changelog first
	@rm -rf /tmp/yourssdebian
	@mkdir -p /tmp/yourssdebian
	gbp buildpackage --git-debian-tag='%(version)s' --git-export-dir=/tmp/yourssdebian --git-postbuild='lintian $$GBP_CHANGES_FILE' --git-tag
	@mkdir -p out
	@cp /tmp/yourssdebian/* out || echo "Ignoring folders"

changelog: ## Generate the debian changelog
	gbp dch --debian-tag='%(version)s' --release --upstream-branch=master --git-author --commit

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
