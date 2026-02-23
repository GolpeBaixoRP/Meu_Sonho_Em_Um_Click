def register(registry, container):

    class ExamplePluginModule:
        def __init__(self, container):
            self.container = container

        def run(self, context):
            context["plugin"] = "executed"
            return context

    registry.register_module("ExamplePlugin", ExamplePluginModule(container))
    registry.register_pipeline("ExamplePlugin", ["ExamplePlugin"])
