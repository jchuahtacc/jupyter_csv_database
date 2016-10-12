import pandas
from qgrid import show_grid
import ipywidgets as widgets
from IPython.display import display
class Database:
    _csv = None
    _fields_grid = None
    _df = None
    _fields = None
    _fields_tip = False
    _show_tip = False
    _all_tips = False
    _data_grid = None
    _export_fields = None
    _export_fields_grid = None
    _visible_fields = None
    _export_fields_view_tip = False

    def __init__(self, csv, tips=False):
        self._all_tips = tips
        self._csv = csv
        self._df = pandas.read_csv(csv)
        self._fields = pandas.Series([ field for field in self._df.columns.values], name="Fields")

    def _fields_ok(self, b):
        self._fields_grid.export_all(self._fields_export_callback)

    def _fields_export_callback(self, fields_df):
        fields_array = fields_df[fields_df == "Yes"]
        if self._all_tips or self._fields_tip:
            self._code("<p>You can pre-select fields in the query interface if you know the names of the fields that you would like to query. To repeat this query, use this code:", "db.fields(" + str(fields_array) + ")")
        self._show_tip = True
        self.show(fields_df.loc[fields_df["Show"] == "Yes"]["Fields"].values)

    def _tip(self, text):
        display(widgets.HTML("<div style='border-left: 6px solid #ccc!important; background-color: #ddddff!important; padding: 0.01em 16px; padding-bottom: 16px;'><h4>neesdb tip:</h4>" + text + "</div>"))

    def _code(self, text, code, code_header=True):
        tip_string = "<p>" + text + "</p><br /><code>"
        if code_header:
            tip_string = tip_string + "from neeshub import Database\ndb = Database('" + self._csv + "')\n"
        tip_string = tip_string + code + "</code>"
        self._tip(tip_string)

    def _video(self, text, video):
        self._tip("<table><tr><td style='vertical-align: top; padding-right: 10px;'><p>" + text + "</p></td><td><video autoplay loop controls style='float: right'><source src='" + video + "' type='video/mp4'></video></td></tr></table>")


    def _check_bad_fields(self, fields=None):
        if (fields is not None):
            fieldseries = pandas.Series(fields)
            mismatch = fieldseries.isin(self._fields.values)
            mismatch = mismatch[mismatch == False]
            if (mismatch.size > 10):
                badfields = []
                for index, value in mismatch.iteritems():
                    badfields.append(fields[index])
                raise ValueError("The following fields are not in this .csv file: " + str(badfields))


    def _generate_field_selector(self, fields=None, name="Show"):
        raw_cat = pandas.Categorical([ "No" for field in self._df.columns.values], categories=["Yes", "No"])
        show = pandas.Series(raw_cat, name=name, index=self._fields)
        if fields is not None:
            show[fields] = "Yes"
        df2 = pandas.concat([show], axis=1)
        return df2

    def fields(self, fields=None):
        if (fields is not None):
            self._check_bad_fields(fields)
        else:
            self._fields_tip = True

        df2 = self._generate_field_selector(fields)

        if self._all_tips or self._fields_tip:
            self._video("Choose the fields you wish to view in the table below. You may double click on the \"no\" next to a field name, select \"Yes\" and then click on a different cell to change that field's selection. You may also use the filter controls to search for fields. When you are finished, press OK at the bottom of this cell's output.", "./neesdb/select_fields.mp4")
        self._fields_grid = show_grid(df2)
#
        ok = widgets.Button(description="OK")
        ok.on_click(self._fields_ok)
        display(ok)

    def _export_button_onclick(self, b):
        self._export_fields_view_tip = True
        self._export_fields_view()

    def show(self, fields=None):
        self._visible_fields = fields
        if self._all_tips or self._show_tip:
            self._code("If you know the names of the fields in this .csv, you can show them directly using the following code:", "db.show(" + str(fields) + ")")
        df = self._df[fields]
        self._data_grid = show_grid(df)
        export_button = widgets.Button(description="Export Files")
        export_button.on_click(self._export_button_onclick)
        display(export_button)

    def _export_fields_view(self, fields=None):
        if self._visible_fields is None:
            raise ValueError("No fields are in the current display. You must first call db.show() with a list of fields to query.")
        if fields is not None:
            self._check_bad_fields(fields)
        else:
            self._export_fields_view_tip = True

        if self._all_tips or self._export_fields_view_tip:
            pass
        df2 = self._generate_field_selector(fields, name="Files")
        self._export_files_grid = show_grid(df2)


