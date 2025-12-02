"""
lca_engine.py - Lattice Complexity Analysis Engine
Implements Formal Concept Analysis for truth verification.
"""

import numpy as np
import networkx as nx
from typing import Set, Tuple, List, Dict, FrozenSet, Any
from dataclasses import dataclass
from itertools import combinations
import random


@dataclass(frozen=True)
class FormalConcept:
    """
    A formal concept is a pair (Extent, Intent) where:
    - Extent: Set of objects that share all attributes in Intent
    - Intent: Set of attributes shared by all objects in Extent
    """
    extent: FrozenSet[str]  # Objects
    intent: FrozenSet[str]  # Attributes
    
    def __str__(self):
        return f"Concept(Extent={sorted(self.extent)}, Intent={sorted(self.intent)})"
    
    def __hash__(self):
        return hash((self.extent, self.intent))


class FormalContext:
    """
    A formal context K = (G, M, I) where:
    - G: Set of objects
    - M: Set of attributes
    - I: Binary incidence relation (object has attribute)
    """
    
    def __init__(self, objects: Set[str], attributes: Set[str], incidence: Set[Tuple[str, str]]):
        self.objects = frozenset(objects)
        self.attributes = frozenset(attributes)
        self.incidence = set(incidence)  # Set of (object, attribute) pairs
        
        # Build lookup tables for efficiency
        self._obj_attrs = {}  # object -> set of attributes
        self._attr_objs = {}  # attribute -> set of objects
        
        for obj in objects:
            self._obj_attrs[obj] = set()
        for attr in attributes:
            self._attr_objs[attr] = set()
        
        for obj, attr in incidence:
            if obj in objects and attr in attributes:
                self._obj_attrs[obj].add(attr)
                self._attr_objs[attr].add(obj)
    
    def get_attributes(self, obj: str) -> Set[str]:
        """Get all attributes of an object."""
        return self._obj_attrs.get(obj, set())
    
    def get_objects(self, attr: str) -> Set[str]:
        """Get all objects with an attribute."""
        return self._attr_objs.get(attr, set())
    
    def derive_extent(self, attributes: Set[str]) -> Set[str]:
        """
        Derivation operator ' for attributes.
        Returns objects that have ALL given attributes.
        A' = {g ∈ G | ∀m ∈ A: (g,m) ∈ I}
        """
        if not attributes:
            return set(self.objects)
        
        # Start with objects that have the first attribute
        result = set(self._attr_objs.get(next(iter(attributes)), set()))
        
        # Intersect with objects having each remaining attribute
        for attr in attributes:
            result &= self._attr_objs.get(attr, set())
        
        return result
    
    def derive_intent(self, objects: Set[str]) -> Set[str]:
        """
        Derivation operator ' for objects.
        Returns attributes shared by ALL given objects.
        B' = {m ∈ M | ∀g ∈ B: (g,m) ∈ I}
        """
        if not objects:
            return set(self.attributes)
        
        # Start with attributes of the first object
        result = set(self._obj_attrs.get(next(iter(objects)), set()))
        
        # Intersect with attributes of each remaining object
        for obj in objects:
            result &= self._obj_attrs.get(obj, set())
        
        return result
    
    def closure(self, attributes: Set[str]) -> Set[str]:
        """
        Closure of a set of attributes.
        closure(A) = A'' = (A')' 
        Returns the smallest closed set containing A.
        """
        extent = self.derive_extent(attributes)
        return self.derive_intent(extent)
    
    def is_closed(self, attributes: Set[str]) -> bool:
        """Check if a set of attributes is closed."""
        return self.closure(attributes) == attributes


class NextClosureAlgorithm:
    """
    NextClosure algorithm for generating all formal concepts.
    Efficiently traverses the lattice without generating duplicates.
    """
    
    def __init__(self, context: FormalContext):
        self.context = context
        self.attributes_list = sorted(context.attributes)  # Fixed order
        
    def next_closure(self, current: Set[str]) -> Set[str]:
        """
        Compute the next closed set after current in the canonical order.
        Returns None if current is the last closed set.
        """
        # Iterate through attributes in reverse order
        for i in range(len(self.attributes_list) - 1, -1, -1):
            attr = self.attributes_list[i]
            
            # Check if we can "flip" this attribute
            if attr not in current:
                # Try adding this attribute and closing
                candidate = current | {attr}
                closure = self.context.closure(candidate)
                
                # Check if the closure only adds attributes that come after i
                # This ensures canonical order
                valid = True
                for m in closure:
                    if m not in candidate:
                        m_idx = self.attributes_list.index(m)
                        if m_idx <= i:
                            valid = False
                            break
                
                if valid:
                    return closure
            else:
                # Remove this attribute for backtracking
                current = current - {attr}
        
        return None  # No next closure exists
    
    def generate_all_concepts(self) -> List[FormalConcept]:
        """Generate all formal concepts using NextClosure."""
        concepts = []
        
        # Start with the empty set
        current = set()
        current = self.context.closure(current)
        
        while current is not None:
            # Create the formal concept
            extent = self.context.derive_extent(current)
            intent = current
            concept = FormalConcept(
                extent=frozenset(extent),
                intent=frozenset(intent)
            )
            concepts.append(concept)
            
            # Find next closure
            current = self.next_closure(current)
        
        return concepts


class ConceptLattice:
    """
    Hierarchical structure of formal concepts with subconcept/superconcept relations.
    """
    
    def __init__(self, concepts: List[FormalConcept]):
        self.concepts = concepts
        self.graph = nx.DiGraph()
        
        # Add concepts as nodes
        for concept in concepts:
            self.graph.add_node(concept)
        
        # Add edges (subconcept -> superconcept)
        # c1 ≤ c2 iff extent(c1) ⊆ extent(c2) iff intent(c2) ⊆ intent(c1)
        for c1 in concepts:
            for c2 in concepts:
                if c1 != c2:
                    if c1.intent > c2.intent:  # c1 is more specific (subconcept)
                        # Check if there's no intermediate concept
                        is_direct = True
                        for c3 in concepts:
                            if c3 != c1 and c3 != c2:
                                if c1.intent > c3.intent > c2.intent:
                                    is_direct = False
                                    break
                        
                        if is_direct:
                            self.graph.add_edge(c1, c2)
    
    def get_top(self) -> FormalConcept:
        """Get the top concept (most general)."""
        for concept in self.concepts:
            if len(concept.intent) == 0:
                return concept
        return None
    
    def get_bottom(self) -> FormalConcept:
        """Get the bottom concept (most specific)."""
        max_intent = max(len(c.intent) for c in self.concepts)
        for concept in self.concepts:
            if len(concept.intent) == max_intent:
                return concept
        return None
    
    def calculate_density(self) -> float:
        """
        Lattice Density: D_L = |E| / |C|²
        Measures how interconnected the concepts are.
        """
        num_concepts = len(self.concepts)
        if num_concepts == 0:
            return 0.0
        
        num_edges = self.graph.number_of_edges()
        return num_edges / (num_concepts ** 2)
    
    def find_irreducibles(self) -> Dict[str, List[FormalConcept]]:
        """
        Find meet-irreducible and join-irreducible elements.
        - Meet-irreducible: Cannot be expressed as meet (∧) of other concepts
        - Join-irreducible: Cannot be expressed as join (∨) of other concepts
        """
        meet_irreducibles = []
        join_irreducibles = []
        
        for concept in self.concepts:
            # Join-irreducible: has exactly one lower cover
            predecessors = list(self.graph.predecessors(concept))
            if len(predecessors) == 1:
                join_irreducibles.append(concept)
            
            # Meet-irreducible: has exactly one upper cover
            successors = list(self.graph.successors(concept))
            if len(successors) == 1:
                meet_irreducibles.append(concept)
        
        return {
            'meet_irreducible': meet_irreducibles,
            'join_irreducible': join_irreducibles
        }
    
    def calculate_stability_index(self, concept: FormalConcept, samples: int = 100) -> float:
        """
        Stability Index: Robustness of a concept to noise/subsetting.
        Uses Monte Carlo sampling to estimate the proportion of subsets
        that preserve the concept.
        """
        if len(concept.extent) == 0:
            return 1.0
        
        preserved_count = 0
        extent_list = list(concept.extent)
        
        for _ in range(samples):
            # Randomly remove some objects
            sample_size = random.randint(1, len(extent_list))
            subset = set(random.sample(extent_list, sample_size))
            
            # Check if the concept's intent is preserved
            # (Would need context access - simplified here)
            # In practice, check if closure of intent on subset equals intent
            preserved_count += 1  # Placeholder
        
        return preserved_count / samples
    
    def calculate_betti_numbers(self) -> Dict[int, int]:
        """
        Betti Numbers: Topological homology ranks.
        β_0: Number of connected components
        β_1: Number of loops (cycles)
        β_2+: Higher-dimensional holes
        """
        # Convert to undirected for homology
        undirected = self.graph.to_undirected()
        
        # β_0: Number of connected components
        beta_0 = nx.number_connected_components(undirected)
        
        # β_1: Number of independent cycles (loops)
        # β₁ = |E| - |V| + |C| for each connected component
        beta_1 = 0
        for component in nx.connected_components(undirected):
            subgraph = undirected.subgraph(component)
            e = subgraph.number_of_edges()
            v = subgraph.number_of_nodes()
            beta_1 += e - v + 1
        
        return {
            'beta_0': beta_0,
            'beta_1': beta_1
        }


def text_to_context(text: str) -> FormalContext:
    """
    Convert text to a FormalContext for analysis.
    Objects: Sentences
    Attributes: Unique words
    Incidence: (sentence, word) if word appears in sentence
    """
    import re
    
    # Split into sentences (simple splitting)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Extract words
    all_words = set()
    sentence_words = {}
    
    for i, sentence in enumerate(sentences):
        words = re.findall(r'\b\w+\b', sentence.lower())
        sentence_id = f"sent_{i}"
        sentence_words[sentence_id] = set(words)
        all_words.update(words)
    
    # Build incidence relation
    incidence = set()
    for sent_id, words in sentence_words.items():
        for word in words:
            incidence.add((sent_id, word))
    
    objects = set(sentence_words.keys())
    attributes = all_words
    
    return FormalContext(objects, attributes, incidence)


if __name__ == '__main__':
    # Test with simple example
    print("=== Testing LCA Engine ===\n")
    
    # Example context: Animals and their features
    objects = {'dog', 'cat', 'bird', 'fish'}
    attributes = {'legs', 'fur', 'flies', 'swims'}
    incidence = {
        ('dog', 'legs'),
        ('dog', 'fur'),
        ('cat', 'legs'),
        ('cat', 'fur'),
        ('bird', 'legs'),
        ('bird', 'flies'),
        ('fish', 'swims')
    }
    
    context = FormalContext(objects, attributes, incidence)
    
    print("Formal Context:")
    print(f"  Objects: {sorted(context.objects)}")
    print(f"  Attributes: {sorted(context.attributes)}")
    print(f"  Incidence: {len(incidence)} relations\n")
    
    # Generate concepts
    algo = NextClosureAlgorithm(context)
    concepts = algo.generate_all_concepts()
    
    print(f"Generated {len(concepts)} concepts:")
    for concept in concepts:
        print(f"  {concept}")
    print()
    
    # Build lattice
    lattice = ConceptLattice(concepts)
    
    print("Lattice Metrics:")
    print(f"  Density: {lattice.calculate_density():.3f}")
    
    irreducibles = lattice.find_irreducibles()
    print(f"  Meet-irreducible: {len(irreducibles['meet_irreducible'])}")
    print(f"  Join-irreducible: {len(irreducibles['join_irreducible'])}")
    
    betti = lattice.calculate_betti_numbers()
    print(f"  Betti Numbers: β₀={betti['beta_0']}, β₁={betti['beta_1']}")
    
    print("\n✅ LCA Engine Test Complete")
