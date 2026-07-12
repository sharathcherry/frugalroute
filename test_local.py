import nodes
class MockPolicy:
    def prefer_remote(self, cat):
        return False
state = {'task': 'check the latest price of amd stock', 'category': 'qa'}
print(nodes.local(state, MockPolicy()))
