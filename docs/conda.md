# Conda

Update conda software

```bash
conda update -n base -c defaults conda
```

Update environment from yaml file

```bash
conda env update -f myenv.yml
conda env update -f myenv.yml --prune  # removes dependencies not needed
```

Search for package versions

```bash
conda search packageName
```

Search for package and list dependency info

```bash
conda search packageName=<version> --info
```

Clean unneeded files

```bash
conda clean -tp
```

Run conda inside a bash script

```bash
eval "$(conda shell.bash hook)"
```

Channel Priority: put this in your `~/.condarc` file
```yaml
channels:
  - conda-forge
  - defaults
```

## Using Conda in a script

In a Windows .bat script, use

```
CALL conda.bat activate <env-name>
```

In a bash script, use
```
eval "$(conda shell.bash hook)"
conda activate <env-name>
```

## Conda Mamba Solver: Faster Environment Solver

Use the [mamba](https://conda.github.io/conda-libmamba-solver/getting-started/) solver in Conda (must be using Conda version>=22.11.0)

    conda install -n base conda-libmamba-solver -c conda-forge

Then set this solver as the default

    conda config --set solver libmamba

Read more about this solver [here](https://conda.github.io/conda-libmamba-solver/).

> If you have issues, see https://github.com/conda/conda-libmamba-solver/issues/244#issuecomment-1699956540


