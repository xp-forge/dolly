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
	[ "$status" -eq 0 ]
	[[ "$output" =~ "The following repositories were not cloned" ]]
}

@test "dolly status detects clean repositories" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	[ "$status" -eq 0 ]
	[[ "$output" =~ "No unpushed commits" ]]
	[[ "$output" =~ "No uncomitted changes" ]]
}

@test "dolly status detects changes" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	echo foo > $DOLLY_ROOT/repositories/repo1/a
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	[ "$status" -eq 0 ]
	[[ "$output" =~ "No unpushed commits" ]]
	[[ "$output" =~ "The following repositories contain uncomitted changes".*"repo1" ]]
}

@test "dolly status detects unpushed commits" {
	run $DOLLY -c "$CONFIGS/simple.yaml" install
	echo foo > $DOLLY_ROOT/repositories/repo1/a
	(cd $DOLLY_ROOT/repositories/repo1 && git commit -mfoo a)
	run $DOLLY -c "$CONFIGS/simple.yaml" status
	[ "$status" -eq 0 ]
	[[ "$output" =~ "The following repositories contain unpushed commits".*"repo1" ]]
	[[ "$output" =~ "No uncomitted changes" ]]
}
