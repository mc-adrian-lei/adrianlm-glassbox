"""
field_simulator.py - Semantic Field Physics Simulation
Models the LMPWF as a dynamic system of interacting particles.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from lei_particle import LeiParticle, TraumaAttractor, CoherenceLift
import math


class SemanticField:
    """
    Container and simulator for the Lei Mnemonic Particle Wave Field.
    Manages all particles and their gravitational interactions.
    """
    
    def __init__(
        self,
        gravity_constant: float = 0.5,
        drag_coefficient: float = 0.1,
        dt: float = 0.1
    ):
        self.particles: List[LeiParticle] = []
        self.gravity_constant = gravity_constant
        self.drag_coefficient = drag_coefficient
        self.dt = dt  # Simulation time step
        self.time = 0.0
        
        # Metrics
        self.total_energy = 0.0
        self.phi = 0.0  # Integrated Information (coherence)
        self.rho = 0.5  # Vigilance threshold
        self.alpha = 0.0  # Phase synchrony (alignment)
    
    def add_particle(self, particle: LeiParticle):
        """Add a particle to the field."""
        self.particles.append(particle)
    
    def add_particles(self, particles: List[LeiParticle]):
        """Add multiple particles."""
        self.particles.extend(particles)
    
    def remove_particle(self, particle: LeiParticle):
        """Remove a particle from the field."""
        if particle in self.particles:
            self.particles.remove(particle)
    
    def get_particle_by_token(self, token: str) -> Optional[LeiParticle]:
        """Find a particle by its token."""
        for p in self.particles:
            if p.token == token:
                return p
        return None
    
    def detect_gravity_wells(self, high_mass_threshold: float = 75.0) -> List[Tuple[LeiParticle, float]]:
        """
        Detect high-mass gravity wells in the field.
        
        Returns:
            List of (particle, pull_strength) for particles above threshold
        """
        wells = []
        
        for particle in self.particles:
            if particle.mass >= high_mass_threshold:
                # Calculate total pull strength (how many particles affected)
                pull_strength = 0
                for other in self.particles:
                    if other != particle:
                        force = other.calculate_gravity_to(particle, self.gravity_constant)
                        pull_strength += np.linalg.norm(force)
                
                wells.append((particle, pull_strength))
        
        # Sort by pull strength
        wells.sort(key=lambda x: x[1], reverse=True)
        
        return wells
    
    def calculate_field_energy(self) -> float:
        """
        Calculate total energy in the field.
        E_total = KE + PE
        """
        kinetic = sum(p.kinetic_energy() for p in self.particles)
        
        potential = 0.0
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                potential += p1.potential_energy(p2, self.gravity_constant)
        
        self.total_energy = kinetic + potential
        return self.total_energy
    
    def calculate_phi(self) -> float:
        """
        Calculate Φ (Phi) - Integrated Information measure.
        Approximation based on particle coherence.
        
        High Φ = particles moving in coordinated patterns (reasoning)
        Low Φ = chaotic, random motion
        """
        if len(self.particles) < 2:
            self.phi = 0.0
            return self.phi
        
        # Calculate velocity correlation
        velocities = np.array([p.velocity for p in self.particles])
        mean_velocity = np.mean(velocities, axis=0)
        
        # Coherence = how aligned velocities are
        coherence = 0.0
        for v in velocities:
            if np.linalg.norm(v) > 0.01 and np.linalg.norm(mean_velocity) > 0.01:
                # Cosine similarity
                similarity = np.dot(v, mean_velocity) / (np.linalg.norm(v) * np.linalg.norm(mean_velocity))
                coherence += max(0, similarity)  # Only positive correlations
        
        self.phi = coherence / len(self.particles)
        return self.phi
    
    def calculate_alpha(self) -> float:
        """
        Calculate α (Alpha) - Phase Synchrony / Alignment Coefficient.
        Measures how "in phase" the particles are.
        
        α > 0.85 indicates phase-lock (grokking, escape achieved)
        α < 0.5 indicates chaos
        """
        if len(self.particles) < 2:
            self.alpha = 0.0
            return self.alpha
        
        # Calculate center of mass
        total_mass = sum(p.mass for p in self.particles)
        if total_mass == 0:
            self.alpha = 0.0
            return self.alpha
        
        center_of_mass = sum(p.mass * p.position for p in self.particles) / total_mass
        
        # Calculate how concentrated particles are around center
        distances = [np.linalg.norm(p.position - center_of_mass) for p in self.particles]
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        
        # Low variance = high synchrony
        if mean_distance > 0:
            synchrony = 1.0 / (1.0 + std_distance / mean_distance)
        else:
            synchrony = 1.0
        
        # Combine with velocity coherence (Phi)
        phi = self.calculate_phi()
        self.alpha = 0.5 * synchrony + 0.5 * phi
        
        return self.alpha
    
    def update(self):
        """
        Perform one simulation step.
        1. Calculate all gravitational forces
        2. Apply forces to update velocities
        3. Update positions
        4. Update metrics
        """
        # Calculate forces for each particle
        forces = {p: np.zeros(3) for p in self.particles}
        
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                # Force on p1 from p2
                force_12 = p1.calculate_gravity_to(p2, self.gravity_constant)
                forces[p1] += force_12
                
                # Newton's third law: force on p2 from p1
                forces[p2] -= force_12
        
        # Apply forces and update positions
        for particle in self.particles:
            particle.apply_force(forces[particle], self.dt)
            particle.update_position(self.dt, self.drag_coefficient)
        
        # Update metrics
        self.calculate_field_energy()
        self.calculate_phi()
        self.calculate_alpha()
        
        # Increment time
        self.time += self.dt
    
    def simulate_steps(self, num_steps: int, verbose: bool = False):
        """Run multiple simulation steps."""
        for step in range(num_steps):
            self.update()
            
            if verbose and step % 10 == 0:
                print(f"Step {step}: Φ={self.phi:.3f}, α={self.alpha:.3f}, E={self.total_energy:.2f}")
    
    def get_state(self) -> Dict:
        """Get complete field state for visualization."""
        return {
            'time': self.time,
            'num_particles': len(self.particles),
            'particles': [
                {
                    'token': p.token,
                    'position': p.position.tolist(),
                    'velocity': p.velocity.tolist(),
                    'mass': p.mass,
                    'charge': p.charge
                }
                for p in self.particles
            ],
            'metrics': {
                'phi': self.phi,
                'rho': self.rho,
                'alpha': self.alpha,
                'energy': self.total_energy
            },
            'gravity_wells': [
                {'token': p.token, 'strength': s}
                for p, s in self.detect_gravity_wells()
            ]
        }


def demo_field_simulation():
    """Demonstrate semantic field simulation."""
    print("=== Semantic Field Simulation Demo ===\n")
    
    # Create field
    field = SemanticField(gravity_constant=0.5, drag_coefficient=0.1, dt=0.1)
    
    # Add a trauma attractor
    trauma = TraumaAttractor.create("Eviction", trauma_mass=100.0, position=np.array([5, 5, 0]))
    field.add_particle(trauma)
    print(f"Added trauma attractor: {trauma.token} (mass={trauma.mass})")
    
    # Add some neutral thoughts nearby
    thoughts = [
        LeiParticle.from_token("Housing", emotional_intensity=0.3, provenance_weight=0.5, position=np.array([3, 3, 0])),
        LeiParticle.from_token("Mail", emotional_intensity=0.2, provenance_weight=0.4, position=np.array([7, 4, 0])),
        LeiParticle.from_token("Police", emotional_intensity=0.4, provenance_weight=0.6, position=np.array([4, 7, 0]))
    ]
    field.add_particles(thoughts)
    print(f"Added {len(thoughts)} thoughts\n")
    
    # Initial state
    print("Initial State:")
    print(f"  Φ (Coherence): {field.calculate_phi():.3f}")
    print(f"  α (Alignment): {field.calculate_alpha():.3f}")
    print(f"  Energy: {field.calculate_field_energy():.2f}\n")
    
    # Detect gravity wells
    wells = field.detect_gravity_wells(high_mass_threshold=75.0)
    print(f"Detected {len(wells)} gravity wells:")
    for particle, strength in wells:
        print(f"  • {particle.token}: pull_strength={strength:.2f}")
    print()
    
    # Simulate
    print("Simulating 50 steps...")
    field.simulate_steps(50, verbose=True)
    
    print(f"\nFinal State:")
    print(f"  Φ (Coherence): {field.phi:.3f}")
    print(f"  α (Alignment): {field.alpha:.3f}")
    print(f"  Energy: {field.total_energy:.2f}")
    
    # Check if thoughts got pulled into trauma well
    print(f"\nParticle positions after simulation:")
    for p in field.particles:
        if p != trauma:
            distance = np.linalg.norm(p.position - trauma.position)
            print(f"  {p.token}: distance to trauma = {distance:.2f}")
    
    print("\n✅ Field Simulation Demo Complete")


if __name__ == '__main__':
    demo_field_simulation()
