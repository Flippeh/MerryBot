#!/bin/bash
pid=$(screen -ls | awk '/\.MerryBot\t/ {print strtonum($1)}')
kill $pid
