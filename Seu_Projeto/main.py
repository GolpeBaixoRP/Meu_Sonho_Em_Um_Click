from core.registry import Registry
from core.orchestrator import Orchestrator
from core.plugin_loader import PluginLoader
from infra.container import Container

from modules.drive.format_module import FormatModule
from modules.drive.installer_module import InstallerModule
from modules.ps1.ps1_module import PS1Module
from modules.ps2.ps2_module import PS2Module


def bootstrap():
    container = Container()
    registry = Registry()

    # Core Modules
    registry.register_module("FormatModule", FormatModule(container))
    registry.register_module("InstallerModule", InstallerModule(container))
    registry.register_module("PS1Module", PS1Module(container))
    registry.register_module("PS2Module", PS2Module(container))

    # Default Pipelines
    registry.register_pipeline("FormatModule", ["FormatModule"])
    registry.register_pipeline("InstallerModule", ["InstallerModule"])
    registry.register_pipeline("PS1Module", ["PS1Module"])
    registry.register_pipeline("PS2Module", ["PS2Module"])

    # Plugin Auto-Load
    PluginLoader.load_plugins(registry, container)

    orchestrator = Orchestrator(registry)
    return orchestrator


def main():
    bootstrap()
    print("Sistema 100% funcional com plugins.")


if __name__ == "__main__":
    main()