# Install Fonts for Matplotlib

## Install Font (Linux)

Download and unzip additional fonts in the `~/.fonts` directory.

```bash
mkdir ~/.fonts
```

I like to use Fira Code for monospace font and Mona/Hubos Sans for all other text.

```bash
cd ~/.fonts
mkdir FiraCode
cd FiraCode
wget https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip
unzip Fira_Code_v6.2.zip

cd ~/.fonts
mkdir MonaSans
cd MonaSans
wget https://github.com/github/mona-sans/releases/download/v1.0/Mona.Sans.1.0.zip
unzip Mona.Sans.1.0.zip

cd ~/.fonts
mkdir HubotSans
cd HubotSans
wget https://github.com/github/hubot-sans/releases/download/v1.0/Hubot.Sans.1.0.zip
unzip Hubot.Sans.1.0.zip
```

Once you have the fonts downloaded, then update the font cache.

```bash
fc-cache
```

> More details at [linuxconfic.org](https://linuxconfig.org/how-to-install-and-manage-fonts-on-linux)

Now delete the Matplotlib Font cache file

```bash
rm ~/.cache/matplotlib/fontlist*
```

# Update rcParams

```python
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = "Hubot-Sans"
mpl.rcParams["font.monospace"] = "Fira Code"

```
