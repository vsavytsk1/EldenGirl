# ─────────────────────────────────────────────────────────────────────────
# THE GATES are task one. "make gates" is the whole promise, executable.
#   A gate that warns is a comment. These exit non-zero and block the merge.
# ─────────────────────────────────────────────────────────────────────────
PYTHON ?= python

.DEFAULT_GOAL := gates

.PHONY: gates gates-fast hooks web-check help

## gates       : run every gate; exits non-zero on any failure (CI target)
gates:
	$(PYTHON) gates/run_gates.py

## gates-fast  : the <5s subset, for the pre-commit hook
gates-fast:
	$(PYTHON) gates/run_gates.py --fast

## hooks       : install the pre-commit hook so an agent hits the wall in minute two
hooks:
	$(PYTHON) gates/install_hooks.py

## web-check   : the web tier zero-write / no-network / not-installable check
web-check:
	$(PYTHON) gates/run_gates.py --fast

## help        : list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'
