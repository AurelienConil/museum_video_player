#!/bin/sh
sudo lsof -t -i udp:60221 | xargs kill -9
