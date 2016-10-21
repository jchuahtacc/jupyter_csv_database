import pandas
from qgrid import show_grid
from .fields import FieldsWidget
from .tip import TipWidget
import ipywidgets as widgets
from IPython.display import display
import warnings
warnings.filterwarnings('ignore')
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
            self._show_tip = True

        _fields_widget = self._make_fields_widget(fields)

        if self._all_tips or self._fields_tip:
            t = TipWidget()
            t.tip = "Select the fields that you wish to view"
            t.src = "select_fields.mp4"
            display(t)

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
            t = TipWidget()
            t.tip = "If you know the names of the fields in this .csv and you wish to bypass the user interface, you can use the following code"
            t.code = "from neesdb import Database\ndb = new Database('" + self._csv + "')\ndb.show(" + str(fields) + ")"
            display(t)
        df = self._df[fields]
        t = TipWidget()
        t.tip = "Filter the data for the rows you wish to export."
        t.src = "place_holder.mp4"
        display(t)
        self._data_grid = show_grid(df)
        def add_button_click(widget):
            self._data_grid.add_row()

        def remove_button_click(widget):
            self._data_grid.remove_row()

        add_button = widgets.Button(description="Add Row")
        add_button.on_click(add_button_click)
        remove_button = widgets.Button(description="Remove Row")
        remove_button.on_click(remove_button_click)
        export_button = widgets.Button(description="Export Files")
        export_button.on_click(self._export_button_onclick)
        hbox = widgets.HBox(children=[add_button, remove_button, export_button])
        display(hbox)


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
        t = TipWidget()
        t.tip = "Select the fields which contain filenames to export."
        t.video = "place_holder.mp4"
        display(t)

        display(_fields_widget)
        def _click(widget):
            selected_fields = self._get_selected_fields(_fields_widget)
            self._export_continue_onclick(selected_fields)
        ok = widgets.Button(description="Continue")
        ok.on_click(_click)
        display(ok)

