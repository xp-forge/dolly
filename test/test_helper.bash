load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

DOLLY_ROOT="$BATS_TMPDIR/dolly_test/dev"
DOLLY="$BATS_TEST_DIRNAME/../dolly/__main__.py -r $DOLLY_ROOT"
FIXTURES="$BATS_TEST_DIRNAME/fixtures"
CONFIGS="$BATS_TMPDIR/dolly_test/configs"

cleanup() {
  rm -rf "$BATS_TMPDIR/dolly_test"
}

prepare_configs() {
  # Replace $FIXTURES in the dolly config files.
  mkdir -p "$CONFIGS"
  for file in "$FIXTURES"/*.yaml; do
    sed 's#$FIXTURES#'"$FIXTURES"'#g' "$file" > "$CONFIGS/$(basename $file)"
  done
}
