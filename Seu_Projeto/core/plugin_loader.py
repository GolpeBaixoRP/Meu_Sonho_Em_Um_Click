import importlib
import pkgutil

class PluginLoader:

    @staticmethod
    def load_plugins(registry, container):
        import plugins
        for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
            module = importlib.import_module(f"plugins.{module_name}")
            if hasattr(module, "register"):
                module.register(registry, container)
