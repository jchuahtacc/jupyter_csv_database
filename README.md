# Jupyter CSV "Database"

Using a Jupyter Notebook to read, filter and export data from a CSV file

### Setup

This project requires `ipywidgets` and `qgrid`. I have submitted a [pull request](https://github.com/quantopian/qgrid/pull/93) to [quantopian/qgrid](https://github.com/quantopian/qgrid) that implements an `export_view` function, required for this project. Until it is merged, the necessary functionality is available in the fork [jchuahtacc/qgrid](https://github.com/jchuahtacc/qgrid).

I used the following statements to enable the necessary widgets and notebook extensions:

```
conda install -c conda-forge ipywidgets
conda install -c conda-forge qgrid
jupyter nbextension enable --py --sys-prefix widgetsnbextension
```

Then, I added qgrid's widgets by using:

```
import qgrid
qgrid.nbinstall()
```

At this point, QGrid and its `qgridjs` widgets must be patched from [jchuahtacc/qgrid](https://github.com/jchuahtacc/qgrid)
