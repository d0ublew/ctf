#!/usr/bin/env bash

java -jar ./bundletool-all-1.17.2.jar build-apks --bundle=./app-release.aab --output=./app-release.apks --mode=universal
