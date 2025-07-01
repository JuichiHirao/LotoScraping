#!/bin/bash
source /home/ec2-user/LotoScraping/venv/bin/activate
cd /home/ec2-user/LotoScraping
PYTHONPATH=. python loto/scraping_lottery.py
PYTHONPATH=. python loto/winning_check.py
