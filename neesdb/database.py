import pandas
from qgrid import show_grid
import ipywidgets as widgets
from IPython.display import display
class Database:
    _csv = None
    _fields_grid = None
    _df = None
    fields = None
    def __init__(self, csv):
        self._csv = csv
        self._df = pandas.read_csv(csv)
        self.fields = pandas.Series([ field for field in self._df.columns.values], name="Fields")

    def _fields_ok(self, b):
        self._fields_grid.export_all(self._fields_export_callback)

    def _fields_export_callback(self, fields_df):
        fields_array = fields_df.loc[fields_df["Show"] == "Yes"]["Fields"].values;
        self._display_query_code(fields_array)
        print self._df[fields_df.loc[fields_df["Show"] == "Yes"]["Fields"].values]

    def _tip(self, text):
        return "<div style='border-left: 6px solid #ccc!important; background-color: #ddddff!important; padding: 0.01em 16px; padding-bottom: 16px;'>" + text + "</div>"

    def _display_query_code(self, fields_array):
        display(widgets.HTML(self._tip("<h4>neesdb tip:</h4><p>You can pre-select fields in the query interface if you know the names of the fields that you would like to query. To repeat this query, use this code:</p><br /><code>from neeshub import Database\ndb = Database('" + self._csv + "')\ndb.query(fields=" + str(fields_array) + ")</code>")))

    def query(self, fields=None):
        if (fields is not None):
            fieldseries = pandas.Series(fields)
            mismatch = fieldseries.isin(self.fields.values)
            mismatch = mismatch[mismatch == False]
            if (mismatch.size > 10):
                badfields = []
                for index, value in mismatch.iteritems():
                    badfields.append(fields[index])
                raise ValueError("The following fields are not in this .csv file: " + str(badfields))
        raw_cat = pandas.Categorical([ "No" for field in self._df.columns.values], categories=["Yes", "No"])
        show = pandas.Series(raw_cat, name="Show")
        df2 = pandas.concat([self.fields, show], axis=1)
        if (fields is not None):
            df3 = df2[df2['Fields'].isin(fields)]
            for index, value in df3["Fields"].iteritems():
                df2.set_value(index, "Show", "Yes")

        display(widgets.HTML("<h3>neesdb Query</h3><video autoplay loop controls style='float: right'><source src='./neesdb/select_fields.mp4' type='video/mp4'></video><p>First, please choose the fields you wish to view in the table below. You may double click on the \"no\" next to a field name, select \"Yes\" and then click on a different cell to change that field's selection. You may also use the filter controls to search for fields. When you are finished, press OK at the bottom of this cell's output.</p>"))
        self._fields_grid = show_grid(df2)

        ok = widgets.Button(description="OK")
        ok.on_click(self._fields_ok)
        display(ok)

