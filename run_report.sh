#!/bin/bash
# Quick start script to generate IFRS 17 report

# Activate virtual environment
source venv/bin/activate

# Generate report
python -m ifrs17.main "$@"

# Deactivate virtual environment
deactivate
