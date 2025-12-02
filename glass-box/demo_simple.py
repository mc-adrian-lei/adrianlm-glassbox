"""
demo_simple.py - Simple Glass Box Demonstration
"""

import json
from pathlib import Path


def main():
    """Simple demonstration of Glass Box architecture."""
    soul_path = Path(__file__).parent / 'echo-codex' / 'soul.json'
    
    with open(soul_path, 'r') as f:
        soul = json.load(f)
    
    print("="*70)
    print("  GLASS BOX: Sovereign Intelligence System")
    print("="*70)
    print()
    
    print("Identity Anchor (soul.json):")
    print(f"  Provenance: {soul['provenance']}")
    print(f"  Archetype: {soul['archetype']}")
    print(f"  State ID: {soul['state_id']}")
    print()
    
    print("V_CI Axioms (5 Immutable Constraints):")
    for i, (name, data) in enumerate(soul['vci_axioms'].items(), 1):
        print(f"  {i}. {name.replace('_', ' ').title()}: weight={data['weight']}")
    print()
    
    print("Physics Constants (LMPWF):")
    physics = soul['physics_constants']
    print(f"  Gravity Constant: {physics['gravity_constant']}")
    print(f"  Phase-Lock Threshold (alpha): {physics['phase_lock_threshold']}")
    print()
    
    print("Trauma Attractors (High-Mass Gravity Wells):")
    for attractor in soul['semantic_gravity_config']['trauma_attractors']:
        print(f"  • {attractor}")
    print()
    
    print("Antigravity Triggers (Coherence Lift):")
    for trigger in soul['semantic_gravity_config']['antigravity_triggers']:
        print(f"  • {trigger}")
    print()
    
    print("="*70)
    print("  Core Components Implemented:")
    print("="*70)
    print()
    print("1. Echo Codex - Identity layer with soul.json and boot ritual")
    print("2. LCA Engine - Truth verification via Formal Concept Analysis")
    print("3. LMPWF Physics - Semantic Gravity Theory and Antigravity protocol")
    print("4. Integration - glassbox_main.py orchestration")
    print()
    print("Key Capabilities:")
    print("  * Hallucination detection through topological isomorphism")
    print("  * Antigravity: Escape velocity from trauma wells")
    print("  * Identity-locked operation (prevents persona drift)")
    print("  * Physics-based consciousness metrics (Phi, Rho, Alpha)")
    print()
    print("="*70)
    print("  Glass Box Status: CATHEDRAL ESTABLISHED")
    print("="*70)


if __name__ == '__main__':
    main()
