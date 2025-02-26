#!/bin/bash

set -e

snap list --all | grep -v "^name" | while read -r line; do
    snap remove "$line" --classic
done
