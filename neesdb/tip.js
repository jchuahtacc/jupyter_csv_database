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

            this.$view = $("<div style='border-left: 6px solid #ccc!important; background-color: #ddddff!important; padding: 0.01em 16px; padding-bottom:   16px;'><h4>neesdb tip:</h4><table style='width: 100%;'><tr><td data-role='left' style='vertical-align: top; padding-right: 10px;'><p data-role='tip' class='hidden'></p><br /><code data-role='code' class='hidden'></code></td><td data-role='right'><video style='width: 100%;' data-role='video' autoplay loop controls style='float: right' class='hidden'><source data-role='src' type='video/mp4'></video></td></tr></table></div>");
            $(this.el).append(this.$view);
            this.listenTo(this.model, 'change:tip', this.tip_changed, this);
            this.listenTo(this.model, 'change:code', this.code_changed, this);
            this.listenTo(this.model, 'change:src', this.src_changed, this);
            this.tip_changed();
            this.code_changed();
            this.src_changed();
        },

        tip_changed: function() {
            var tip = this.model.get('tip');
            if (tip && tip.length > 0) {
                this.$view.find("[data-role='tip']").html(tip).removeClass("hidden");
            } else {
                this.$view.find("[data-role='tip']").html("").addClass("hidden");
            }
        },

        code_changed: function() {
            var code = this.model.get('code');
            if (code && code.length > 0) {
               this.$view.find("[data-role='code']").html(code).removeClass("hidden");
            } else {
               this.$view.find("[data-role='code']").html("").addClass("hidden");
            } 
        },

        src_changed: function() {
            var src = this.model.get('src');
            if (src && src.length > 0) {
                this.$view.find("[data-role='left']").css('width', '50%');
                this.$view.find("[data-role='right']").css('width', '50%');
                this.$view.find("[data-role='src']").attr('src', '/nbextensions/neesdb/tips/' + src);
                this.$view.find("[data-role='video']").removeClass("hidden");
            } else {
                this.$view.find("[data-role='left']").css('width', '100%');
                this.$view.find("[data-role='right']").css('width', '0%');
                this.$view.find("[data-role='video']").addClass("hidden");
            }
        }
    });

    return {
        TipWidgetView: TipWidgetView
    }
});
