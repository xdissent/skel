
(function($) {

$.widget('ui.splitpane', {
    
    _init: function() {
        this._setup_panes(true);
    },
    
    _setup_panes: function(init) {
        var self = this, o = this.options;
        
        // TODO: Review
        self.element.addClass('ui-helper-clearfix');

        var width = this.element.width();
        var height = 0;
        
        // Set height to max child element height
        // TODO: Fix for safari
        self.$panes = self.element.children().wrap('<div class="ui-splitpane-pane"></div>').parent().css({float: 'left', width: width / 2}).each(function() {
            if ($(this).height() > height) {
                height = $(this).height();
            }
        }).css({height: height});
        
        // Make the original pane elements match the height
        self.$panes.children(':first-child').each(function() {
            var $this = $(this);
            $this.height(height - ($this.innerHeight() - $this.height()));
        });
        
        self.$panes.resizable({
            // TODO: Fix grid
            grid: [1, 18],
            maxWidth: width - 200,
            minWidth: 200,
            minHeight: height,
            resize: function(e, ui) {
                var height = ui.element.height();
                ui.element.siblings().width(width - ui.element.width()).height(ui.element.height());
                self.$panes.children(':first-child').each(function() {
                    var $this = $(this);
                    $this.height(height - ($this.innerHeight() - $this.height()));
                    $this.children('.ui-tabs-panel').each(function() {
                        $(this).height(height - $(this).position().top - ($(this).innerHeight() - $(this).height()));
                    });
                });
                self._trigger('resize', null, self._ui())
            }
        });
    },
    
    _ui: function() {
        return {
            element: this.element,
        }
    }
    
});

$(function() {
    $('.ui-splitpane').splitpane();
});

})(jQuery);