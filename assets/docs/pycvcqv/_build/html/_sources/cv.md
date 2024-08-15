# Coefficient of Variation

Coefficient of variation _($CV$)_ is a measure of relative dispersion representing the degree of variability relative to the mean {cite:p}`Kelley2007`. Since cv is unitless, it is useful for comparison of variables with different units {cite:p}`Albatineh2014`. It is also a measure of homogeneity. The _population_ coefficient of variation is:

$$CV = \frac{\sigma}{\mu},$$

where $\sigma$ is the population standard deviation and $\mu$ is the population mean. Almost always, we analyze data from samples but want to generalize it as the population's parameter {cite:p}`Albatineh2014`.

Its sample's estimate is given as:

$$cv = \frac{sd}{\bar{X}}$$

where $sd$ is the sample standard deviation, the square root of the unbiased estimator of population variance, and $\bar{X}$ is the sample mean.

The corrected _cv_ to account for the sample size is:

$$
cv_{corr} = cv * \biggl(1 - \frac{1}{4(n-1)}
+ \frac{1}{n}cv^2
+ \frac{1}{2 (n-1)^2} \biggr)
$$

## What is MyST?

MyST stands for "Markedly Structured Text". It
is a slight variation on a flavor of markdown called "CommonMark" markdown,
with small syntax extensions to allow you to write **roles** and **directives**
in the Sphinx ecosystem.

For more about MyST, see [the MyST Markdown Overview](https://jupyterbook.org/content/myst.html).

## Sample Roles and Directives

Roles and directives are two of the most powerful tools in Jupyter Book. They
are like functions, but written in a markup language. They both
serve a similar purpose, but **roles are written in one line**, whereas
**directives span many lines**. They both accept different kinds of inputs,
and what they do with those inputs depends on the specific role or directive
that is being called.

Here is a "note" directive:

```{note}
Here is a note
```

It will be rendered in a special box when you build your book.

Here is an inline directive to refer to a document: {doc}`cqv`.

## Citations

You can also cite references that are stored in a `bibtex` file. For example,
the following syntax: .

Moreover, you can insert a bibliography into your page with this syntax:
The `{bibliography}` directive must be used for all the `{cite}` roles to
render properly.
For example, if the references for your book are stored in `references.bib`,
then the bibliography is inserted with:

```{bibliography}
:style: unsrt
```

## Learn more

This is just a simple starter to get you started.
You can learn a lot more at [jupyterbook.org](https://jupyterbook.org).
