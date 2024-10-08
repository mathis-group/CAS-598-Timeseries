import numpy as np
from itertools import permutations
from collections import Counter
import math

class PermutationEntropy:
    def __init__(self, timeseries, K):
        """Initialize with time series and K (embedding dimension)."""
        if not isinstance(timeseries, np.ndarray):
            raise ValueError("Time series must be a numpy array")
        if K >= len(timeseries):
            raise ValueError("K must be less than the length of the time series")

        self.timeseries = timeseries
        self.K = K
        self.n = len(timeseries)
        self.ordinals = list(permutations(range(K)))
        self.patterns = self._get_patterns()  #  orderings of K elements
        self.pe = self.compute_entropy()

    def _get_patterns(self):
        """Extract the ordinal patterns from the time series."""
        patterns = []
        for i in range(self.n - self.K + 1):
            subseq = self.timeseries[i:i + self.K]
            # Get the indices that would sort the array, i.e., its ordinal pattern
            pattern = tuple(np.argsort(subseq))
            patterns.append(pattern)
        pattern_counts = Counter(patterns)
        # Force all patterns to occur in counter, even if they're missing in the timseries (dumb for large K)
        found_patterns = set(pattern_counts.keys())
        missing_patterns = [o for o in self.ordinals if o not in found_patterns]
        for m in missing_patterns:
            pattern_counts[m] = 0

        return pattern_counts  # Return a dictionary of pattern frequencies


    def compute_entropy(self):
        """Compute permutation entropy."""
        # Get all ordinal patterns
        pattern_counts = self.patterns

        # Calculate the probability distribution
        total_patterns = sum(pattern_counts.values())
        probabilities = [count / total_patterns for count in pattern_counts.values()]

        # Compute the entropy (Shannon entropy)
        indiv_contributions = [-p* math.log(p, 2) for p in probabilities if p > 0]
        entropy = sum(indiv_contributions)/math.log(len(self.ordinals), 2)
        return entropy

if __name__ == "__main__":
    from lorenz import lorenz_ts

    # Example usage:
    timeseries, _, _, t = lorenz_ts([1.0, 1.0, 1.0], 50, 10000) # np.random.rand(100)  
    random_ts = np.random.choice(timeseries, len(timeseries), replace=False) # Random time series for testing
    K = 5  # Embedding dimension

    lorenz_pe = PermutationEntropy(timeseries, K)
    entropy_value = lorenz_pe.compute_entropy()

    print(f"Lorenz Permutation Entropy: {entropy_value}")

    rand_pe = PermutationEntropy(random_ts, K)
    entropy_value = rand_pe.compute_entropy()

    print(f"Random Permutation Entropy: {entropy_value}")