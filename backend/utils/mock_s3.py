class FakeS3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage = {}

    def put_object(self):
        pass

    def get_object(self):
        pass
