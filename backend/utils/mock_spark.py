class FakeSparkJob:
    def __init__(self, partitions, records_per_partition):
        self.partitions = partitions
        self.records_per_partition = records_per_partition

    def run(self):
        pass
