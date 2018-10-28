# jswip
A Jupyter Kernel for SWI-Prolog.

Inspired by [madmax2012/SWI-Prolog-Kernel](https://github.com/madmax2012/SWI-Prolog-Kernel) and now using [PySwip](https://github.com/yuce/pyswip).

**USE WITH CARE!**

This kernel is only barely tested using jupyter lab on debian linux. If anyone tests it e. g. on plain jupyter and/or windows feel free to open a ticket to report success and/or failure.

I have only just started out learning prolog and have not tested this kernel with all language constructs of prolog yet. There might still be problems with more advanced prolog stuff.

## Usage Notes and Limitations

You should **split your knowledgebase and your queries into different cells**. KB entries (facts and so on) will be retained as long as the kernel is running. This means that if you run a cell containing facts twice the facts will be sent to swipl twice. This will typically not result in errors but in odd outputs when querying the KB.

Should you receive bogus output when running queries restart the kernel and make sure you run any cell containing something other than queries only once.

Every query must start with `?-`.

Working example:

```
man(socrates).
mortal(X) :- man(X).

?- mortal(socrates).
?- mortal(X).
?- mortal(bob).
```

Will output.

```
true.
X = socrates.
false.
```

Keep in mind that for some queries there are lots of answers. For the kernel to always succeed in a reasonable amount of time the default output limit to any one query is 10 answers. You can influence this limit by the following syntax.

```
?- someQuery(...) {LIMIT}.
```

Where `LIMIT` is replaced by the maximum number of answers that will be displayed for this query. It is not very smartly parsed (sorry), so there must be no spaces inside the curly braces or in between the closing curly brace and the period. *Not like this:* ~`{1} .`~ or this ~`{ 1 }.`~

A limit value of `-1` means no limit. Be careful with this!

## Supported environments

Only **pyhton3** is supported (anybody still using python2 should really have upgraded by now...) and it was only tested on **linux** as I have no jupyter installation on windows. In theory it should work on windows though.

## Installation

1. Install [SWI-Prolog](http://www.swi-prolog.org).
2. Install jswipl `python3 -m pip install --upgrade --user jswipl`
3. Change directory to your jupyters kernel directory. Typically `~/.local/share/jupyter/kernels`.
4. `mkdir jswipl && cd jswipl`
5. Install kernel spec: `wget https://raw.githubusercontent.com/targodan/jupyter-swi-prolog/master/kernel.json`
6. Restart jupyter
7. Profit

## Upgrading

Keeping up to date is as simple as running `python3 -m pip install --upgrade --user jswipl` from time to time.

## Contributing

Feel free to open tickets if something goes wrong or open pull requests. If you open a pull request do open it onto the `develop` branch. This repository loosely adheres to the [git flow workflow](https://datasift.github.io/gitflow/IntroducingGitFlow.html). The `master` branch is the branch on which only "released" versions are. Anything in development goes into the `develop` branch.

Please do keep in mind that this is just a very small side project and I am unlikely to sink tons of development time into this. However I will try to answer on any issues even if it's just a quick "Yup, would be nice. Please open a pull request someone." and I'll try to handly pull requests quickly.

Anyone who's interested in becoming a co-maintainer: open an issue and let me know. :)
