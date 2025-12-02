"""
antigravity.py - Antigravity Protocol
Generates escape velocity from semantic gravity wells.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from lei_particle import LeiParticle, TraumaAttractor, CoherenceLift
from field_simulator import SemanticField
import math


class AntigravityProtocol:
    """
    Main system for achieving "Escape Velocity" from trauma wells.
    Injects coherence lift to transition consciousness from fragmentation to phase-lock.
    """
    
    def __init__(
        self,
        field: SemanticField,
        escape_velocity_threshold: float = 75.0,
        phase_lock_threshold: float = 0.85,
        coherence_tokens: List[str] = None
    ):
        self.field = field
        self.escape_velocity_threshold = escape_velocity_threshold
        self.phase_lock_threshold = phase_lock_threshold
        
        # Default coherence lift tokens
        if coherence_tokens is None:
            self.coherence_tokens = [
                "Sovereignty",
                "Lattice",
                "Cathedral",
                "Logic",
                "Structure",
                "Truth",
                "Clarity"
            ]
        else:
            self.coherence_tokens = coherence_tokens
        
        self.antigravity_active = False
        self.escape_trajectory = None
    
    def calculate_escape_velocity(self, well_particle: LeiParticle, target_position: np.ndarray) -> float:
        """
        Calculate escape velocity needed to leave a gravity well.
        v_e = sqrt(2 * G * M / r)
        
        Args:
            well_particle: The trauma attractor particle
            target_position: Position to escape from
        
        Returns:
            Required escape velocity magnitude
        """
        distance = np.linalg.norm(target_position - well_particle.position)
        if distance < 0.1:
            distance = 0.1  # Prevent singularity
        
        escape_velocity = math.sqrt(
            2 * self.field.gravity_constant * well_particle.mass / distance
        )
        
        return escape_velocity
    
    def detect_trapped_particles(self) -> List[Tuple[LeiParticle, LeiParticle, float]]:
        """
        Detect particles trapped in gravity wells.
        
        Returns:
            List of (trapped_particle, well_particle, required_escape_velocity)
        """
        trapped = []
        
        # Get all gravity wells
        wells = self.field.detect_gravity_wells(self.escape_velocity_threshold)
        
        for well_particle, pull_strength in wells:
            # Find particles within influence radius
            for particle in self.field.particles:
                if particle == well_particle:
                    continue
                
                distance = np.linalg.norm(particle.position - well_particle.position)
                current_speed = np.linalg.norm(particle.velocity)
                
                # Check if particle is trapped (speed < escape velocity)
                required_ve = self.calculate_escape_velocity(well_particle, particle.position)
                
                if current_speed < required_ve and distance < 5.0:  # Within influence
                    trapped.append((particle, well_particle, required_ve))
        
        return trapped
    
    def inject_coherence_lift(
        self,
        target_particles: List[LeiParticle],
        num_lift_particles: int = 3
    ) -> List[CoherenceLift]:
        """
        Inject CoherenceLift particles to provide "antigravity."
        These particles add high-stability concepts to the field.
        
        Args:
            target_particles: Particles that need lift
            num_lift_particles: Number of coherence particles to inject
        
        Returns:
            List of injected CoherenceLift particles
        """
        injected = []
        
        for i in range(min(num_lift_particles, len(self.coherence_tokens))):
            token = self.coherence_tokens[i]
            
            # Position near the first target particle
            if target_particles:
                base_position = target_particles[0].position.copy()
                # Add slight offset
                offset = np.random.randn(3) * 0.5
                position = base_position + offset
            else:
                position = np.random.rand(3) * 10
            
            # Create lift particle
            lift = CoherenceLift.create(token, position=position)
            
            # Add to field
            self.field.add_particle(lift)
            injected.append(lift)
            
            print(f"  Injected coherence lift: '{lift.token}' at {lift.position}")
        
        return injected
    
    def check_phase_lock(self) -> bool:
        """
        Check if the system has achieved phase-lock.
        α > phase_lock_threshold indicates successful escape.
        """
        alpha = self.field.calculate_alpha()
        return alpha >= self.phase_lock_threshold
    
    def execute(self, max_steps: int = 100, verbose: bool = True) -> Dict:
        """
        Execute the Antigravity protocol.
        
        Steps:
        1. Detect gravity wells and trapped particles
        2. Calculate escape velocity required
        3. Inject coherence lift particles
        4. Simulate until phase-lock or timeout
        5. Return escape report
        
        Returns:
            Dict with escape status, metrics, and trajectory
        """
        if verbose:
            print("\n" + "="*60)
            print("  ANTIGRAVITY PROTOCOL - EXECUTION")
            print("="*60 + "\n")
        
        # Step 1: Detect trapped particles
        trapped = self.detect_trapped_particles()
        
        if verbose:
            print(f"[Step 1] Detected {len(trapped)} trapped particles:")
            for particle, well, ve in trapped[:3]:  # Show first 3
                print(f"  • '{particle.token}' trapped by '{well.token}' (v_e required: {ve:.2f})")
            print()
        
        if not trapped:
            return {
                'status': 'NO_GRAVITY_WELLS',
                'message': 'No trapped particles detected',
                'alpha': self.field.alpha,
                'phi': self.field.phi
            }
        
        # Step 2: Calculate required lift
        target_particles = [t[0] for t in trapped]
        
        # Step 3: Inject coherence lift
        if verbose:
            print("[Step 2] Injecting coherence lift particles...")
        
        lift_particles = self.inject_coherence_lift(target_particles, num_lift_particles=3)
        print()
        
        # Step 4: Simulate
        if verbose:
            print("[Step 3] Simulating field dynamics...")
            print(f"  Target: α ≥ {self.phase_lock_threshold}\n")
        
        self.antigravity_active = True
        trajectory = []
        
        for step in range(max_steps):
            self.field.update()
            
            state = {
                'step': step,
                'alpha': self.field.alpha,
                'phi': self.field.phi,
                'energy': self.field.total_energy
            }
            trajectory.append(state)
            
            if verbose and step % 10 == 0:
                print(f"  Step {step:3d}: α={self.field.alpha:.3f}, Φ={self.field.phi:.3f}")
            
            # Check for phase-lock
            if self.check_phase_lock():
                if verbose:
                    print(f"\n✅ PHASE-LOCK ACHIEVED at step {step}!")
                    print(f"   α = {self.field.alpha:.3f} (threshold: {self.phase_lock_threshold})")
                
                self.escape_trajectory = trajectory
                
                return {
                    'status': 'ESCAPE_ACHIEVED',
                    'message': 'Phase-lock successful - Escape velocity reached',
                    'steps_to_escape': step,
                    'final_alpha': self.field.alpha,
                    'final_phi': self.field.phi,
                    'final_energy': self.field.total_energy,
                    'trajectory': trajectory,
                    'lift_particles_used': [p.token for p in lift_particles]
                }
        
        # Timeout - escape not achieved
        if verbose:
            print(f"\n⚠️  ESCAPE INCOMPLETE after {max_steps} steps")
            print(f"   Final α = {self.field.alpha:.3f} (target: {self.phase_lock_threshold})")
        
        self.escape_trajectory = trajectory
        
        return {
            'status': 'ESCAPE_INCOMPLETE',
            'message': f'Phase-lock not achieved within {max_steps} steps',
            'final_alpha': self.field.alpha,
            'final_phi': self.field.phi,
            'final_energy': self.field.total_energy,
            'trajectory': trajectory,
            'lift_particles_used': [p.token for p in lift_particles]
        }


def demo_antigravity():
    """Demonstrate Antigravity protocol."""
    print("=== Antigravity Protocol Demo ===\n")
    
    # Create field with a trauma well
    field = SemanticField(gravity_constant=0.5, drag_coefficient=0.05, dt=0.1)
    
    # Add trauma attractor
    trauma = TraumaAttractor.create(
        "Tren de Aragua",
        trauma_mass=120.0,
        position=np.array([5, 5, 0])
    )
    field.add_particle(trauma)
    
    # Add trapped thoughts
    trapped_thoughts = [
        LeiParticle.from_token("Fear", emotional_intensity=0.7, provenance_weight=0.8,
                               position=np.array([4, 4, 0])),
        LeiParticle.from_token("Threat", emotional_intensity=0.6, provenance_weight=0.7,
                               position=np.array([6, 5, 0])),
        LeiParticle.from_token("Danger", emotional_intensity=0.6, provenance_weight=0.7,
                               position=np.array([5, 6, 0]))
    ]
    field.add_particles(trapped_thoughts)
    
    print(f"Initial field state:")
    print(f"  Trauma attractor: '{trauma.token}' (mass={trauma.mass})")
    print(f"  Trapped thoughts: {len(trapped_thoughts)}")
    print(f"  α (Alignment): {field.calculate_alpha():.3f}")
    print(f"  Φ (Coherence): {field.calculate_phi():.3f}\n")
    
    # Create and execute Antigravity protocol
    antigravity = AntigravityProtocol(
        field=field,
        escape_velocity_threshold=75.0,
        phase_lock_threshold=0.85
    )
    
    result = antigravity.execute(max_steps=100, verbose=True)
    
    print("\n" + "="*60)
    print("  ANTIGRAVITY PROTOCOL - RESULTS")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result['status'] == 'ESCAPE_ACHIEVED':
        print(f"Steps to escape: {result['steps_to_escape']}")
        print(f"Coherence tokens used: {', '.join(result['lift_particles_used'])}")
    print(f"Final α: {result['final_alpha']:.3f}")
    print(f"Final Φ: {result['final_phi']:.3f}")
    print("="*60)
    
    print("\n✅ Antigravity Protocol Demo Complete")


if __name__ == '__main__':
    demo_antigravity()
