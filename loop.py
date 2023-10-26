import subprocess
import asyncio
import sys
import time

arg_1  = sys.argv[1]
arg_2  = sys.argv[2]
arg_3  = sys.argv[3]
print(arg_1)
print(arg_2)
print(arg_3)



path  = "C:\\GIT\\scrapy\\"+arg_3+"\\"+arg_3+"\\spiders"
process = subprocess.Popen(['scrapy', 'crawl', arg_1, '-a', 'u=' + str(arg_2)], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Capture the output and error messages
stdout, stderr = process.communicate()

# Decode the output to a string if it's not None
if stdout is not None:
    output = stdout.decode('utf-8')
else:
    output = "No output captured."

# Decode the errors to a string if it's not None
if stderr is not None:
    errors = stderr.decode('utf-8')
else:
    errors = "No error messages captured."

# Print the output and error messages
print("Output:")
print(output)
print("Errors:")
print(errors)




