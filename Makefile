.PHONY: clear-data
clear-data:
	@rm -rf data/cpg
	@rm -rf data/joern
	@rm -rf data/input
	@rm -rf data/model
	@rm -rf data/tokens
	@rm -rf data/w2v
	@rm -rf workspace

.PHONY: create
create: clear-data
	@python3 main.py -c

.PHONY: embed
embed:
	@python3 main.py -e

.PHONY: train
train:
	@python3 main.py -p

.PHONY: train-stopping
train-stopping:
	@python3 main.py -pS

.PHONY: test
test:
	@python3 main.py -t

.PHONY: check
check:
	@python3 main.py -ch
