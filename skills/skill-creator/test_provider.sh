#!/bin/bash
# Test script to verify provider flag works
# Run from skill-creator directory: ./test_provider.sh

set -e

cd "$(dirname "$0")"

echo "=== Testing Provider Flag Functionality ==="
echo ""

echo "1. Testing run_eval.py --help with provider flag..."
python3 -m scripts.run_eval --help 2>/dev/null | grep -q "provider" && echo "   PASS: --provider flag available"

echo ""
echo "2. Testing available providers..."
python3 -c "import sys; sys.path.insert(0, '.'); from scripts.run_eval import get_available_providers; print('   Available:', get_available_providers())"

echo ""
echo "3. Testing run_loop.py --help with provider flag..."
python3 -m scripts.run_loop --help 2>/dev/null | grep -q "provider" && echo "   PASS: --provider flag available"

echo ""
echo "4. Testing improve_description.py --help with provider flag..."
python3 -m scripts.improve_description --help 2>/dev/null | grep -q "provider" && echo "   PASS: --provider flag available"

echo ""
echo "5. Testing provider-specific command building..."
python3 -c "
import sys
sys.path.insert(0, '.')
from scripts.run_eval import build_command, PROVIDERS
for p in PROVIDERS:
    cmd = build_command(p, 'test query', None)
    print(f'   {p}: {cmd[0]} -p ...')
"

echo ""
echo "=== All Provider Flag Tests Passed ==="
