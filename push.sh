#!/bin/bash
echo -n "Enter commit name > "
read text
git add .
git commit -m "$text"
git push origin back_test
