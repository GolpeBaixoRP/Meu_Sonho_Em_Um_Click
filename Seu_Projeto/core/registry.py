class Registry:

    def __init__(self):
        self.modules = {}
        self.pipelines = {}

    def register_module(self, name, module):
        self.modules[name] = module

    def register_pipeline(self, name, flow):
        self.pipelines[name] = flow
