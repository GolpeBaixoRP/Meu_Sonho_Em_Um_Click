import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from main import bootstrap

def run_tests():
    orchestrator = bootstrap()
    result = orchestrator.execute("ExamplePlugin", {})
    assert result.get("plugin") == "executed"
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()
