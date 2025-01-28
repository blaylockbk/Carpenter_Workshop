# IPython / Jupyter

## Cell Timers

In your jupyter notebook, you can print the time it takes to execute a cell
```
%%time
```

You can also time the exceution many times and print the average time. This is great for measuring code performance as your developing code
```
%%timeit
```

## Embed IPython in a function

You can embed an IPython in your function or script

```python
from IPython import embed; embed()
```

```python
def this_function():
    print("welcome to this function. I have an IPython interpreter for you...")
    a = 5
    b = 10
    c = a + b
    from IPython import embed; embed()
```

This can be useful for debugging your function. When you run a Python script, if your function has the embeded IPython, then it will let you explor the values in that function.

## Auto reload imports

Put this at the top of your notebook to automatically reload imports
```
%load_ext autoreload
%autoreload 2
```
