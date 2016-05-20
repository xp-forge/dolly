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
	run $DOLLY -c "$CONFIGS/simple.yaml" update
	assert_success
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]
}

@test "dolly update pulls existing repositories" {
	# First, install all repositories.
	run $DOLLY -c "$CONFIGS/simple.yaml" update
	assert_success
	# Reset one of them.
	(cd "$DOLLY_ROOT"/repositories/repo2 && git reset --hard HEAD^)
	# Verify that some files are missing.
	[[ ! -e "$DOLLY_ROOT"/repositories/repo2/e ]]

	# Dolly should undo this.
	run $DOLLY -c "$CONFIGS/simple.yaml" update
	assert_success
	# Check that both repositories exist...
	[[ -d "$DOLLY_ROOT"/repositories/repo1 ]]
	[[ -d "$DOLLY_ROOT"/repositories/repo2 ]]
	# ...and that the file is there now.
	[[ -e "$DOLLY_ROOT"/repositories/repo2/e ]]
}

@test "dolly update runs the project's post_update command after cloning" {
	run $DOLLY -c "$CONFIGS/post_update.yaml" update
	assert_success
	[[ -e "$DOLLY_ROOT"/post_update ]]
}

@test "dolly update does not run a repository's post_update command when nothing is updated" {
	$DOLLY -c "$CONFIGS/repo_post_update.yaml" update
	[[ -e "$DOLLY_ROOT"/repositories/repo1/post_update ]]
	rm "$DOLLY_ROOT"/repositories/repo1/post_update

	$DOLLY -c "$CONFIGS/repo_post_update.yaml" update
	[[ ! -e "$DOLLY_ROOT"/repositories/repo1/post_update ]]
}
