import pandas
import json
from qgrid import QGridWidget
from .fields import FieldsWidget
from .tip import TipWidget
import ipywidgets as widgets
from IPython.display import display
from ipywidgets_file_selector import IPFileSelector
import zipfile
import os
import numpy as np

import warnings
warnings.filterwarnings('ignore')

class Database:
    _csv = None
    _fields_grid = None
    _df = None
    _show_df = None
    _fields = None
    _fields_tip = False
    _show_tip = False
    _all_tips = False
    _data_grid = None
    _export_fields = None
    _export_fields_grid = None
    _visible_fields = None
    _export_fields_view_tip = False
    _grid_options = {
        'fullWidthRows': True,
        'syncColumnCellResize': True,
        'forceFitColumns': True,
        'defaultColumnWidth': 150,
        'rowHeight': 28,
        'enableColumnReorder': False,
        'enableTextSelectionOnCells': True,
        'editable': True,
        'autoEdit': False,
        'multiSelect' : False
    }
    _add_files_box = None
    _export_files_box = None

    def __init__(self, csv, tips=False):
        self._all_tips = tips
        self._csv = csv
        self._df = pandas.read_csv(csv, index_col=False)
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
            #t.src = "select_fields.mp4"
            display(t)

        display(_fields_widget)
        def _click(widget):
            _fields_widget.close()
            widget.close()
            self.show(self._get_selected_fields(_fields_widget))
        ok = widgets.Button(description="OK")
        ok.on_click(_click)
        display(ok)

    def _possible_file_fields(self):
        valid_fields = [ ]
        for field in self._visible_fields:
            series = self._show_df[field]
            for index, value in series.iteritems():
                valuestr = str(value)
                if valuestr is not None and not valuestr == "nan":
                    try:
                        if unicode(value).isnumeric():
                            break
                        json.loads(value)
                    except Exception:
                        break
                if index == series.size - 1:
                    valid_fields.append(field)
        return valid_fields

    def _get_file_list(self, tree):
        filelist = [ ]
        def _recurse_file_tree(subtree, path):
            for key, value in subtree.iteritems():
                if type(value) is dict:
                    _recurse_file_tree(subtree[key], key + "/")
                else:
                    filelist.append(path + key)
        _recurse_file_tree(tree, "")
        return filelist

    def export(self, fields=None, filename=None):
        try:
            zip = zipfile.ZipFile(filename, 'w')
            self._df.loc[self._data_grid.filtered].to_csv('__temp.csv', index=False)
            zip.write('__temp.csv', self._csv, zipfile.ZIP_DEFLATED)
            os.remove('__temp.csv')
            for field in fields:
                for index in self._data_grid.filtered:
                    series = self._data_grid.df[field]
                    files = series[index]
                    if not (str(files) == "nan"):
                        try:
                            tree = json.loads(files)
                            filelist = self._get_file_list(tree)
                            for f in filelist:
                                try:
                                    if os.path.isdir(f):
                                        for (dirpath, dirnames, filenames) in os.walk(f):
                                            for subfile in filenames:
                                                subpath = os.sep.join([dirpath, subfile])
                                                zip.write(subpath, subpath, zipfile.ZIP_DEFLATED)
                                    zip.write(f, f, zipfile.ZIP_DEFLATED)
                                except Exception:
                                    print "Couldn't find file: ", f

                        except Exception:
                            pass
            html = widgets.HTML("Your exported files are available for download: <a href='./" + filename + "'>" + filename + "</a>")
            display(html)
            pass
        except IOError:
            t = TipWidget()
            t.tip = "You entered an invalid filename."

    def show(self, fields=None):
        self._visible_fields = fields
        if self._all_tips or self._show_tip:
            t = TipWidget()
            t.tip = "If you know the names of the fields in this .csv and you wish to bypass the user interface, you can use the following code"
            t.code = "from neesdb import Database\ndb = new Database('" + self._csv + "')\ndb.show(" + str(fields) + ")"
            display(t)
        if fields is not None:
            self._show_df = self._df[fields]
        else:
            self._show_df = self._df
        t = TipWidget()
        t.tip = "Filter the data for the rows you wish edit or view. You may add or remove rows from the database, add file references to the currently selected row, and export all files in the current view. If you modify, add or remove data or files, make sure you click 'Save changes'."
        #t.src = "place_holder.mp4"
        display(t)
        self._data_grid = QGridWidget(df=self._show_df, grid_options=self._grid_options)
        display(self._data_grid)
        def add_button_click(widget):
            self._data_grid.add_row()

        def remove_button_click(widget):
            sel = self._data_grid.get_selected_rows()
            if len(sel) > 0:
                self._df = self._df.drop(self._df.index[sel])
                self._data_grid.remove_row()

        def add_files_button_click(widget):
            selected_rows = self._data_grid.get_selected_rows()
            if len(selected_rows) > 0:
                fields = self._possible_file_fields()
                label = widgets.Label(value="Select a field to add files")
                display(label)
                radio = widgets.RadioButtons(options=fields)
                display(radio)
                def go_for_files(widget):
                    label.close()
                    radio.close()
                    widget.close()
                    tip = TipWidget()
                    tip.tip = "Select files to place in this field."
                    display(tip)
                    existing = self._show_df[radio.value][self._data_grid.get_selected_rows()[0]]
                    selected = dict()
                    if not np.isnan(existing) and  len(str(existing)) > 0:
                        selected = json.loads(existing)
                    files = IPFileSelector(selected=selected)
                    display(files)
                    def ok_file_select(widget):
                        newjson = json.dumps(files.selected)
                        self._data_grid.df[radio.value][self._data_grid.get_selected_rows()[0]] = newjson
                        self._data_grid._df_changed()
                        tip.close()
                        files.close()
                        widget.close()
                    ok = widgets.Button(description="OK")
                    ok.on_click(ok_file_select)
                    display(ok)
                    pass
                ok = widgets.Button(description="OK")
                ok.on_click(go_for_files)
                display(ok)
                self._add_files_box=widgets.Box(children=[label, radio, ok])

        def save_button_click(widget):
            self._df.update(self._data_grid.df)
            outer = pandas.merge(self._df, self._data_grid.df, how='outer')
            left_series = [ ]
            for col in self._df.columns:
                if not col in self._data_grid.df.columns:
                    left_series.append(col)
            diff = outer[outer.isin(self._df)][left_series]
            outer[diff.isnull()] = np.nan
            self._df = outer
            self._df.to_csv(self._csv, index=False)
            display(widgets.HTML("<script>alert('Changes saved to " + self._csv + "');</script>"))
            pass

        def export_button_click(widget):
            fields = self._possible_file_fields()
            label = widgets.Label(value="Select fields containing files you wish to export")
            display(label)
            checks = [ widgets.Checkbox(description=field) for field in fields ]
            box = widgets.Box(children=checks)
            display(box)
            ok = widgets.Button(description="OK")
            display(ok)
            def export_ok_click(widget):
                export_fields = [ ]
                for check in checks:
                    if check.value:
                        export_fields.append(check.description)
                label.close()
                box.close()
                widget.close()
                explabel = widgets.Label(value="Enter a name for the zipfile that will contain your exported files")
                display(explabel)
                expfilename = widgets.Text(placeholder='filename')
                display(expfilename)
                def expfilename_ok_click(widget):
                    explabel.close()
                    filename = expfilename.value
                    expfilename.close()
                    expfilename_ok.close()
                    widget.close()
                    if len(filename) > 0:
                        filename = filename.strip()
                        if not filename.endswith(".zip"):
                            filename = filename + ".zip"
                        self.export(fields=export_fields, filename=filename)
                    pass
                expfilename_ok = widgets.Button(description="OK")
                expfilename_ok.on_click(expfilename_ok_click)
                display(expfilename_ok)
            ok.on_click(export_ok_click)

        save_button = widgets.Button(description='Save changes')
        save_button.on_click(save_button_click)
        add_button = widgets.Button(description="Add row")
        add_button.on_click(add_button_click)
        remove_button = widgets.Button(description="Remove row")
        remove_button.on_click(remove_button_click)
        add_files_button = widgets.Button(description="Add files")
        add_files_button.on_click(add_files_button_click)
        export_button = widgets.Button(description="Export files")
        export_button.on_click(export_button_click)
        hbox = widgets.HBox(children=[save_button, add_button, remove_button, add_files_button, export_button])
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
#        t.video = "place_holder.mp4"
        display(t)

        display(_fields_widget)
        def _click(widget):
            selected_fields = self._get_selected_fields(_fields_widget)
            self._export_continue_onclick(selected_fields)
        ok = widgets.Button(description="Continue")
        ok.on_click(_click)
        display(ok)

