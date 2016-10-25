from ipywidgets import DOMWidget
from traitlets import Unicode, Dict

class FieldsWidget(DOMWidget):
    _view_module = Unicode('nbextensions/neesdb/fields', sync=True)
    _view_name = Unicode('FieldsWidgetView', sync=True)
    fields = Dict().tag(sync=True)

    def __init__(self, *args, **kwargs):
        super(FieldsWidget, self).__init__(*args, **kwargs)
        self.fields = kwargs.get('fields', dict())
        self.on_msg(self._handleMsg)

    def _handleMsg(self, widget, content, buffers=None):
        if (content['type'] == 'select'):
            self.fields[content['field']] = content['value']
