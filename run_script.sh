#!/bin/bash

# Script to run main_german.py with proper environment setup
cd /Users/arriazui/Desktop/GreenComputing/lithops_fork
source .venv/bin/activate
export LITHOPS_CONFIG_FILE=/Users/arriazui/Desktop/GreenComputing/lithops_fork/lithops_config.yaml
python energy_documentation/main_german.py
