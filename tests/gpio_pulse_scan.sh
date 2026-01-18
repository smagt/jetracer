#!/bin/bash
set -e
GPIOS=(4 5 6 12 13 16 17 18 19 20 21 22 23 24 25 26 27)
for g in "${GPIOS[@]}"; do
  cmd="sudo gpioset -c gpiochip0 -t 1s,0 ${g}=1"
  echo ">>> $cmd"
  read -p "Press Enter to pulse GPIO${g}…"
  eval "$cmd"
done
