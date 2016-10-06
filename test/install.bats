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
	assert_success
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]
}

@test "dolly install ignores existing repositories" {
	mkdir -p "$DOLLY_ROOT"/repositories/repo1/.git
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	assert_success
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]        # Folder exists...
	[[ ! -f "$DOLLY_ROOT"/repositories/repo1/.git/index ]] # ...but is still empty.
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]        # This repository is new.
}
