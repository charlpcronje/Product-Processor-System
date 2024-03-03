#!/bin/bash

# Create Conda environment
conda create --name pna python=3.12 -y

# Activate the environment
source activate pna

# Install requirements using pip
pip install -r requirements.txt

# Wait for user input before closing
read -p "Press any key to continue... " -n1 -s
