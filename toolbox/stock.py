## Brian Blaylock
## July 17, 2020

"""
===================
Miscellaneous Stock
===================

"Take stock in these, they might be worth something someday."

Named "stock" for the cattle stock a rancher might have roaming
around that can be worth something when rounded up.

"""
from datetime import datetime
import inspect
from pathlib import Path
import operator
import os
import shutil
import contextlib
import sys
import warnings

import multiprocessing
from multiprocessing import Pool, cpu_count          # Multiprocessing
from multiprocessing.dummy import Pool as ThreadPool # Multithreading

import numpy as np
import matplotlib.pyplot as plt

try:
    from dask import delayed, compute
except Exception as e:
    print(f"WARNING! {e}")
    print('Without dask, you cannot use dask for multiprocessing.')


# ==============
# Python Version
# ==============
python_version = float(f"{sys.version_info.major}.{sys.version_info.minor}")

# ======================================================================
# Append copy method to Path module
# ======================================================================
def _copy(self, target, verbose=True):
    """
    Add this copy method to a Path object.
    
    For Path objects created by ``toolbox.stock.full_path``, there will
    be this copy method added for easy copying the file to other Paths.
    
    .. note:: 
        Based answer on `StackOverflow <https://stackoverflow.com/a/40319071/2383070/>`_
    
    Parameters
    ----------
    self : pathlib.Path
        A Path object file to be copied.
    target : {str, pathlib.Path}
        The destination Path to copy the file to.
        If target is a directory, will preserve the file name.
        If target is a file, will rename the file.
        
    Example
    -------
    Add this copy method to the Path module.
    
    >>> from pathlib import Path
    >>> Path.copy = _copy
    
    then use the copy method on any Path object.
    >>> Path('this_file.txt').copy(Path('this_dir/renamed.txt'))
    >>> Path('this_file.txt').copy(Path('this_dir'))
    """
    assert self.is_file()
    assert python_version >= 3.7, "🐍 Python 3.7+ is required for shutil to accept Path object."
    
    shutil.copy(self, target)
        
    if verbose: print(f"📄➡📁 Copied [{self}] to [{target}]")

Path.copy = _copy

# ======================================================================
# File paths
# ======================================================================
def full_path(p, must_exist=True, mkdir=False, verbose=True):
    """
    Convert string to ``pathlib.Path``. Resolve path and environment variables.
    
    ``pathlib.Path`` does not resolve environment variables in a path string.
    This function replaces environment variables like '$HOME' with the value
    of ``os.environ['HOME']`` and returns a pathlib.Path.
        
    Parameters
    ----------
    p : {str, pathlib.Path}
        The file path that may include '~', '..', or environment 
        variables, (i.e., $HOME, $PWD, $WORKDIR, $HOME).
    must_exist : bool
        True, the resolved Path must exist, or else an assert error is raised.
        False, the resolved Path does not have to exist.
    mkdir : bool
        True, make the directory if it does not exist.
        False, do not make the directory.
        
    Returns
    -------
    The fully resolved pathlib.Path.
    
    Examples
    --------
    >>> full_path('$HOME/figs')
    PosixPath('/p/home/blaylock/figs')
        
    >>> full_path("~/pyBKB_NRL")
    PosixPath('/p/home/blaylock/pyBKB_NRL')

    """
    if isinstance(p, str):
        p = Path(p)
    
    # Replace environment variables values (platform dependent)
        
    # PosixPath (linux and mac):  Environment variables look like $HOME
    if '$' in str(p):
        split_path = str(p).split(os.sep)
        environ = [os.environ[i[1:]] if '$' in i else i for i in split_path]
        p = Path('/'.join(environ))
        
    # Resolve path for `~`, `~blaylock`, `..`, `//`, and `.` 
    p = p.expanduser().resolve()
    
    # Make Directory if it doesn't exist
    if not p.exists() and mkdir:
        if p.suffix == '':
            p.mkdir(parents=True)
        else:
            p.parent.mkdir(parents=True)  # because p is a file.
        if verbose: print(f'👷🏼‍♂️ Created directory: {p}')
    
    if must_exist:
        assert p.exists(), f"🦇 Does Not Exist: {p}."
    
    return p

def ls(p, pattern='*', which='files', recursive=False, hidden=False):
    """
    List contents of a directory path; files, directories, or both.
    
    Parameters
    ----------
    p : pathlib.Path
        The directories path you want to search in for files.
    pattern : str
        A glob pattern to search for files. Default is ``\*`` to search for 
        all files, but other examples are ``\*.txt`` for all text files.
    which : {'files', 'dirs', 'both'}
        Specify which type of Path object to list.
    recursive : bool
        True, will search for files recursively in subdirectories.
        False, will search only the provided Path (default).
    hidden : bool
        True, show hidden files or directories (name starts with '.').
        False, do not show hidden files or directories (default).
    """
    
    p = full_path(p)
        
    if recursive:
        glob_obj = p.rglob(pattern)
    else:
        glob_obj = p.glob(pattern)
        
    if which == 'files':
        f = filter(lambda x: x.is_file(), glob_obj)
    elif which == 'dirs':
        f = filter(lambda x: x.is_dir(), glob_obj)
    else:
        f = glob_obj
    
    if hidden:
        f = filter(lambda x: x.name.startswith('.'), f)
    else:
        f = filter(lambda x: not x.name.startswith('.'), f)
    
    f = list(f)
    f.sort()
    
    if len(f) == 0:
        warnings.warn(f'🤔 None from {p}')
    
    return f

def cp(src, dst='$TMPDIR', name=None, verbose=True):
    """
    Copy a file to another directory.
            
    Parameters
    ----------
    src : {str, pathlib.Path}
        The source file to be copied.
    dst : {str, pathlib.path}
        A directory path to copy the file. 
        Default is a temporary directory at $WORKDIR/tmp
    name : {None, str}
        If None (default), the src filename is preserved, otherwise change
        the name to something else.
    """
    src = full_path(src)
    dst = full_path(dst)
    
    assert src.is_file()
    assert dst.is_dir()
    
    if name is None:
        dst = dst / src.name
    else:
        dst = dst / name

    if not dst.parent.exists():
        dst.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(src, dst)
    
    if verbose: print(f"📄➡📁 Copied [{src}] to [{dst}]")
    
    return dst

def create_path(p, verbose=True):
    """
    Create a path if it does not exist.
    
    Parameters
    ----------
    p : string or pathlib.Path
        Path of directory that will be created if it does not exist.
    """
    p = full_path(p, must_exist=False)
    
    try:
        p.mkdir(parents=True)
        if verbose: print(f'📂 Created directory: {p}')
    except:
        if verbose: print(f'🍄 Directory already exists: {p}')
            
    return p
            

# ======================================================================
# Multiprocessing and Multithreading 🤹🏻‍♂️ 🧵 📏 🐲
# ======================================================================
# Resources:
# - https://chriskiehl.com/article/parallelism-in-one-line
# - https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python

def _multipro_helper_MP(job_arg):
    i, n, func, args, kwargs = job_arg
    if not hasattr(args, '__len__'):
        args = [args]
    process = multiprocessing.current_process().name
    thread = multiprocessing.dummy.current_process().name
    output = func(*args, **kwargs)
    print(f"\r    ⏳ {process}/{thread} completed task [{i:,}/{n:,}] {' '*15}", end='')
    return output

def multipro_helper(func, args, kwargs={}, *,
                    cpus=None, threads=None, dask=None,
                    max_threads=20, max_dask_workers=32, 
                    verbose=True):
    """
    Multiprocessing and multithreading helper.

    By default, cpus and threads are set to None and each task will 
    be done sequentially via list comprehension. To use multiprocessing
    or multithreading, specify a number for ``cpus`` or ``threads``.
    Use multiprocessing for CPU-bound tasks. Use multithreading for 
    IO-bound tasks.
    
    Parameters
    ----------
    func : function
        A function you want to apply to each item in the list ``inputs``.
        If your function has many inputs, it is useful to call a helper 
        function that unpacks the arguments for each input.
    args : list
        A list of input for the function being called.
        These are *different* for each process. If multiple arguments
        are needed, then each item in the list should be a tuple.
    kwargs : dict
        Keyword arguments for the function. 
        These are the *same* for each process.
    
    cpus : int or None
        Number of CPUs to use to complete the task with multiprocessing.
        Will not exceed maximum number available and will not exceed 
        the length of ``inputs``.
        If None, will try to use multithreading instead.
    threads : int or None
        Number of threads to use. Will not exceed ``max_threads`` kwarg
        (default 20) and will not exceed the length of ``inputs``.
        If None, will try to do each task sequentially as a list 
        comprehension.
    dask : {None, 'processes', 'threads', 'single-threaded'}
        If you want to use Dask to parallelize the code, set
        from None to a dask schedular. 
        - 'sync' or 'synchronous' is the same as 'single-threaded'
        See docs for more info
        https://docs.dask.org/en/latest/setup/single-machine.html
    max_threads : int
        The maximum number of threads to use. Default 20.
    max_dask_workers : int
        If dask gives you a KeyboardInterupt, try lowering the 
        num_workers for dask.compute (i.e., ``max_dask_workers=32``).
        This seems to just be a problem when the 'processes' scheduler
        is used, not the 'threads' or 'single-threaded' scheduler.
    """
    
    assert callable(func), f"👻 {func} must be a callable function."
    assert hasattr(args, "__len__"), f"👻 args must have length."
    assert isinstance(kwargs, dict), f"👻 kwargs must be a dict."
    
    timer = datetime.now()
    
    n = len(args)
    inputs = [(i, n, func, arg, kwargs) for i, arg in enumerate(args, start=1)]
    
    # If only one task, we don't need multiprocessing
    if n == 1:
        cpus = None
        threads = None
        dask = None

    info = {}
    info['n'] = len(inputs)

    # Multiprocessing
    if cpus is not None:
        assert isinstance(cpus, (int, np.integer)), f"👻 cpus must be an int. You gave {type(cpus)}"
        cpus = np.minimum(cpus, cpu_count())
        cpus = np.minimum(cpus, len(inputs))
        print(f'🤹🏻‍♂️ Multiprocessing [{func.__module__}.{func.__name__}] with [{cpus:,}] CPUs for [{n:,}] items.')
        with Pool(cpus) as p:
            results = p.map(_multipro_helper_MP, inputs)
            p.close()
            p.join()
        info['TYPE'] = 'multiprocessing'
        info['cpus'] = cpus
        info['timer'] = datetime.now()-timer

    # Multithreading
    elif threads is not None:
        assert isinstance(threads, (int, np.integer)), f"👻 threads must be an int. You gave {type(threads)}"
        threads = np.minimum(threads, max_threads)
        threads = np.minimum(threads, len(inputs))
        print(f'🧵 Multithreading [{func.__module__}.{func.__name__}] with [{threads:,}] threads for [{n:,}] items.')
        with ThreadPool(threads) as p:
            results = p.map(_multipro_helper_MP, inputs)
            p.close()
            p.join()
        info['TYPE'] = 'multithreading'
        info['threads'] = threads
        info['timer'] = datetime.now()-timer

    # Dask delayed
    elif dask is not None:
        jobs = [delayed(_multipro_helper_MP)(i) for i in inputs]
        if dask == 'processes':
            workers = np.minimum(max_dask_workers, len(jobs))
        else:
            workers = None
        print(f"🐲 Dask delayed [{func.__module__}.{func.__name__}] with [num_workers={workers}, scheduler='{dask}'] for [{n:,}] items.")
        results = compute(jobs, num_workers=workers, scheduler=dask)[0]
        info['TYPE'] = 'Dask.delayed'
        info['dask scheduler'] = dask
        info['dask workers'] = workers
        info['timer'] = datetime.now()-timer
        # I'm not super convinced I'm doing this Dask stuff right.
        # https://docs.dask.org/en/latest/delayed-best-practices.html
        # https://docs.dask.org/en/latest/delayed.html
        # https://docs.dask.org/en/latest/setup/single-machine.html

    # Sequential jobs via list comprehension
    else:
        print(f'📏 Sequentially do [{func.__module__}.{func.__name__}] for [{n:,}] items.')
        results = [_multipro_helper_MP(i) for i in inputs]
        info['TYPE'] = 'sequential' 
        info['timer'] = datetime.now()-timer
    
    print(f"\r    Completed task [{len(results):,}/{n:,}]  Timer={datetime.now()-timer} {' '*15}")
    
    return results, info

def plot_multipro_efficiency(func, args=(), kwargs={}, 
                             pools=range(1,11),
                             plot_multipro=True, 
                             plot_multithread=True,
                             plot_sequential=True,
                             plot_dask=True, figsize=(7,5)):
    """
    Display a figure showing the multiprocessing/multithreadding 
    efficiency for a range of Pool sizes.
    
    func : function
        A function that has keyword arguments for ``cpus`` and ``threads``.
    args, kwargs : 
        Arguments and keyword arguments for the function.
    pools : list of int
        List of number of Pools to start for multiprocessing/multithreading.
    """
    plt.rcParams['hatch.linewidth'] = 8
    
    pools = [i for i in pools if i > 0]
    
    assert 'MP_kwargs' in inspect.getfullargspec(func).args, "👺 The function {func.__name__} does not have a `MP_kwargs` argument."

    plt.figure(figsize=figsize)

    if plot_multipro:
        multipro = []
        for i in pools:
            timer = datetime.now()
            _, info = func(*args, **kwargs, MP_kwargs=dict(cpus=i))
            timer = datetime.now()-timer
            multipro.append(timer)
        plt.bar(list(pools), [i.total_seconds() for i in multipro],
                label='Multiprocessing', color='.1', zorder=5)
   
    if plot_multithread:
        multithread = []
        for i in pools:
            timer = datetime.now()
            _, info = func(*args, **kwargs, MP_kwargs=dict(threads=i))
            timer = datetime.now()-timer
            multithread.append(timer)
        plt.bar(list(pools), [i.total_seconds() for i in multithread],
                label='Multithreading', hatch='/', edgecolor='tab:blue',
                alpha=.33, color='tab:blue', zorder=6)

    if plot_sequential:
        timer = datetime.now()
        _, info = func(*args, **kwargs, MP_kwargs=dict(cpus=None, threads=None, dask=None))
        timer = datetime.now()-timer
        sequential = timer
        plt.axhline(sequential.total_seconds(), color='k', lw=3,
                    label='Sequential', zorder=4)
    
    if plot_dask:
        for scheduler, color, ls in zip(['single-threaded', 'threads', 'processes'], ['tab:green', 'tab:red', 'tab:purple'], ['--', '-.', ':']):
            try:
                timer = datetime.now()
                _, info = func(*args, **kwargs, MP_kwargs=dict(cpus=None, threads=None, dask=scheduler))
                dask_timer = datetime.now()-timer
                plt.axhline(dask_timer.total_seconds(), ls=ls, color=color, label=f"Dask '{scheduler}'", zorder=6)
            except Exception as e:
                print(f"Error with Dask scheduler{scheduler}''.")
                print(f"Error is {e}")
                pass
    
    # Cosmetics
    plt.ylabel('Seconds')
    plt.xlabel('Number in Pool')
    plt.title(f"{func.__module__}.{func.__name__}", loc='left', fontweight='bold')
    plt.title(f"Number of Tasks: {info['n']}", loc='right')
    plt.xticks(list(pools))
    plt.grid(zorder=0, ls='--', alpha=.25)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    
    #return multipro, multithread, sequential


# ======================================================================
# Other
# ======================================================================
def no_print(func, *args, **kwargs):
    """When a function insists on printing, force it not to.
    
    https://stackoverflow.com/a/46129367/2383070
    
    Parameters
    ----------
    func : function
        A function you wish to call
    *args : 
        The functions arguments
    **kwargs :
        The function's key word arguments
        
    Examples
    --------
    >>> def test_print(a):
    ...    print("I insist on printing all this junk")
    ...    print("and there is nothing you can do about it.")
    ...    print("Whahahah!")
    ...    print(f'2 * {a} =')
    ...    return 2*a
    >>> no_print(test_print, 30)
    60
    
    >>> test_print(30)
    I insist on printing all this junk
    and there is nothing you can do about it.
    Whahahah!
    2 * 30 =
    60
    
    """
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        value = func(*args, **kwargs)
    return value
            
def str_operator(left, operator_str, right):
    """
    Performs an operation when you have an operator as a string.

    .. note:: An alternative method is to use the `eval()` function, 
    if you aren't worried about the security vulnerabilities.
    
    Example: `a=5; b=6; eval('a + b')` the result is 11.
    
    Parameters
    ----------
    left : 
        A value or array on the left side of the operato.
    operator_str : {'>', '>=', '==', '<', '<=', '+', '-', '*', '/', '//', '%', '**', 'is', 'is not', 'in'}
        An operator as a string.
    right :
        A value or array on the right side of the operator.
        
    Returns
    -------
    The results of the operation. This isn't heart surgery.
    
    Examples
    --------
    >>> a = 5
    >>> b = 6
    >>> c = np.array([3, 5, 7])
    
    >>> a > b
    False
    
    is the same as...
    
    >>> str_operator(a, '>', b)
    False
    
    >>> a > c
    array([ True, False, False])
    
    is the same as...
    
    >>> str_operator(a, '>', c)
    array([ True, False, False])
    """
    op_list = {'>': operator.gt,
               '>=': operator.ge,
               '==': operator.eq,
               '<': operator.lt,
               '<=': operator.le,
               '+': operator.add,
               '-': operator.sub,
               '*': operator.mul,
               '/': operator.truediv,
               '//': operator.floordiv,
               '%': operator.mod,
               '**': operator.pow,
               'is': operator.is_,
               'is not': operator.is_not,
               'in': operator.contains,
               }
    assert operator_str in list(op_list), f"`operator_str` must be one of {list(op_list)}"
    
    return op_list[operator_str](left, right)

def normalize(value, lower_limit, upper_limit, clip=True):
    """
    Normalize values between 0 and 1.
    
    Normalize between a lower and upper limit. In other words, it 
    converts your number to a value in the range between 0 and 1. 
    Follows `normalization formula 
    <https://stats.stackexchange.com/a/70807/220885>`_
    
    This is the same concept as `contrast or histogram stretching 
    <https://staff.fnwi.uva.nl/r.vandenboomgaard/IPCV20162017/LectureNotes/IP/PointOperators/ImageStretching.html>`_
    

    .. code:: python
    
        NormalizedValue = (OriginalValue-LowerLimit)/(UpperLimit-LowerLimit)
            
    Parameters
    ----------
    value :
        The original value. A single value, vector, or array.
    upper_limit :
        The upper limit. 
    lower_limit :
        The lower limit.
    clip : bool
        - True: Clips values between 0 and 1 for RGB.
        - False: Retain the numbers that extends outside 0-1 range.
    Output:
        Values normalized between the upper and lower limit.
    """
    norm = (value-lower_limit)/(upper_limit-lower_limit)
    if clip:
        norm = np.clip(norm, 0, 1)
    return norm

