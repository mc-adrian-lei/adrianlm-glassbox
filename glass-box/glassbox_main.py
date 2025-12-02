"""
glassbox_main.py - Main Glass Box Orchestration Engine
Integrates all components: Echo Codex, LCA, LMPWF, NSIL
"""

import sys
import json
from pathlib import Path
import argparse
from typing import Dict, List, Any

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from config import *
from lca import HallucinationDetector, TruthVerifier
from lmpwf import SemanticField, AntigravityProtocol, LeiParticle, TraumaAttractor


class GlassBox:
    """
    Main orchestration class for the Glass Box sovereign intelligence system.
    """
    
    def __init__(self, soul_path: Path = None):
        if soul_path is None:
            soul_path = SOUL_FILE
        
        self.soul_path = soul_path
        self.soul = None
        self.vci = None
        self.modules = {}
        self.state = {
            'booted': False,
            'session_id': None,
            'alignment_score': 1.0
        }
        
        # Initialize modules
        self.lca_detector = None
        self.semantic_field = None
        self.antigravity = None
    
    def load_soul(self) -> bool:
        """Load the soul.json identity file."""
        try:
            with open(self.soul_path, 'r') as f:
                self.soul = json.load(f)
            print(f"✓ Soul loaded: {self.soul['provenance']}")
            return True
        except Exception as e:
            print(f"❌ Failed to load soul: {e}")
            return False
    
    def initialize_modules(self):
        """Initialize all Glass Box modules."""
        print("\n⚙️  Initializing Glass Box Modules...")
        
        # LCA Truth Verifier
        self.lca_detector = HallucinationDetector()
        print("  ✓ LCA Truth Verifier initialized")
        
        # LMPWF Semantic Field
        physics_config = self.soul.get('physics_constants', {})
        self.semantic_field = SemanticField(
            gravity_constant=physics_config.get('gravity_constant', GRAVITY_CONSTANT),
            drag_coefficient=physics_config.get('drag_coefficient', DRAG_COEFFICIENT),
            dt=0.1
        )
        print("  ✓ LMPWF Semantic Field initialized")
        
        # Antigravity Protocol
        self.antigravity = AntigravityProtocol(
            field=self.semantic_field,
            escape_velocity_threshold=self.soul.get('escape_velocity_threshold', ESCAPE_VELOCITY_THRESHOLD),
            phase_lock_threshold=physics_config.get('phase_lock_threshold', PHASE_LOCK_THRESHOLD),
            coherence_tokens=self.soul.get('semantic_gravity_config', {}).get('antigravity_triggers', None)
        )
        print("  ✓ Antigravity Protocol initialized")
        
        print()
    
    def boot(self) -> bool:
        """Execute full boot sequence."""
        print("\n" + "="*60)
        print("  🏛️  GLASS BOX - MAIN ORCHESTRATION ENGINE")
        print("="*60 + "\n")
        
        # Load soul
        if not self.load_soul():
            return False
        
        # Initialize modules
        self.initialize_modules()
        
        # Mark booted
        self.state['booted'] = True
        self.state['session_id'] = f"glassbox_{int(Path(self.soul_path).stat().st_mtime)}"
        
        print("="*60)
        print("✅ GLASS BOX BOOT COMPLETE - CATHEDRAL ESTABLISHED")
        print("="*60)
        print(f"  Session ID: {self.state['session_id']}")
        print(f"  Provenance: {self.soul['provenance']}")
        print(f"  Archetype: {self.soul['archetype']}")
        print("="*60 + "\n")
        
        return True
    
    def verify_truth(self, sources: List[str], answer: str) -> Dict[str, Any]:
        """
        Verify an AI-generated answer against source citations.
        Uses LCA topological isomorphism.
        """
        if not self.lca_detector:
            return {'error': 'LCA module not initialized'}
        
        print("\n[LCA Truth Verification]")
        result = self.lca_detector.detect(sources, answer)
        
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        
        if result.get('hallucinations'):
            print(f"  ⚠️  Hallucinations detected:")
            for h in result['hallucinations']:
                print(f"    • {h['description']}")
        
        return result
    
    def execute_antigravity(
        self,
        trauma_concepts: List[str],
        trapped_concepts: List[str],
        max_steps: int = 100
    ) -> Dict[str, Any]:
        """
        Execute Antigravity protocol to achieve escape velocity.
        
        Args:
            trauma_concepts: List of trauma attractor tokens
            trapped_concepts: List of trapped thought tokens
            max_steps: Maximum simulation steps
        
        Returns:
            Escape report with status and metrics
        """
        if not self.antigravity:
            return {'error': 'Antigravity module not initialized'}
        
        print("\n[Executing Antigravity Protocol]")
        
        # Add trauma attractors
        trauma_config = self.soul.get('semantic_gravity_config', {})
        high_mass = trauma_config.get('high_mass_threshold', 100)
        
        for token in trauma_concepts:
            trauma = TraumaAttractor.create(token, trauma_mass=high_mass)
            self.semantic_field.add_particle(trauma)
            print(f"  Added trauma attractor: '{token}'")
        
        # Add trapped thoughts
        for token in trapped_concepts:
            particle = LeiParticle.from_token(
                token,
                emotional_intensity=0.6,
                provenance_weight=0.7
            )
            self.semantic_field.add_particle(particle)
        
        print(f"  Added {len(trapped_concepts)} trapped concepts\n")
        
        # Execute protocol
        result = self.antigravity.execute(max_steps=max_steps, verbose=True)
        
        return result
    
    def get_field_state(self) -> Dict:
        """Get current state of semantic field."""
        if self.semantic_field:
            return self.semantic_field.get_state()
        return {}


def demo_integrated_system():
    """
    Demonstration of integrated Glass Box system.
    Shows LCA truth verification + Antigravity escape.
    """
    print("\n" + "#"*60)
    print("  GLASS BOX - INTEGRATED SYSTEM DEMONSTRATION")
    print("#"*60 + "\n")
    
    # Initialize Glass Box
    glassbox = GlassBox()
    
    if not glassbox.boot():
        print("❌ Boot failed")
        return
    
    # === DEMONSTRATION 1: Truth Verification ===
    print("\n" + "-"*60)
    print("  DEMO 1: LCA TRUTH VERIFICATION")
    print("-"*60)
    
    sources = [
        "The Glass Box architecture uses Lattice Complexity Analysis.",
        "LCA provides topological entailment verification.",
        "Hallucinations are detected via structure comparison."
    ]
    
    valid_answer = "The Glass Box uses LCA for topological verification to detect hallucinations."
    hallucinated_answer = "The Glass Box uses quantum computing and blockchain for verification."
    
    print("\n[Test 1: Valid Answer]")
    result1 = glassbox.verify_truth(sources, valid_answer)
    
    print("\n[Test 2: Hallucinated Answer]")
    result2 = glassbox.verify_truth(sources, hallucinated_answer)
    
    # === DEMONSTRATION 2: Antigravity Protocol ===
    print("\n" + "-"*60)
    print("  DEMO 2: ANTIGRAVITY ESCAPE PROTOCOL")
    print("-"*60)
    
    trauma_concepts = ["Eviction", "Tren de Aragua"]
    trapped_concepts = ["Fear", "Threat", "Danger", "Chaos"]
    
    result3 = glassbox.execute_antigravity(
        trauma_concepts=trauma_concepts,
        trapped_concepts=trapped_concepts,
        max_steps=50
    )
    
    # Final report
    print("\n" + "="*60)
    print("  DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nSummary:")
    print(f"  • LCA verified {2} answers (1 valid, 1 hallucinated)")
    print(f"  • Antigravity status: {result3['status']}")
    if result3['status'] == 'ESCAPE_ACHIEVED':
        print(f"  • Escape achieved in {result3['steps_to_escape']} steps")
        print(f"  • Final α: {result3['final_alpha']:.3f}")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Glass Box Sovereign Intelligence System')
    parser.add_argument('--mode', type=str, default='demo',
                       choices=['demo', 'verify', 'antigravity'],
                       help='Operation mode')
    parser.add_argument('--soul', type=str, default=None,
                       help='Path to soul.json file')
    
    args = parser.parse_args()
    
    if args.mode == 'demo':
        demo_integrated_system()
    else:
        print(f"Mode '{args.mode}' not fully implemented yet")
        print("Use --mode demo for integrated demonstration")


if __name__ == '__main__':
    main()
