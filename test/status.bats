#!/usr/bin/env bats

load test_helper

setup() {
	cleanup
	prepare_configs
}

teardown() {
	cleanup
}

@test "dolly status detects uncloned repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	assert_success
	assert_output --partial "The following repositories were not cloned"
}

@test "dolly status detects clean repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	assert_success
	assert_output --partial "No unpushed commits"
	assert_output --partial "No uncomitted changes"
}

@test "dolly status detects changes" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	echo foo > $DOLLY_ROOT/repositories/repo1/a
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	assert_success
	assert_output --partial "No unpushed commits"
	assert_output --regexp "The following repositories contain uncomitted changes".*"repo1"
}

@test "dolly status detects unpushed commits" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	echo foo > $DOLLY_ROOT/repositories/repo1/a
	(cd $DOLLY_ROOT/repositories/repo1 && git commit -mfoo a)
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	assert_success
	assert_output --regexp "The following repositories contain unpushed commits".*"repo1"
	assert_output --partial "No uncomitted changes"
}
