import statistics
import random


class FakeSparkJob:
    def __init__(self, partitions, records_per_partition):
        self.partitions = partitions
        self.records_per_partition = records_per_partition

    def run(self):
        # Simulate partition sizes with some skew
        partition_sizes = []
        for _ in range(self.partitions):
            # Add some randomness to simulate data skew
            size = self.records_per_partition * random.uniform(0.5, 1.5)
            partition_sizes.append(size)

        # Detect skew using standard deviation of partition sizes
        skew_score = statistics.stdev(partition_sizes) if len(partition_sizes) > 1 else 0.0

        # Shuffle cost based on number of partitions
        shuffle_cost = self.partitions * 10.0  # Base shuffle cost per partition

        # Compute time components
        base_cost = 50.0  # Base computation time
        skew_penalty = skew_score * 2.0  # Penalty for data skew
        compute_time = base_cost + skew_penalty + shuffle_cost

        return {
            "compute_time": compute_time,
            "skew_score": skew_score,
            "shuffle_cost": shuffle_cost
        }

