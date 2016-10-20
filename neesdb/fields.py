from ipywidgets import DOMWidget
from traitlets import Unicode, Int

class FieldsWidget(DOMWidget):
    _view_module = Unicode('nbextensions/neesdb/neesdb', sync=True)
    _view_name = Unicode('FieldsWidgetView', sync=True)
    count = Int(sync=True)
