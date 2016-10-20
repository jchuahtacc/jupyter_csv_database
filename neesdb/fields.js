if (IPython.version[0] === '4' && parseInt(IPython.version[2]) >= 2) {
    var path = 'jupyter-js-widgets';
} else {
    var path = 'widgets/js/widget';
    if (IPython.version[0] !== '3') {
        path = 'nbextensions/widgets/' + path;
    }
}

define(['jquery', path ], function($, widget) {
    var FieldsWidgetView = widget.DOMWidgetView.extend({
        render: function() {
            FieldsWidgetView.__super__.render.apply(this, arguments);
            this._count_changed();
            this.listenTo(this.model, 'change:count', this._count_changed, this);
        },

        _count_changed: function() {
            var old_value = this.model.previous('count');
            var new_value = this.model.get('count');
            $(this.el).text(String(old_value) + ' -> ' + String(new_value));
        }
    });

    return {
        FieldsWidgetView: FieldsWidgetView
    }
});
