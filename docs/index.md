<div align=center>

<h1> 🧰 Brian's Carpenter Workshop</h1>


<a href="https://zenodo.org/badge/latestdoi/337500272"><img src="https://zenodo.org/badge/337500272.svg"></a>

    
</div>

I have a lot of useful python tools. Instead of letting them be strewn across the garage, I want to organize them into this "workshop" and make them more useful. I enjoy woodworking and think there are a lot of analogies between carpentry and programing.

This is as an optional dependency to [`Herbie`](https://github.com/blaylockbk/Herbie), [`goes2go`](https://github.com/blaylockbk/goes2go), and [`SynopticPy`](https://github.com/blaylockbk/SynopticPy) and anything else I create.

# Install

Installation is easy with pip.

```
pip install git+https://github.com/blaylockbk/Carpenter_Workshop.git
```

Or, clone the repo and install as an "editable" package (so you can pull changes).

```
git clone https://github.com/blaylockbk/Carpenter_Workshop.git
cd Carpenter_Workshop
pip install -e .
```

# How to Cite and Acknowledge
If you borrow my tools, please cite this software and/or include me in your acknowledgments.

*Suggested Citation*

```
Blaylock, B. K. (2022). Carpenter Workshop (Version 2022.11.0) [Computer software]. https://github.com/blaylockbk/Carpenter_Workshop
```

*Suggested Acknowledgment*
```
A portion of this work used code generously provided by Brian Blaylock's Carpenter Workshop python package (https://github.com/blaylockbk/Carpenter_Workshop)
```


# My Python Philosophy

- Code should be clearly commented. Nay, code should be clearly _narrated_! 
    - Yes, I know this goes against the idea of "don't comment too much," but I feel it's better to error on the side of commenting too much rather than commenting too little.
    - Comments don't necessarily have to say what a line or block does, but it should say _why_ you are doing it that way.
    - Keep comments up to date!
- Stay up-to-date on the most recent stable software. When a new version comes out, use it and read the release notes. New features are added because someone needed those features, and they might be useful in your own work (or, at least useful to know about).
    - Do not assume sticking with a certain version number will prevent breaking changes. [It wont](https://hynek.me/articles/semver-will-not-save-you/). If you want to future-proof your code, it's best to update to newest versions rapidly, find and fix the breaking changes quickly, and enjoy modern software. If you don't update rapidly, you only postpone problems that will pile up and become unbearable. 
- Learn how to use a debugger (like in vscode).
- "If the milk is sour, throw it out!" If the script or block of code you are writing is giving you trouble and just isn't working, toss it and start over. You'll have better luck starting with a clean slate and fresh mind. 
- "If It Ain't Broke, You're Not Trying" – Uncle Red (The Red Green Show). To me, this means that it's ok to have broken code. Don't be too dissapointed in yourself. There is nothing a little duct tape can't repair. It can be fixed, and that is the joy of coding.
- A workman can't have too many tools. Everything has its place. Know how to use your tools. Keep them organized.
    - Use a code formatter; it helps you write cleaner code. (I'm using Black to format my python code.)
- Old band-aids are gross. Don't keep them in your code; fix the issues and then THROW THEM AWAY!
