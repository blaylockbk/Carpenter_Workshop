## Brian Blaylock
## November 26, 2021

"""
=============
Simple Colors
=============

20 simple, distinct colors from Sasha Trubetskoy

https://sashamaps.net/docs/resources/20-colors/

If you want to use these colors as your matplotlib color cycle just do

    import paint
    paint.SimpleColors()

"""

from cycler import cycler
import matplotlib as mpl

# 95% accessible colors
simple_colors_9500 = {
    "red": "#e6194B",
    "green": "#3cb44b",
    "yellow": "#ffe119",
    "blue": "#4363d8",
    "orange": "#f58231",
    "purple": "#911eb4",
    "cyan": "#42d4f4",
    "magenta": "#f032e6",
    "lime": "#bfef45",
    "pink": "#fabed4",
    "teal": "#469990",
    "lavender": "#dcbeff",
    "brown": "#9A6324",
    "beige": "#fffac8",
    "maroon": "#800000",
    "mint": "#aaffc3",
    "olive": "#808000",
    "apricot": "#ffd8b1",
    "navy": "#000075",
    "grey": "#a9a9a9",
    "white": "#ffffff",
    "black": "#000000",
}

# 99% accessible colors
simple_colors_9900 = {
    "red": "#e6194B",
    "green": "#3cb44b",
    "yellow": "#ffe119",
    "blue": "#4363d8",
    "orange": "#f58231",
    "cyan": "#42d4f4",
    "magenta": "#f032e6",
    "pink": "#fabed4",
    "teal": "#469990",
    "lavender": "#dcbeff",
    "brown": "#9A6324",
    "beige": "#fffac8",
    "maroon": "#800000",
    "mint": "#aaffc3",
    "navy": "#000075",
    "grey": "#a9a9a9",
    "white": "#ffffff",
    "black": "#000000",
}

# 99.99% accessible colors
simple_colors_9999 = {
    "yellow": "#ffe119",
    "blue": "#4363d8",
    "orange": "#f58231",
    "lavender": "#dcbeff",
    "maroon": "#800000",
    "navy": "#000075",
    "grey": "#a9a9a9",
    "white": "#ffffff",
    "black": "#000000",
}

# 100% accessible colors
simple_colors_10000 = {
    "yellow": "#ffe119",
    "blue": "#4363d8",
    "grey": "#a9a9a9",
    "white": "#ffffff",
    "black": "#000000",
}


class SimpleColors:
    """
    Class for 20 simple, distinct colors (plus white and black).

    Based on https://sashamaps.net/docs/resources/20-colors/

    Examples
    --------
    To cycle through these colors with Matplotlib, do
    >>> import paint
    >>> paint.SimpleColors()
    """

    def __init__(self, accessibility=0.95, *, exclude=None, include=None):
        """
        Parameters
        ----------
        accessibility : {0.95, .99, .9999, 1}
            Get colors that are at a level of accessibility.
            Default is 95% accessible (22 colors).
        exclude : None, list, or str
            Names of colors to exclude from the list.
            List: ['blue', 'white']
            String: 'blue', or 'blue,white'
        include : dict
            Dictionary of additional colors to include (or overwrite).
        """
        self.accessibility = accessibility

        if accessibility == 1:
            self.colors = simple_colors_10000.copy()
        elif accessibility >= 0.9999:
            self.colors = simple_colors_9999.copy()
        elif accessibility >= 0.99:
            self.colors = simple_colors_9900.copy()
        else:
            self.colors = simple_colors_9500.copy()

        if exclude is not None:
            if isinstance(exclude, str):
                exclude = exclude.split(",")
            for i in exclude:
                _ = self.colors.pop(i.strip())

        if include is not None:
            self.colors |= include

        self.color_list = [i for _, i in self.colors.items()]

        # Set the Matplotlib rcParameters
        self.set_rcParams

    @property
    def cycler(self):
        """Create a cycler object with the color list"""
        return cycler(color=self.color_list)

    @property
    def set_rcParams(self):
        """Set the Matplotlib rcParams to cycle through the colors"""
        mpl.rcParams["axes.prop_cycle"] = self.cycler
