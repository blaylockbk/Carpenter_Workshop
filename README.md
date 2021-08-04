# 🧰 Brian's Carpenter Workshop

I have a lot of useful python tools. Instead of letting them be strewn across the garage, I want to organize them into this "workshop" and make them more useful. I enjoy woodworking and think there are a lot of analogies between carpentry and programing.

**My Python Philosophy**  
- Code should clearly commented. Nay, code should be clearly _narrated_! 
    - Yes, I know this goes against the idea of "don't comment too much," but I feel it's better to error on the side of commenting too much rather than commenting too little.
    - Comments don't necessarily have to say what a line or block does, but it should say _why_ you are doing it that way.
- Stay up-to-date on the most recent stable software. When a new version comes out, use it and read the release notes. New features are added because someone needed those features, and they might be useful in your own work (or, at least useful to know about)
- Learn how to use a debugger (like in vscode).
- "If the wine is sour, throw it out!" Well, I'd never know if wine was sour because I don't drink wine. But this saying means if the script you are writing is giving you trouble and just isn't working, toss it and start over. You'll have better luck starting with a clean slate and fresh mind. 
- "If It Ain't Broke, You're Not Trying" – Uncle Red (The Red Green Show). To me, this means that it's ok to have broken code. Don't be too dissapointed in yourself. There is nothing a little duct tape can't repair. It can be fixed, and that is the joy of coding.
- A workman can't have too many tools. Everything has its place.

<br><br>

---

> **Other packages or tools I want to remember that might come in use later**
> - [Thermofeel](https://github.com/ecmwf-projects/thermofeel) calculate human thermal comfort indexes
> -

<br><br><br>
---

# Quick Reference
I am tired of re-searching for these snippets on the internet. If I put them here, maybe I'll remember they are here.

## Conda
Update from yaml file

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

### Matplotlib: Jupyter Figure Transparency
Use Jupyter Magic to give transparency to the figure displayed in the notebook
```python
%config InlineBackend.print_figure_kwargs = {'facecolor':'none'}
%config InlineBackend.print_figure_kwargs = {'facecolor' : 'w'}
```

### Matplotlib: style parameters
```python
# Use my custom style sheet (if in )
plt.style.use('BB_style')

# Change default date formatter
plt.rcParams['date.autoformatter.day'] = '%b %d\n%H:%M'
plt.rcParams['date.autoformatter.hour'] = '%b %d\n%H:%M'

# Put grid lines behind patches (i.e., bar plots)
plt.rcParams["axes.axisbelow"] = True  

# Needed this to modify fonts in Adobe Illustrator
plt.rcParams['svg.fonttype'] = 'none'
```

### Matplotlib: Discrete Colormap and Norm
```python
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

cmap = plt.get_cmap('bwr', 10)
norm = mcolors.Normalize(vmin=5, vmax=10)
plt.pcolormesh(np.random.rand(10,10)*8+5, cmap=cmap, norm=norm)
plt.colorbar()

# or, make colormap index based on discrete intervals

cmap = plt.get_cmap('bwr', 10)
norm = mcolors.BoundaryNorm([1,2,5,8,10], 10)
plt.pcolormesh(np.random.rand(10,10)*8+2, cmap=cmap, norm=norm)
plt.colorbar(spacing='proportional')
```

### Matplotlib: Dates
```python
import matplotlib.dates as mdates
formatter = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(formatter)
```
```python
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.HourLocator(range(0, 24, 3)))
ax.xaxis.set_minor_locator(mdates.HourLocator(range(0, 24, 1)))
```


### Matplotlib: Latex Strings
The syntax depends on the character you use. Some require an escape character or use the raw string format.
```python
# Greek Letters
plt.title('$\\theta$') # Use the \\ to escape single \, because \t means tab
plt.title(r'$\theta$') # or, use raw string r''
plt.title('$\\alpha$')
plt.title('$\Delta$')  # Does not require \\ or r''

# Superscript (e.g. wind speed m/s, FSOI J/kg, PM2.5 ug/m3)
plt.ylabel('Wind Speed (m s${^{-1}}$)')
plt.xlabel('FSOI (J kg$^{-1}$)')
plt.ylabel('PM 2.5 Concentration ($\mu$g m${^{-3}}$)')

# Subscript (e.g., CO_2, theta_surface)
plt.ylabel('CO$_2$ (ppm)')
plt.ylabel('$\\theta$${_{surface}}$')  #
plt.ylabel('$\\theta\mathregular{_{surface}}$')  # use \mathregular for non-italics

# Temperature Degree
plt.ylabel('Temperature ($\degree$C)')

```

### Exceptions Warning
```python
try:
    (do something)
except Exception as e:
    print(f"WARNING: {e}")
```
