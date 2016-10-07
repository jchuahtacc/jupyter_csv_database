import pandas
# import qgrid
import ipywidgets as widgets
from IPython.display import display
class Database:
    _column_checks = None
    _item_layout = widgets.Layout(width='15%')
    _box_layout = widgets.Layout(display='flex', flex_flow='row wrap')

    def __init__(self, csv):
        df = pandas.read_csv(csv)
        self._column_checks = tuple(widgets.Checkbox(description=field, value=True, layout=self._item_layout) for field in list(df.columns.values))
        box = widgets.Box(children = self._column_checks, layout=self._box_layout)
        display(box)


