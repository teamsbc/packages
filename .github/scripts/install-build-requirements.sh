#!/usr/bin/env bash
set -euo pipefail

requirements=()
while IFS= read -r dir; do
  pushd "$dir" > /dev/null
  options=()
  if [ -f .build-args ]; then mapfile -t options < .build-args; fi
  specs=(./*.spec)
  if [ -f .prepared ]; then specs=(SPECS/*.spec); fi
  output=$(rpmspec "${options[@]}" -q --srpm --buildrequires "${specs[@]}")
  if [ -n "$output" ]; then
    mapfile -t package_requirements <<< "$output"
    requirements+=("${package_requirements[@]}")
  fi
  popd > /dev/null
done < "$1"

if [ "${#requirements[@]}" -gt 0 ]; then
  dnf install -y "${requirements[@]}"
fi
