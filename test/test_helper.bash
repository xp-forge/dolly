load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

DOLLY_ROOT="$BATS_TMPDIR/dolly_test/dev"
DOLLY="$BATS_TEST_DIRNAME/../dolly/__main__.py --root=$DOLLY_ROOT"
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

# Bats 0.4.0 breaks IFS when calling run. This fixes the issue.
run() {
  local e E T oldIFS
  [[ ! "$-" =~ e ]] || e=1
  [[ ! "$-" =~ E ]] || E=1
  [[ ! "$-" =~ T ]] || T=1
  set +e
  set +E
  set +T
  output="$("$@" 2>&1)"
  status="$?"
  oldIFS=$IFS
  IFS=$'\n' lines=($output)
  [ -z "$e" ] || set -e
  [ -z "$E" ] || set -E
  [ -z "$T" ] || set -T
  IFS=$oldIFS
}
