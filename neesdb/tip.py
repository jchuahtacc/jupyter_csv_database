from ipywidgets import DOMWidget
from traitlets import Unicode

class TipWidget(DOMWidget):
    _view_module = Unicode('nbextensions/neesdb/tip', sync=True)
    _view_name = Unicode('TipWidgetView', sync=True)
    tip = Unicode().tag(sync=True)
    code = Unicode().tag(sync=True)
    src = Unicode().tag(sync=True)

    def __init__(self, *args, **kwargs):
        super(TipWidget, self).__init__(*args, **kwargs)

