#!/bin/sh

set -eu

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "downloading xray"
wget -O "${TMP_DIR}/xray.zip" https://github.com/XTLS/Xray-core/releases/download/v26.3.27/Xray-linux-64.zip

echo "installing"
unzip "${TMP_DIR}/xray.zip" -d "${TMP_DIR}"
chmod +x "${TMP_DIR}/xray"
mv "${TMP_DIR}/xray" /usr/local/bin/xray
echo "installed!"
