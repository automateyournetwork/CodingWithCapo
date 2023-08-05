import os
from genie.testbed import load

def main(runtime):
    if not runtime.testbed:
        # If no testbed is provided 
        testbedfile = os.path.join('interface_intent.yaml')
        testbed = load(testbedfile)
    else:
        testbed = runtime.testbed
    
    testscript = os.path.join(os.path.dirname(__file__), 'interface_tests.py')

    runtime.tasks.run(testscript=testscript, testbed=testbed)