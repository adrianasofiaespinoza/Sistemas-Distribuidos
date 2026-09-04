#!/usr/bin/env bash
set -u

lab="${1:-naming_lab}"

mkdir -p "$lab/data"
cd "$lab"

printf "Distributed Systems\n" > data/original.txt

echo '$ find .'
find .

echo
echo '$ ln data/original.txt hardlink.txt'
ln data/original.txt hardlink.txt

echo '$ ln -s data/original.txt softlink.txt'
ln -s data/original.txt softlink.txt

echo
echo '$ ls -li hardlink.txt softlink.txt data/original.txt'
ls -li hardlink.txt softlink.txt data/original.txt

echo
echo '$ cat hardlink.txt'
cat hardlink.txt

echo '$ cat softlink.txt'
cat softlink.txt

echo
echo '$ mv data/original.txt data/renamed.txt'
mv data/original.txt data/renamed.txt

echo '$ cat hardlink.txt'
cat hardlink.txt

echo '$ cat softlink.txt'
cat softlink.txt || true

echo
echo '$ rm data/renamed.txt'
rm data/renamed.txt

echo '$ cat hardlink.txt'
cat hardlink.txt

echo '$ cat softlink.txt'
cat softlink.txt || true
