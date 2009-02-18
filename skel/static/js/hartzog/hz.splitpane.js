
(function($) {

$.widget('hz.splitpane', {
    
    _init: function() {
        var self = this, o = this.options;
        
        self.element.addClass(self.widgetBaseClass + 
                ' ui-widget ui-helper-clearfix')
            .css({position: 'relative'});

        var width = o.width || this.element.width();
        var height = o.height;
        
        self.panes = self.element.children().wrap('<div />').parent()
            .addClass(self.widgetBaseClass + '-pane')
            .each(function() {
                    // Set height to max child element height w/ no option
                    if (!o.height && $(this).height() > height) {
                        height = $(this).height();
                    }
                })
            .css({float: 'left', width: width / 2, height: height});
            
        if (o.minHeight && o.minHeight > height) {
            height = o.minHeight;
        }
        
        // Make the original pane elements match the height
        self.panes.children().each(function() {
            var $this = $(this);
            $this.height(height - ($this.innerHeight() - $this.height()));
        });
        
        
        self.panes.resizable({
            grid: o.grid,
            maxWidth: width - o.minWidth,
            minWidth: o.minWidth,
            minHeight: height,
            maxHeight: o.maxHeight,
            resize: function(e, ui) {
                var height = ui.element.height();
                ui.element.siblings().width(width - ui.element.width()).height(ui.element.height());
                self._trigger('resize', null, self._ui());
            }
        });
        
        self._trigger('resize', null, self._ui());
    },
    
    _ui: function() {
        return {
            element: this.element,
        }
    }
    
});

$.extend($.hz.splitpane, {
    version: '0.1',
    eventPrefix: 'splitpane',
    defaults: {
        width: false,
        height: false,
        minHeight: false,
        maxHeight: 800,
        minWidth: 200,
        grid: [1, 1],
    }
});

})(jQuery);