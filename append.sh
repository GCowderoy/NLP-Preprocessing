#!/bin/bash

string=" ."

while read line; do
    echo "$line$string"
done