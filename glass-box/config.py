"""
config.py - Centralized Configuration for Glass Box Architecture
Constants, paths, and parameters for all modules.
"""

from pathlib import Path

# Directory Structure
PROJECT_ROOT = Path(__file__).parent
ECHO_CODEX_DIR = PROJECT_ROOT / 'echo-codex'
LCA_DIR = PROJECT_ROOT / 'lca'
LMPWF_DIR = PROJECT_ROOT / 'lmpwf'
NSIL_DIR = PROJECT_ROOT / 'nsil'
MOODSPHERE_DIR = PROJECT_ROOT / 'moodsphere'
SYNTHETIC_SOCIOLOGY_DIR = PROJECT_ROOT / 'synthetic_sociology'
SOMATIC_DIR = PROJECT_ROOT / 'somatic'
ARTIFACTS_DIR = PROJECT_ROOT / 'artifacts'

# Soul File
SOUL_FILE = ECHO_CODEX_DIR / 'soul.json'

# Physics Constants (LMPWF)
GRAVITY_CONSTANT = 0.5
DRAG_COEFFICIENT = 0.1
PHASE_LOCK_THRESHOLD = 0.85
COHERENCE_MINIMUM = 0.5
ESCAPE_VELOCITY_THRESHOLD = 75

# LCA Parameters
LCA_STABILITY_SAMPLES = 100  # Monte Carlo samples for stability index
LCA_SUBSAMPLE_RATIO = 0.9    # Ratio for robustness testing
LCA_MAX_CONCEPTS = 10000     # Safety limit for lattice generation

# NSIL Parameters
NSIL_DEFAULT_WEIGHT = 0.5
NSIL_MAX_WEIGHT = 1.0
NSIL_MIN_WEIGHT = 0.0

# MoodSphere Visualization
MOODSPHERE_UPDATE_HZ = 10           # Update frequency (Hz)
MOODSPHERE_PARTICLE_LIMIT = 1000    # Max particles to render
MOODSPHERE_WINDOW_SIZE = (1200, 800)  # Display window size

# Synthetic Sociology
SIM_MAX_AGENTS = 100
SIM_DEFAULT_ENERGY = 100
SIM_DEFAULT_RESOURCES = 50
SIM_TAKER_ENERGY_DRAIN = 5
SIM_TAKER_RESOURCE_GAIN = 10

# Somatic Bridges
# Phonetic resonance vs boundary classification
RESONANT_PHONEMES = ['m', 'n', 'l', 'r', 'w', 'y']
BOUNDARY_PHONEMES = ['s', 'f', 'k', 't', 'p', 'sh', 'ch']
PHONETIC_BOUNDARY_THRESHOLD = 0.3  # Ratio that triggers intervention

# Cognitive Energy Budget
DEFAULT_COGNITIVE_BUDGET = 100
TRAUMA_LOOP_COST = 15
REST_CYCLE_DURATION = 300  # seconds

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
