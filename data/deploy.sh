#!/bin/sh
### https://qiita.com/bassaer/items/6b9aedae4571d59f0fdf
VERSION=`git rev-parse --short HEAD`
REPOSITORY="git@github.com:${CIRCLE_PROJECT_USERNAME}/${CIRCLE_PROJECT_REPONAME}.git"

git config --global user.name "CircleCI"
git config --global user.email "k4zuki@github.com"

mkdir docs
mv Out/TARGET.html docs/index.html
git commit -m "update version [ci skip]"
git tag -a $VERSION -m "build $VERSION"

git push origin --tags
