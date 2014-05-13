#!/bin/bash

xelatex -shell-escape Main
makeindex main.idx -s StyleInd.ist
biber Main
xelatex -shell-escape Main
