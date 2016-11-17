if (IPython.version[0] === '4' && parseInt(IPython.version[2]) >= 2) {
    var path = 'jupyter-js-widgets';
} else {
    var path = 'widgets/js/widget';
    if (IPython.version[0] !== '3') {
        path = 'nbextensions/widgets/' + path;
    }
}

define(['jquery', path ], function($, widget) {
    var TipWidgetView = widget.DOMWidgetView.extend({
        render: function() {
            TipWidgetView.__super__.render.apply(this, arguments);

            this.$view = $("<div style='border-left: 6px solid #ccc!important; background-color: #ddddff!important; padding: 0.01em 16px; padding-bottom:   16px;'><br /><p data-role='tip' class='hidden'></p></div>");
            $(this.el).append(this.$view);
            this.listenTo(this.model, 'change:tip', this.tip_changed, this);
            this.listenTo(this.model, 'change:code', this.code_changed, this);
            this.listenTo(this.model, 'change:src', this.src_changed, this);
            this.tip_changed();
            var that = this;
        },

        tip_changed: function() {
            var tip = this.model.get('tip');
            if (tip && tip.length > 0) {
                this.$view.find("[data-role='tip']").html(tip).removeClass("hidden");
            } else {
                this.$view.find("[data-role='tip']").html("").addClass("hidden");
            }
        },

    });

    return {
        TipWidgetView: TipWidgetView
    }
});
