**Brian Blaylock**  
**December 10, 2019**

# LaTeX formating for Markdown ➕➗➖✖ 🔢

If writing markdown in VSCode, install the **[Markdown+Math](https://marketplace.visualstudio.com/items?itemName=goessner.mdmath)** extension and take a look at the short documentation. In Jupyter Lab, the LaTeX ability is already included and mostly follows the same formatting (except for equation numbering).

**In-line expressions** are surrounded by single dollar signs and look like this: $y = mx+b$. Notice there is no white space before/after the `$`:

    $in line equation$

**Equation blocks** are surrounded by a double dollar sign and are in a separate line:
    
    $$block equation$$   

$$y = mx+b$$

You may also give it an equation number by specifying a number like this (doesn't seem to work in Jupyter Lab):

    $$block equation$$ (1)

$$ 7 = x+5$$ (1)


## LaTeX Notation

|Feature|Notation|Rendering|
|-------|--------|---------|
|Times Sign| `y=m \times x+b`| $y=m \times x+b$
|Subscript| `x_{inside}`| $x_{sub}$
|Superscript| `x^{inside}`| $x^{sup}$
|Fraction| `\frac{top}{bottom}`| $\pi = \frac{c}{d}$
|Integral| `\int_{bottom limit}^{top limit}{equation}`| $y=\int_{0}^{1}{x}dx$
|Parentheses| `\left( \frac{x}{y}\right)`| $\left( \frac{x}{y}\right)$
|**All Together**| `F = G \left(\frac{m_1 m_2}{r^2}\right)` | $F = G \left(\frac{m_1 m_2}{r^2}\right)$

> Look at this[list of LaTeX symbols](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols) for more symbols and this [cheatsheet](https://www.authorea.com/users/77723/articles/110898-how-to-write-mathematical-equations-expressions-and-symbols-with-latex-a-cheatsheet) for additional examples.


## Common Equations:

### Data Assimilation

Observation Impact

$$OBIMP = innovation \times sensitivity$$ (1)

Innovation

$$innovation = T_{observation} - T_{background}$$ (2)


### Common Math

|||
|--|--|
|Slope of a line| $y = mx + b$
|Hypotenuse| $c^2 = a^2 + b^2$
|Integral|$y = \int_{0}^{1}{x}^{2}dx$



### [Feature Scaling](https://en.wikipedia.org/wiki/Feature_scaling) (normalization)
Scale a set of number between 0 and 1:

$$ x^{\prime} = \frac{x - x_{min}}{x_{max} - x_{min}} $$ (1)
<br>

Scale a set of number between two numbers, [a, b]:

$$ x^{\prime} = a + \frac{(x-x_{min})(b-a)}{x_{max}-x_{min}}$$ (2)

<br>

Mean Normalization:

$$ x^{\prime} = \frac{x - x_{average}}{x_{max} - x_{min}} $$ (3)

<br>