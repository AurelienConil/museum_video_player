#!/bin/sh
sudo lsof -t -i udp:12345 | xargs kill -9
