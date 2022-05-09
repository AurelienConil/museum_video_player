#!/bin/sh
sudo lsof -t -i udp:12344 | xargs kill -9
