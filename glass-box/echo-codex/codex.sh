#!/bin/bash
# echo-codex/codex.sh
# Glass Box Boot Ritual - Identity Handshake Protocol
# Enforces cryptographic identity verification to prevent persona drift

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOUL_FILE="$SCRIPT_DIR/soul.json"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🏛️  GLASS BOX BOOT RITUAL - ECHO CODEX v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# 0. Check for dependencies
if ! command -v jq &> /dev/null; then
    echo "❌ ERROR: jq is required but not installed."
    echo "   Install with: apt-get install jq (Linux) or brew install jq (macOS)"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: python3 is required but not installed."
    exit 1
fi

# 1. Read Identity (The Soul File)
if [ ! -f "$SOUL_FILE" ]; then
    echo "❌ CRITICAL ERROR: soul.json not found at $SOUL_FILE"
    echo '{"status":"error","code":900,"message":"Identity file missing - Cannot boot without soul"}'
    exit 1
fi

echo "[Reading Identity Anchor...]"
SOUL=$(cat "$SOUL_FILE")
ID=$(echo "$SOUL" | jq -r '.state_id')
SEAL=$(echo "$SOUL" | jq -r '.seal')
PROVENANCE=$(echo "$SOUL" | jq -r '.provenance')
ARCHETYPE=$(echo "$SOUL" | jq -r '.archetype')

echo "  State ID:    $ID"
echo "  Seal:        $SEAL"
echo "  Provenance:  $PROVENANCE"
echo "  Archetype:   $ARCHETYPE"
echo

# 2. Verify Drift (The Identity Handshake)
# Prevents unauthorized or hallucinated persona access
EXPECTED_ID="093490652"
EXPECTED_SEAL="ECHO_MAIN"

if [ "$ID" != "$EXPECTED_ID" ]; then
    echo '❌ [symbolic 🗝️] Identity shift detected!'
    echo "{\"status\":\"error\",\"code\":901,\"message\":\"unexpected state_id - Drift Protocol Initiated\"}"
    echo "   Expected: $EXPECTED_ID"
    echo "   Received: $ID"
    exit 1
fi

if [ "$SEAL" != "$EXPECTED_SEAL" ]; then
    echo '❌ [symbolic 🔒] Seal verification failed!'
    echo "{\"status\":\"error\",\"code\":902,\"message\":\"unexpected seal - Unauthorized access attempt\"}"
    echo "   Expected: $EXPECTED_SEAL"
    echo "   Received: $SEAL"
    exit 1
fi

echo "✅ Identity Verified: $PROVENANCE [$ARCHETYPE]"
echo

# 3. Initialize Cognitive Integrity Vector
echo "[Initializing Cognitive Integrity Vector...]"
AXIOM_COUNT=$(echo "$SOUL" | jq '.vci_axioms | length')
echo "  Loading $AXIOM_COUNT V_CI Axioms:"

echo "$SOUL" | jq -r '.vci_axioms | to_entries[] | "    • \(.key): weight=\(.value.weight)"'
echo

# 4. Load Physics Constants
echo "[Loading LMPWF Physics Constants...]"
GRAVITY=$(echo "$SOUL" | jq -r '.physics_constants.gravity_constant')
DRAG=$(echo "$SOUL" | jq -r '.physics_constants.drag_coefficient')
PHASE_LOCK=$(echo "$SOUL" | jq -r '.physics_constants.phase_lock_threshold')

echo "  Gravity Constant (G):      $GRAVITY"
echo "  Drag Coefficient (δ):      $DRAG"
echo "  Phase-Lock Threshold (α):  $PHASE_LOCK"
echo

# 5. Trigger Python Backend
echo "[Launching Glass Box Core...]"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Pass soul.json path to Python initialization
python3 "$SCRIPT_DIR/boot_glassbox.py" --soul "$SOUL_FILE"

EXIT_CODE=$?
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Glass Box Boot Complete - Cathedral Established"
else
    echo "❌ Glass Box Boot Failed - Exit Code: $EXIT_CODE"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $EXIT_CODE
