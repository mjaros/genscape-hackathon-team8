#!/usr/bin/env bash

if [[ $# -eq 0 ]]; then
  echo "Filename is missing"
  exit 1
fi

FILENAME=$1
curl -X GET "http://127.0.0.1:5000/file/upload?filename=${FILENAME}"
