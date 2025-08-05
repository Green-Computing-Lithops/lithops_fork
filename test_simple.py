import lithops
import logging
import os

# Enable debug logging
# logging.basicConfig(level=logging.DEBUG)
# os.environ['LITHOPS_DEBUG'] = '1'


def simple_function(x): 
    # Simple function without storage access
    return x + 1

# Create executor without debug logging to avoid the storage metadata issue
executor = lithops.FunctionExecutor()

# Execute the function
ft = executor.map(simple_function, [1, 2, 3])

# Get results
print("Results:", executor.get_result(ft))
