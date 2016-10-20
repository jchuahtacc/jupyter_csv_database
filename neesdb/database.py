import pandas
from qgrid import show_grid
from .fields import FieldsWidget
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

    def _get_selected_fields(self, widget):
        fields_array = [ ]
        for field in widget.fields:
            if widget.fields[field]:
                fields_array.append(field)
        return fields_array

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

    def _make_fields_widget(self, fields):
        _fields_widget = FieldsWidget()
        fields_dict = dict((field, False) for field in self._df.columns.values)
        if fields is not None:
            for field in fields:
                fields_dict[field] = True
        _fields_widget.fields = fields_dict
        return _fields_widget

    def fields(self, fields=None):
        if (fields is not None):
            self._check_bad_fields(fields)
        else:
            self._fields_tip = True

        _fields_widget = self._make_fields_widget(fields)

        if self._all_tips or self._fields_tip:
            self._video("Choose the fields you wish to view in the table below. You may double click on the \"no\" next to a field name, select \"Yes\" and then click on a different cell to change that field's selection. You may also use the filter controls to search for fields. When you are finished, press OK at the bottom of this cell's output.", "./neesdb/select_fields.mp4")

        display(_fields_widget)
        def _click(widget):
            self.show(self._get_selected_fields(_fields_widget))
        ok = widgets.Button(description="OK")
        ok.on_click(_click)
        display(ok)

    def _export_button_onclick(self, b):
        self._export_fields_view_tip = True
        self._export_fields_view()

    def show(self, fields=None):
        self._visible_fields = fields
        if self._all_tips or self._show_tip:
            self._code("If you know the names of the fields in this .csv, you can show them directly using the following code:", "db.show(" + str(fields) + ")")
        df = self._df[fields]
        self._video("Filter the data for the rows that you wish to export.", "./neesdb/select_fields.mp4")
        self._data_grid = show_grid(df)
        export_button = widgets.Button(description="Export Files")
        export_button.on_click(self._export_button_onclick)
        display(export_button)

    def _export_continue_onclick(self, b):
        # Ask for export filename
        pass

    def _export_fields_view(self, fields=None):
        if self._data_grid is None:
            raise ValueError("No data has been retrieved in the current display.")
        if fields is not None:
            self._check_bad_fields(fields)
        else:
            self._export_fields_view_tip = True

        _fields_widget = self._make_fields_widget(fields)

        if self._all_tips or self._export_fields_view_tip:
            pass
        self._video("Please select which fields contain filenames to export.", "./neesdb/select_fields.mp4")

        display(_fields_widget)
        def _click(widget):
            selected_fields = self._get_selected_fields(_fields_widget)
            self._export_continue_onclick(selected_fields)
        ok = widgets.Button(description="Continue")
        ok.on_click(_click)
        display(ok)
