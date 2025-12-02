"""
truth_verifier.py - Truth Verification via Topological Isomorphism
Detects AI hallucinations by comparing lattice structures.
"""

import re
from typing import Dict, List, Set, Tuple, Any
from lca_engine import (
    FormalContext, 
    NextClosureAlgorithm, 
    ConceptLattice,
    FormalConcept,
    text_to_context
)
import networkx as nx


class TruthVerifier:
    """
    Verifies AI-generated responses against source citations using
    topological entailment rather than semantic similarity.
    """
    
    def __init__(self):
        self.ground_truth_lattice = None
        self.answer_lattice = None
        self.ground_truth_context = None
        self.answer_context = None
    
    def build_ground_truth_lattice(self, citations: List[str]) -> ConceptLattice:
        """
        Build lattice strictly from source citation text.
        This represents the "Ground Truth" topology.
        """
        # Combine all citations
        combined_text = " ".join(citations)
        
        # Convert to formal context
        self.ground_truth_context = text_to_context(combined_text)
        
        # Generate concepts
        algo = NextClosureAlgorithm(self.ground_truth_context)
        concepts = algo.generate_all_concepts()
        
        # Build lattice
        self.ground_truth_lattice = ConceptLattice(concepts)
        
        return self.ground_truth_lattice
    
    def build_answer_lattice(self, answer_text: str) -> ConceptLattice:
        """
        Build lattice from AI's proposed answer.
        This represents the "Answer" topology to verify.
        """
        # Convert to formal context
        self.answer_context = text_to_context(answer_text)
        
        # Generate concepts
        algo = NextClosureAlgorithm(self.answer_context)
        concepts = algo.generate_all_concepts()
        
        # Build lattice
        self.answer_lattice = ConceptLattice(concepts)
        
        return self.answer_lattice
    
    def extract_relationships(self, lattice: ConceptLattice) -> Set[Tuple[str, str]]:
        """
        Extract attribute-to-attribute relationships from lattice.
        Returns set of (attr1, attr2) pairs where attr1 -> attr2 entailment exists.
        """
        relationships = set()
        
        for concept in lattice.concepts:
            # Get parent concepts (more general)
            for parent in lattice.graph.successors(concept):
                # Attributes in child but not parent represent entailment
                child_attrs = concept.intent
                parent_attrs = parent.intent
                
                # Attributes that appear together
                for attr1 in child_attrs:
                    for attr2 in child_attrs:
                        if attr1 != attr2:
                            relationships.add((attr1, attr2))
        
        return relationships
    
    def check_topological_isomorphism(self) -> Dict[str, Any]:
        """
        Check if answer lattice structure is preserved by (embeds into) 
        ground truth lattice.
        
        Returns dict with:
        - is_valid: bool
        - hallucinated_edges: list of (attr1, attr2) not in ground truth
        - confidence: float (0-1)
        """
        if not self.ground_truth_lattice or not self.answer_lattice:
            return {
                'is_valid': False,
                'error': 'Lattices not built',
                'hallucinated_edges': [],
                'confidence': 0.0
            }
        
        # Extract relationships from both lattices
        gt_relationships = self.extract_relationships(self.ground_truth_lattice)
        ans_relationships = self.extract_relationships(self.answer_lattice)
        
        # Find hallucinated relationships (in answer but not in ground truth)
        hallucinated = []
        for attr1, attr2 in ans_relationships:
            if (attr1, attr2) not in gt_relationships:
                # Check if these attributes even exist in ground truth
                gt_attrs = self.ground_truth_context.attributes
                if attr1 in gt_attrs and attr2 in gt_attrs:
                    # Both attributes exist but relationship doesn't
                    hallucinated.append((attr1, attr2))
        
        # Calculate confidence
        if len(ans_relationships) == 0:
            confidence = 1.0  # No claims made
        else:
            # Confidence = proportion of valid relationships
            valid_count = len(ans_relationships) - len(hallucinated)
            confidence = valid_count / len(ans_relationships)
        
        is_valid = len(hallucinated) == 0
        
        return {
            'is_valid': is_valid,
            'hallucinated_edges': hallucinated,
            'confidence': confidence,
            'ground_truth_concepts': len(self.ground_truth_lattice.concepts),
            'answer_concepts': len(self.answer_lattice.concepts),
            'ground_truth_relationships': len(gt_relationships),
            'answer_relationships': len(ans_relationships)
        }
    
    def verify(self, citations: List[str], answer: str) -> Dict[str, Any]:
        """
        Main verification method.
        Returns comprehensive analysis of answer validity.
        """
        # Build both lattices
        self.build_ground_truth_lattice(citations)
        self.build_answer_lattice(answer)
        
        # Check isomorphism
        result = self.check_topological_isomorphism()
        
        # Add lattice metrics
        gt_metrics = {
            'density': self.ground_truth_lattice.calculate_density(),
            'betti': self.ground_truth_lattice.calculate_betti_numbers(),
            'irreducibles': self.ground_truth_lattice.find_irreducibles()
        }
        
        ans_metrics = {
            'density': self.answer_lattice.calculate_density(),
            'betti': self.answer_lattice.calculate_betti_numbers(),
            'irreducibles': self.answer_lattice.find_irreducibles()
        }
        
        result['ground_truth_metrics'] = gt_metrics
        result['answer_metrics'] = ans_metrics
        
        return result


class HallucinationDetector:
    """
    High-level interface for hallucination detection.
    """
    
    def __init__(self):
        self.verifier = TruthVerifier()
    
    def detect(self, sources: List[str], generated_text: str) -> Dict[str, Any]:
        """
        Detect hallucinations in generated text given source documents.
        
        Args:
            sources: List of source citation texts (ground truth)
            generated_text: AI-generated response to verify
        
        Returns:
            Dict with validation results and flagged hallucinations
        """
        result = self.verifier.verify(sources, generated_text)
        
        # Format output
        output = {
            'status': 'VALID' if result['is_valid'] else 'HALLUCINATION_DETECTED',
            'confidence': result['confidence'],
            'hallucinations': []
        }
        
        if not result['is_valid']:
            for attr1, attr2 in result['hallucinated_edges']:
                output['hallucinations'].append({
                    'type': 'topological_hallucination',
                    'description': f"Invented relationship: '{attr1}' -> '{attr2}'",
                    'severity': 'HIGH'
                })
        
        # Add structural warnings
        gt_complexity = result['ground_truth_metrics']['betti']['beta_1']
        ans_complexity = result['answer_metrics']['betti']['beta_1']
        
        if ans_complexity > gt_complexity * 2:
            output['warnings'] = ['Answer contains significantly more loops than source (potential overgeneralization)']
        
        return output


def demo_hallucination_detection():
    """Demonstrate hallucination detection."""
    print("=== Truth Verification Demo ===\n")
    
    # Ground truth (source)
    sources = [
        "The sky is blue during the day.",
        "Clouds are white or gray.",
        "The sun is yellow and bright."
    ]
    
    # Valid answer
    valid_answer = "The sky is blue and contains white clouds. The sun is bright."
    
    # Hallucinated answer
    hallucinated_answer = "The sky is blue and green. Stars are visible during the day."
    
    detector = HallucinationDetector()
    
    print("Testing VALID answer:")
    print(f"  Answer: {valid_answer}")
    result1 = detector.detect(sources, valid_answer)
    print(f"  Status: {result1['status']}")
    print(f"  Confidence: {result1['confidence']:.2f}\n")
    
    print("Testing HALLUCINATED answer:")
    print(f"  Answer: {hallucinated_answer}")
    result2 = detector.detect(sources, hallucinated_answer)
    print(f"  Status: {result2['status']}")
    print(f"  Confidence: {result2['confidence']:.2f}")
    if result2['hallucinations']:
        print("  Detected hallucinations:")
        for h in result2['hallucinations']:
            print(f"    • {h['description']}")
    
    print("\n✅ Truth Verification Demo Complete")


if __name__ == '__main__':
    demo_hallucination_detection()
