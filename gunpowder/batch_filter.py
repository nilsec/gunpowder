import copy
from batch_provider import BatchProvider

class BatchFilter(BatchProvider):
    '''Convenience wrapper for BatchProviders with exactly one input provider.

    Subclasses need to implement at least 'process' to modify a passed batch 
    (downstream). Optionally, the following methods can be implemented:

        initialize

            Initialize this filter. Called after setup of the DAG. All upstream 
            providers will be initialized already.

        get_spec

            Get the spec of this provider. If not implemented, the upstream 
            provider spec is used.

        prepare

            Prepare for a batch request. Always called before each 
            'request_batch'. Use it to modify a batch spec to be passed 
            upstream.
    '''

    def get_upstream_provider(self):
        assert len(self.get_upstream_providers()) == 1, "BatchFilters need to have exactly one upstream provider"
        return self.get_upstream_providers()[0]

    def get_spec(self):
        return self.get_upstream_provider().get_spec()

    def request_batch(self, batch_spec):

        self.prepare(batch_spec)
        batch = self.get_upstream_provider().request_batch(batch_spec)
        self.process(batch)

        return batch

    def prepare(self, batch_spec):
        '''To be implemented in subclasses.

        Prepare for a batch request. Change the batch_spec as needed, it will be 
        passed on upstream.
        '''
        pass

    def process(self, batch):
        '''To be implemented in subclasses.

        Filter a batch, will be called after 'prepare'. Change batch and its 
        spec as needed, it will be passed downstream.
        '''
        raise RuntimeError("Class %s does not implement 'process'"%self.__class__)

