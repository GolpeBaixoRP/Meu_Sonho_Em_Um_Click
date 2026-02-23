from core.logger import Logger
from core.middleware import ContextMiddleware
from core.event_bus import EventBus

class Orchestrator:

    def __init__(self, registry):
        self.registry = registry
        self.event_bus = EventBus()

    def execute(self, pipeline_name, context):
        ContextMiddleware.validate(context)
        Logger.log(f"Starting pipeline: {pipeline_name}")

        for step in self.registry.pipelines.get(pipeline_name, []):
            module = self.registry.modules.get(step)
            Logger.log(f"Executing module: {step}")
            context = module.run(context)
            self.event_bus.emit("module_executed", step)

        Logger.log(f"Finished pipeline: {pipeline_name}")
        return context
