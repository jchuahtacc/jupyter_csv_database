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
            this.$table = this.getTableSkeleton();
            this._fields = { };
            $(this.el).append(this.$table);
            this.listenTo(this.model, 'change:fields', this._fields_changed, this);
            this._fields_changed()
        },

        getTableSkeleton() {
            var $table = $("<table class='table table-striped table-bordered'></table>");
            var $header = $("<tr data-role='header'><th class='primary'>Field</th><th class='primary'>Select</th></tr>").appendTo($table);
            return $table;
        },

        inputClick(e) {
            var key = $(e.target).prop('name');
            var value = $(e.target).val() == 'Yes';
            var that = e.data.context;
            that._fields[key] = value;
            var msg = { 'type' : 'select', 'field' : key, 'value' : value };
            that.send(msg);
        },

        makeRow(field, value) {
            var $tr = $("<tr data-role='field'><td>" + field + "</td></tr>");
            var $td = $("<td data-role='select'></td>");
            $td.appendTo($tr);
            var context = { context : this };
            var $yes = $("<input type='radio' name='" + field + "' value='Yes'>&nbsp;Yes&nbsp;</input>");
            $yes.click(context, this.inputClick);
            var $no = $("<input type='radio' name='" + field + "' value='No'>&nbsp;No&nbsp;</input>");
            $no.click(context, this.inputClick);
            if (value) {
                $yes.prop('checked', true);
            } else {
                $no.prop('checked', true);
            }
            $yes.appendTo($td);
            $no.appendTo($td);
            return $tr;
        },

        _fields_changed: function() {
            new_fields = this.model.get('fields');
            this.$table.find("tr [data-role='field']").remove();
            var keys = Object.keys(new_fields);
            for (var i in keys) {
                var key = keys[i];
                if (this._fields[key] == undefined) {
                    this._fields[key] = new_fields[key];
                    this.$table.append(this.makeRow(key, this._fields[key]));
                } else {
                    this._fields[key] = new_fields[key];
                    var $yes = this.$table.find("input[name='" + key + "'][value='Yes']");
                    var $no = this.$table.find("input[name='" + key + "'][value='No']");
                    $yes.prop('checked', new_fields[key]);
                    $no.prop('checked', !new_fields[key]);
                }
            }
        }
    });

    return {
        FieldsWidgetView: FieldsWidgetView
    }
});
