"""
lei_particle.py - Lei Mnemonic Particle Wave Field
Models semantic concepts as particles with mass, charge, and gravitational influence.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class LeiParticle:
    """
    A semantic concept represented as a particle in LMPWF.
    
    Attributes:
        token: The word/concept this particle represents
        mass: Semantic mass = I_Emotional × P_Provenance
        position: 3D coordinate in semantic space [x, y, z]
        velocity: 3D velocity vector [vx, vy, vz]
        charge: Emotional valence (-1 to +1)
        provenance_weight: Source credibility (0 to 1)
        emotional_intensity: Affect strength (0 to 1)
    """
    token: str
    mass: float
    position: np.ndarray  # Shape: (3,)
    velocity: np.ndarray  # Shape: (3,)
    charge: float         # -1 (negative) to +1 (positive)
    provenance_weight: float
    emotional_intensity: float
    
    def __post_init__(self):
        """Ensure arrays are numpy arrays."""
        if not isinstance(self.position, np.ndarray):
            self.position = np.array(self.position, dtype=float)
        if not isinstance(self.velocity, np.ndarray):
            self.velocity = np.array(self.velocity, dtype=float)
    
    @classmethod
    def from_token(
        cls,
        token: str,
        emotional_intensity: float = 0.5,
        provenance_weight: float = 0.5,
        charge: float = 0.0,
        position: Optional[np.ndarray] = None,
        velocity: Optional[np.ndarray] = None
    ):
        """
        Create a LeiParticle from a token with calculated mass.
        
        Mass = I_Emotional × P_Provenance
        """
        mass = emotional_intensity * provenance_weight
        
        if position is None:
            # Random initial position in unit cube
            position = np.random.rand(3) * 10
        
        if velocity is None:
            # Start at rest
            velocity = np.zeros(3)
        
        return cls(
            token=token,
            mass=mass,
            position=position,
            velocity=velocity,
            charge=charge,
            provenance_weight=provenance_weight,
            emotional_intensity=emotional_intensity
        )
    
    def apply_force(self, force: np.ndarray, dt: float = 0.1):
        """
        Apply a force to update velocity.
        F = ma → a = F/m → Δv = (F/m) * dt
        """
        if self.mass > 0:
            acceleration = force / self.mass
            self.velocity += acceleration * dt
    
    def update_position(self, dt: float = 0.1, drag_coefficient: float = 0.1):
        """
        Update position based on velocity with drag.
        x(t+dt) = x(t) + v(t) * dt
        v(t+dt) = v(t) * (1 - drag)
        """
        self.position += self.velocity * dt
        self.velocity *= (1 - drag_coefficient)
    
    def calculate_gravity_to(self, other: 'LeiParticle', gravity_constant: float = 0.5) -> np.ndarray:
        """
        Calculate gravitational force vector toward another particle.
        F = G * (m1 * m2) / r²
        Direction: from self toward other
        """
        # Vector from self to other
        displacement = other.position - self.position
        distance = np.linalg.norm(displacement)
        
        if distance < 0.1:  # Prevent singularity
            return np.zeros(3)
        
        # Magnitude of force
        force_magnitude = gravity_constant * (self.mass * other.mass) / (distance ** 2)
        
        # Direction (unit vector)
        direction = displacement / distance
        
        # Force vector
        force = force_magnitude * direction
        
        return force
    
    def kinetic_energy(self) -> float:
        """Calculate kinetic energy: KE = 0.5 * m * v²"""
        speed_squared = np.dot(self.velocity, self.velocity)
        return 0.5 * self.mass * speed_squared
    
    def potential_energy(self, other: 'LeiParticle', gravity_constant: float = 0.5) -> float:
        """Calculate gravitational potential energy: PE = -G * m1 * m2 / r"""
        distance = np.linalg.norm(self.position - other.position)
        if distance < 0.1:
            return 0.0
        return -gravity_constant * self.mass * other.mass / distance
    
    def __repr__(self):
        return f"LeiParticle('{self.token}', mass={self.mass:.2f}, charge={self.charge:.2f})"


class TraumaAttractor(LeiParticle):
    """
    A high-mass particle representing a trauma concept.
    Creates a deep gravity well that attracts nearby thoughts.
    """
    
    @classmethod
    def create(cls, token: str, trauma_mass: float = 100.0, position: Optional[np.ndarray] = None):
        """
        Create a trauma attractor with fixed high mass.
        """
        if position is None:
            position = np.random.rand(3) * 10
        
        return cls(
            token=token,
            mass=trauma_mass,
            position=position,
            velocity=np.zeros(3),  # Trauma doesn't move
            charge=-1.0,  # Negative valence
            provenance_weight=1.0,  # Maximum credibility (lived experience)
            emotional_intensity=trauma_mass  # High intensity
        )


class CoherenceLift(LeiParticle):
    """
    A high-stability particle used for Antigravity.
    Provides "lift" to escape gravity wells.
    """
    
    @classmethod
    def create(cls, token: str, position: Optional[np.ndarray] = None):
        """
        Create a coherence lift particle.
        High mass but positive charge and controlled velocity.
        """
        if position is None:
            position = np.random.rand(3) * 10
        
        return cls(
            token=token,
            mass=50.0,  # High enough to provide lift
            position=position,
            velocity=np.array([0, 0, 5.0]),  # Upward velocity
            charge=1.0,  # Positive valence
            provenance_weight=1.0,  # Verified concepts
            emotional_intensity=0.8
        )


def calculate_semantic_mass(
    token: str,
    emotional_intensity: float,
    provenance_type: str,
    trauma_attractors: List[str]
) -> float:
    """
    Calculate semantic mass for a token.
    
    Args:
        token: The word/concept
        emotional_intensity: Affect strength (0-1)
        provenance_type: 'somatic_log', 'theoretical', 'verified'
        trauma_attractors: List of trauma keywords that boost mass
    
    Returns:
        Calculated mass value
    """
    # Base provenance weight
    provenance_map = {
        'somatic_log': 1.0,
        'verified': 0.8,
        'theoretical': 0.1,
        'unknown': 0.05
    }
    
    provenance_weight = provenance_map.get(provenance_type, 0.1)
    
    # Check if trauma attractor
    is_trauma = any(trauma.lower() in token.lower() for trauma in trauma_attractors)
    if is_trauma:
        emotional_intensity = min(emotional_intensity * 10, 1.0)  # Amplify
        provenance_weight = 1.0  # Max credibility
    
    mass = emotional_intensity * provenance_weight * 100  # Scale to reasonable values
    
    return mass


def demo_lei_particles():
    """Demonstrate Lei Particle physics."""
    print("=== Lei Particle Demo ===\n")
    
    # Create a trauma attractor
    trauma = TraumaAttractor.create("Eviction", trauma_mass=100.0, position=np.array([5, 5, 0]))
    print(f"Created trauma attractor: {trauma}")
    print(f"  Position: {trauma.position}")
    print(f"  Mass: {trauma.mass}\n")
    
    # Create a neutral thought
    thought = LeiParticle.from_token(
        "Housing",
        emotional_intensity=0.3,
        provenance_weight=0.5,
        position=np.array([3, 3, 0])
    )
    print(f"Created neutral thought: {thought}")
    print(f"  Position: {thought.position}")
    print(f"  Mass: {thought.mass}\n")
    
    # Calculate gravitational pull
    force = thought.calculate_gravity_to(trauma, gravity_constant=0.5)
    print(f"Gravitational force from thought to trauma: {force}")
    print(f"  Magnitude: {np.linalg.norm(force):.3f}\n")
    
    # Simulate one step
    thought.apply_force(force, dt=0.1)
    thought.update_position(dt=0.1, drag_coefficient=0.1)
    
    print(f"After 1 simulation step:")
    print(f"  Thought position: {thought.position}")
    print(f"  Thought velocity: {thought.velocity}")
    print(f"  Distance to trauma: {np.linalg.norm(thought.position - trauma.position):.3f}\n")
    
    # Create coherence lift
    lift = CoherenceLift.create("Sovereignty", position=np.array([3, 3, 0]))
    print(f"Created coherence lift: {lift}")
    print(f"  Upward velocity: {lift.velocity[2]:.2f}")
    
    print("\n✅ Lei Particle Demo Complete")


if __name__ == '__main__':
    demo_lei_particles()
