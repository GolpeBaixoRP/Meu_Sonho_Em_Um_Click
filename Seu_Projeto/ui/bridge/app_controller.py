class AppController:

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def execute(self, pipeline_name, context=None):
        if context is None:
            context = {}
        return self.orchestrator.execute(pipeline_name, context)
