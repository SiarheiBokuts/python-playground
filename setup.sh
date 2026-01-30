#!/bin/bash

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install browsers for Playwright
python -m playwright install

echo "✔️ Installation complete!"