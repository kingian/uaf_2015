#!/bin/bash
while true
do
    sleep 5
    sudo find /tmp/motion/cam1 -name "*.jpg" -not -newermt '-5 seconds' -delete
    sudo find /tmp/motion/cam2 -name "*.jpg" -not -newermt '-5 seconds' -delete
    sudo find /tmp/motion/cam3 -name "*.jpg" -not -newermt '-5 seconds' -delete
done
