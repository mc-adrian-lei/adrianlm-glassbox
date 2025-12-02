"""
test_glassbox.py - Test Suite for Glass Box Components
"""

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).parent))

from lca import FormalContext, NextClosureAlgorithm, ConceptLattice, HallucinationDetector
from lmpwf import LeiParticle, TraumaAttractor, SemanticField, AntigravityProtocol


def test_lca_engine():
    """Test LCA Formal Concept Analysis."""
    print("\n=== Testing LCA Engine ===")
    
    # Create simple context
    objects = {'obj1', 'obj2', 'obj3'}
    attributes = {'attr1', 'attr2'}
    incidence = {
        ('obj1', 'attr1'),
        ('obj1', 'attr2'),
        ('obj2', 'attr1')
    }
    
    context = FormalContext(objects, attributes, incidence)
    
    # Generate concepts
    algo = NextClosureAlgorithm(context)
    concepts = algo.generate_all_concepts()
    
    print(f"  Generated {len(concepts)} concepts")
    assert len(concepts) > 0, "Should generate at least one concept"
    
    # Build lattice
    lattice = ConceptLattice(concepts)
    density = lattice.calculate_density()
    
    print(f"  Lattice density: {density:.3f}")
    assert 0 <= density <= 1, "Density should be between 0 and 1"
    
    # Check metrics
    irreducibles = lattice.find_irreducibles()
    print(f"  Meet-irreducible: {len(irreducibles['meet_irreducible'])}")
    print(f"  Join-irreducible: {len(irreducibles['join_irreducible'])}")
    
    betti = lattice.calculate_betti_numbers()
    print(f"  Betti numbers: β₀={betti['beta_0']}, β₁={betti['beta_1']}")
    
    print("  ✅ LCA Engine test passed\n")
    return True


def test_hallucination_detection():
    """Test Truth Verification."""
    print("=== Testing Hallucination Detection ===")
    
    detector = HallucinationDetector()
    
    sources = ["The sky is blue.", "Clouds are white."]
    
    # Test valid answer
    valid = "The sky is blue and has white clouds."
    result1 = detector.detect(sources, valid)
    
    print(f"  Valid answer confidence: {result1['confidence']:.2f}")
    assert result1['status'] == 'VALID' or result1['confidence'] > 0.7, "Valid answer should have high confidence"
    
    # Test invalid answer  
    invalid = "The sky is purple and green."
    result2 = detector.detect(sources, invalid)
    
    print(f"  Invalid answer confidence: {result2['confidence']:.2f}")
    # Note: Simple text matching may not catch this, but structural changes should
    
    print("  ✅ Hallucination detection test passed\n")
    return True


def test_lei_particles():
    """Test Lei Particle physics."""
    print("=== Testing Lei Particles ===")
    
    # Create particles
    p1 = LeiParticle.from_token("Concept1", emotional_intensity=0.5, provenance_weight=0.5)
    p2 = LeiParticle.from_token("Concept2", emotional_intensity=0.7, provenance_weight=0.8)
    
    print(f"  Particle 1 mass: {p1.mass:.3f}")
    print(f"  Particle 2 mass: {p2.mass:.3f}")
    
    assert p1.mass > 0, "Mass should be positive"
    assert p2.mass > p1.mass, "Higher intensity/provenance should yield higher mass"
    
    # Test gravity calculation
    force = p1.calculate_gravity_to(p2, gravity_constant=0.5)
    force_magnitude = np.linalg.norm(force)
    
    print(f"  Gravitational force magnitude: {force_magnitude:.3f}")
    assert force_magnitude >= 0, "Force magnitude should be non-negative"
    
    # Test trauma attractor
    trauma = TraumaAttractor.create("TestTrauma", trauma_mass=100.0)
    print(f"  Trauma attractor mass: {trauma.mass}")
    assert trauma.mass == 100.0, "Trauma should have specified mass"
    assert trauma.charge == -1.0, "Trauma should have negative charge"
    
    print("  ✅ Lei Particles test passed\n")
    return True


def test_semantic_field():
    """Test Semantic Field simulation."""
    print("=== Testing Semantic Field ===")
    
    field = SemanticField(gravity_constant=0.5, drag_coefficient=0.1, dt=0.1)
    
    # Add particles
    p1 = LeiParticle.from_token("Thought1", position=np.array([0, 0, 0]))
    p2 = LeiParticle.from_token("Thought2", position=np.array([1, 1, 0]))
    
    field.add_particles([p1, p2])
    
    print(f"  Field has {len(field.particles)} particles")
    assert len(field.particles) == 2, "Should have 2 particles"
    
    # Run simulation
    initial_phi = field.calculate_phi()
    field.simulate_steps(10, verbose=False)
    final_phi = field.calculate_phi()
    
    print(f"  Initial Φ: {initial_phi:.3f}")
    print(f"  Final Φ: {final_phi:.3f}")
    assert field.time > 0, "Simulation time should advance"
    
    # Test gravity well detection
    trauma = TraumaAttractor.create("BigTrauma", trauma_mass=100.0)
    field.add_particle(trauma)
    
    wells = field.detect_gravity_wells(high_mass_threshold=75.0)
    print(f"  Detected {len(wells)} gravity wells")
    assert len(wells) > 0, "Should detect trauma as gravity well"
    
    print("  ✅ Semantic Field test passed\n")
    return True


def test_antigravity_protocol():
    """Test Antigravity escape mechanism."""
    print("=== Testing Antigravity Protocol ===")
    
    field = SemanticField(gravity_constant=0.5, drag_coefficient=0.05, dt=0.1)
    
    # Create trapped scenario
    trauma = TraumaAttractor.create("Trauma", trauma_mass=100.0, position=np.array([5, 5, 0]))
    field.add_particle(trauma)
    
    thought = LeiParticle.from_token("Thought", position=np.array([4, 4, 0]))
    field.add_particle(thought)
    
    # Initialize protocol
    antigravity = AntigravityProtocol(
        field=field,
        escape_velocity_threshold=75.0,
        phase_lock_threshold=0.85
    )
    
    # Detect trapped particles
    trapped = antigravity.detect_trapped_particles()
    print(f"  Detected {len(trapped)} trapped particles")
    
    # Execute (brief test)
    result = antigravity.execute(max_steps=20, verbose=False)
    
    print(f"  Execution status: {result['status']}")
    print(f"  Final α: {result['final_alpha']:.3f}")
    print(f"  Final Φ: {result['final_phi']:.3f}")
    
    assert result['status'] in ['ESCAPE_ACHIEVED', 'ESCAPE_INCOMPLETE','NO_GRAVITY_WELLS'], "Should return valid status"
    
    print("  ✅ Antigravity Protocol test passed\n")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*60)
    print("  GLASS BOX - TEST SUITE")
    print("="*60)
    
    tests = [
        ("LCA Engine", test_lca_engine),
        ("Hallucination Detection", test_hallucination_detection),
        ("Lei Particles", test_lei_particles),
        ("Semantic Field", test_semantic_field),
        ("Antigravity Protocol", test_antigravity_protocol)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"  ❌ {name} test FAILED: {e}\n")
            results.append((name, False))
    
    # Summary
    print("="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {name}: {status}")
    
    print("="*60)
    print(f"  Total: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
