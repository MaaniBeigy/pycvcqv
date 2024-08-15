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

There are various methods for the calculation of **confidence intervals (CI)** for _cv_. All of them are fruitful and have particular use cases. Some of them are model-based hence their usage depends the assumptions regarding the distribution of data. For sake of versatility, we cover almost all of these methods in `cvcqv` package. Here, we explain them along with some examples:

## Kelley Confidence Interval

Let us assume that _CV_ follows a noncentral _t_ distribution, when the parent population of the scores is _normally-distributed_, with noncentrality ($\lambda$) parameter:

$$
\lambda = \frac{\sqrt{n}}{cv}
$$

with _v_ degrees of freedom, where $v = n - 1$.

Let $1 - \alpha$ be the CI coverage with $\alpha_L + \alpha_U = \alpha$ in which $\alpha_L$ is the the proportion of times that _cv_ will be
less than the lower confidence bound and $\alpha_U$ the proportion of times that _cv_ will be greater than the upper confidence bound in the CI procedure {cite:p}`Kelley2007`. The lower confidence tile for $\lambda$ is is the noncentrality parameter that results in $t_{(1-\alpha_L,v,\lambda_L)}=\hat{\lambda}$ and the upper confidence tile for $\lambda$ is is the noncentrality parameter that results in $t_{(\alpha_U,v,\lambda_U)}=\hat{\lambda}$, where $t_{(1-\alpha_L,v,\lambda_L)}=\hat{\lambda}$ is the value of noncentral _t_ distribution at the $1-\alpha_L$ **quantile** with noncentrality parameter $\lambda_L$ and $t_{(\alpha_U,v,\lambda_U)}=\hat{\lambda}$ is the value of noncentral _t_ distribution at the $\alpha_U$ **quantile** with noncentrality parameter $\lambda_U$, respectively {cite:p}`Kelley2007`. Afterwards, we transform the tiles of the confidence interval for $\lambda$, by dividing the tiles by $\sqrt{n}$ and thereafter inverting them; the CI limits of
$cv$ will be obtained:

$$
p\left[\biggl(\frac{\lambda_U}{\sqrt{n}}\biggr)^{-1}
\le CV \le \biggl(\frac{\lambda_L}{\sqrt{n}}\biggr)^{-1}\right] = 1-\alpha
$$

where $p$ stands for _probability_.

```{bibliography}
:style: unsrt
```
