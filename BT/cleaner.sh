#!/bin/bash
while true
do
    sleep 2
    sudo find /tmp/motion/cam1 -name "*.jpg" -not -newermt '-6 seconds' -delete
    sudo find /tmp/motion/cam2 -name "*.jpg" -not -newermt '-6 seconds' -delete
    sudo find /tmp/motion/cam3 -name "*.jpg" -not -newermt '-6 seconds' -delete
done
