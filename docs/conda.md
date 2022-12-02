# Conda

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
