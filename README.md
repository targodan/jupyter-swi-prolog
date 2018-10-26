# jupyter-swi-prolog
A Jupyter Kernel for SWI-Prolog.

Inspired by [madmax2012/SWI-Prolog-Kernel](https://github.com/madmax2012/SWI-Prolog-Kernel).

**USE WITH CARE!***

This kernel is only barely tested using jupyter lab on debian linux. If anyone tests it e. g. on plain jupyter and/or windows feel free to open a ticket to report success and/or failure.

I have only just started out learning prolog and have not tested this kernel with all language constructs of prolog yet. There might still be problems with more advanced prolog stuff.

**Changes likely!***

So far the installation is rather uncomfortable (see below). In the long run it would be nice to have a proper pip package and an install command. This means however that the installation process would completely change and there would probably be some renaming and refactoring happening. Potentially even down to the filename.

If you still want to use it already feel free to follow the installation steps below. Keep an eye on #3 as any pip-progress will be reported there.

## Usage Notes and Limitations

The knowledge base is only available from within the **same cell**. So any queries in a cell must be solvable for prolog with the data contained in the same cell the query is located in.

Any query starts with `?-` any line that does not start with `?-` is written to a temporary file that `swipl` gets as script input.

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

## Supported environments

Only **pyhton3** is supported (anybody still using python2 should really have upgraded by now...) and it was only tested on **linux** as I have no jupyter installation on windows. In theory it should work on windows though.

## Installation

1. Install [SWI-Prolog](http://www.swi-prolog.org) and make sure `swipl` is available in your `PATH`.
2. Change directory to your jupyters kernel directory. In my case this is `/home/jupyter/.local/share/jupyter/kernels`.
3. `git clone https://github.com/targodan/jupyter-swi-prolog.git swi-prolog && cd swi-prolog`
4. Change the file `kernel.json` such that the path in line 4 matches where you just cloned this repository to.
5. Restart jupyter
6. Profit

## Contributing

Feel free to open tickets if something goes wrong or open pull requests. If you open a pull request do open it onto the `develop` branch. This repository loosely adheres to the [git flow workflow](https://datasift.github.io/gitflow/IntroducingGitFlow.html). The `master` branch is the branch on which only "released" versions are. Anything in development goes into the `develop` branch.

Please do keep in mind that this is just a very small side project and I am unlikely to sink tons of development time into this. However I will try to answer on any issues even if it's just a quick "Yup, would be nice. Please open a pull request someone." and I'll try to handly pull requests quickly.

Anyone who's interested in becoming a co-maintainer: open an issue and let me know. :)
