#!/bin/bash
python3 /home/joft/homeautomation/main_rpi_board/main.py &

cd /home/joft/homeautomation/main_rpi_board/vue/
npm run serve &

cd 
