# Subprocess

Run a command in the shell and get the output.

```python
def run_command(cmd):
    "Run a command in the shell and return the output"
    return subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        check=False, 
        encoding='utf-8',
    )

a = run_command("ls .")
```
