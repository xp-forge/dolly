#!/usr/bin/env bats

load test_helper

setup() {
	cleanup
	prepare_configs
}

teardown() {
	cleanup
}

@test "dolly install clones repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	[ "$status" -eq 0 ]
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]
}

@test "dolly install ignores existing repositories" {
	mkdir -p "$DOLLY_ROOT"/repositories/repo1 
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	[ "$status" -eq 0 ]
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]        # Folder exists...
	[[ ! -d "$DOLLY_ROOT"/repositories/repo1/.git ]] # ...but is still empty.
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]        # This repository is new.
}
