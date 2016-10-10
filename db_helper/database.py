import pandas
from qgrid import show_grid
import ipywidgets as widgets
from IPython.display import display
class Database:
    _csv = None
    _fields_grid = None
    _df = None
    def __init__(self, csv):
        self._csv = csv
        self._df = pandas.read_csv(csv)
        fields = pandas.Series([ field for field in self._df.columns.values], name="Fields")
        raw_cat = pandas.Categorical([ "No" for field in self._df.columns.values], categories=["Yes", "No"])
        show = pandas.Series(raw_cat, name="Show")

        df2 = pandas.concat([fields, show], axis=1)
        display(widgets.HTML("<h3>Jupyter CSV Database</h3><video autoplay loop controls style='float: right'><source src='./db_helper/select_fields.mp4' type='video/mp4'></video><p>First, please choose the fields you wish to view in the table below. You may double click on the \"no\" next to a field name, select \"Yes\" and then click on a different cell to change that field's selection. You may also use the filter controls to search for fields. When you are finished, press OK at the bottom of this cell's output.</p>"))
        self._fields_grid = show_grid(df2)

        ok = widgets.Button(description="OK")
        ok.on_click(self._fields_ok)
        display(ok)

    def _fields_ok(self, b):
        self._fields_grid.export_all(self._fields_export_callback)

    def _fields_export_callback(self, fields_df):
        print self._df[fields_df.loc[fields_df["Show"] == "Yes"]["Fields"].values]
