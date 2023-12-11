##
# @file
# @version 0.1
STACK_NAME          ?= $(notdir $(CURDIR))-example
PULUMI_BACKEND_URL  ?= file://$(CURDIR)/../

info:
	@echo $(STACK_NAME)

init:
	PULUMI_BACKEND_URL=$(PULUMI_BACKEND_URL) \
	PULUMI_CONFIG_PASSPHRASE= \
	pulumi stack init -s $(STACK_NAME)

node_modules:
	npm install
	@echo @TODO npm link @jonjitsu/fabric

setup: node_modules

up-preview:
	PULUMI_BACKEND_URL=$(PULUMI_BACKEND_URL) \
	PULUMI_CONFIG_PASSPHRASE= \
	pulumi up -s $(STACK_NAME)

up:
	PULUMI_BACKEND_URL=$(PULUMI_BACKEND_URL) \
	PULUMI_CONFIG_PASSPHRASE= \
	pulumi up -s $(STACK_NAME) -y --skip-preview

destroy:
	PULUMI_BACKEND_URL=$(PULUMI_BACKEND_URL) \
	PULUMI_CONFIG_PASSPHRASE= \
	pulumi destroy -s $(STACK_NAME) -y

rm: destroy
	PULUMI_BACKEND_URL=$(PULUMI_BACKEND_URL) \
	PULUMI_CONFIG_PASSPHRASE= \
	pulumi stack rm -s $(STACK_NAME) -y --preserve-config

cleanup:
	-rm -rf node_modules
	-rm Pulumi.$(STACK_NAME).yaml

clean: destroy rm cleanup

e2e: setup init up destroy rm cleanup

converge: setup init up

.PHONY: info init setup up-preview up destroy rm cleanup clean e2e converge
# end
