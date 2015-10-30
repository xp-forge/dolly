#!/usr/bin/env bats

load test_helper

setup() {
	cleanup
	prepare_configs
}

teardown() {
	cleanup
}

@test "dolly update clones repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	[ "$status" -eq 0 ]
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]
}

@test "dolly update pulls existing repositories" {
	# First, install all repositories.
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	[ "$status" -eq 0 ]
	# Reset one of them.
	(cd "$DOLLY_ROOT"/repositories/repo2 && git reset --hard HEAD^)
	# Verify that some files are missing.
	[[ ! -e "$DOLLY_ROOT"/repositories/repo2/e ]]

	# Dolly should undo this.
	run $DOLLY -c "$CONFIGS/simple.yaml" update
	[ "$status" -eq 0 ]
	# Check that both repositories exist...
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]
	# ...and that the file is there now.
	[[ ! -e "$DOLLY_ROOT"/repositories/repo2/e ]]
}
