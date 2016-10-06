#!/usr/bin/env bats

load test_helper

setup() {
	cleanup
	prepare_configs
}

teardown() {
	cleanup
}

@test "dolly untracked does not detect tracked repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	run $DOLLY -c "$CONFIGS/simple.yaml" untracked
	assert_success
	assert_output --partial "No untracked repositories."
}

@test "dolly status detects untracked repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	mkdir $DOLLY_ROOT/foobar $DOLLY_ROOT/repositories/untracked
	(cd $DOLLY_ROOT/foobar && git init)
	(cd $DOLLY_ROOT/repositories/untracked && git init)
	run $DOLLY -c "$CONFIGS/simple.yaml" untracked
	assert_success
	assert_output --partial "2 untracked repositories"
	assert_output --partial " - foobar"
	assert_output --partial " - repositories/untracked"
}

@test "dolly status does not detect untracked repositories below tracked ones" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	mkdir $DOLLY_ROOT/repositories/repo1/untracked
	(cd $DOLLY_ROOT/repositories/repo1/untracked && git init)
	run $DOLLY -c "$CONFIGS/simple.yaml" untracked
	assert_success
	assert_output --partial "No untracked repositories."
}
