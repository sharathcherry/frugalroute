#!/bin/sh
cd /frugalroute
echo "=== BLOCK B: Real Calibration Harness on MI300X ===" > /tmp/harness.log
echo "Started: $(date)" >> /tmp/harness.log
python3 eval/harness.py >> /tmp/harness.log 2>&1
echo "Finished: $(date)" >> /tmp/harness.log
echo "=== calib.json ===" >> /tmp/harness.log
cat /frugalroute/calib.json >> /tmp/harness.log
echo "=== automix.json ===" >> /tmp/harness.log
cat /frugalroute/automix.json >> /tmp/harness.log
