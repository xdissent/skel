(function($) {

$.widget('hz.superimage', {
    
    _init: function() {
        var self = this, o = this.options;
        
        
        // TODO: Perhaps this should be 
        self.idPrefix = self.element.attr('id');
        
        self.fileInput = o.fileInput || 
                self.element.siblings('input[type=file]');
        
        self.widget = self.element.wrap('<div />').parent()
            .addClass(self.widgetBaseClass + ' ' + 'ui-widget');
            
        self.sourcePane = $('<div><ul /></div>')
            .addClass(self.widgetBaseClass + '-source-pane')
            .appendTo(self.widget)
            .tabs();
            
        $(['Current', 'Upload']).each(function() {
            var label = this, name = this.toLowerCase(),
                anchor = '#' + self.idPrefix + '-' + name;
            self.sourcePane.tabs('add', anchor, label);
            self[name + 'Tab'] = self.sourcePane.find(anchor);
            $('<div />').css({overflow: 'auto', height: '100%'})
                .appendTo(self[name + 'Tab']);
        });
        
        this.element.css({
                    width: '100%', 
                    //height: '100%',
                    display: 'block',
                    margin: 0,
                    padding: 0,
                })
            .appendTo(self.currentTab.children());
            // TODO: Add button to toggle off css width or maybe \
            // explicitly set to o.originalSize for "fullsize" mode
            
        self.pluginPane = $('<div><ul /></div>')
            .addClass(self.widgetBaseClass + '-plugin-pane')
            .appendTo(self.widget)
            .tabs();
            
            
        $(o.plugins).each(function() {
            var plugin = this, id = '#' + self.idPrefix + '-' + this.id;
            
            self.pluginPane.tabs('add', id, this.label)
                .find('a[href=' + id + ']')
                .click(function() {
                        if (self.currentPlugin && 
                                self.currentPlugin != self.plugin) {
                            self.currentPlugin.deactivate(self);
                            plugin.activate(self);
                        }
                        self.currentPlugin = plugin;
                        return false;
                    });
            plugin.init(self.widget.find(id), self.element, o.originalSize);
        });
        
        // Activate first plugin since its tab won't get clicked
        o.plugins[0].activate(self);
        self.currentPlugin = o.plugins[0];
        

        // TODO: implement split option
        self.widget.splitpane({
            // TODO: Move this into hz.splitpane.js. It needs to be called.
            resize: function(e, ui) {
                ui.element.find('.hz-splitpane-pane > .ui-tabs')
                    .add('.hz-splitpane-pane > .ui-tabs > .ui-tabs-panel')
                    .each(function() {
                            var $this = $(this),
                                height = $this.parent().height() -
                                        $this.position().top,
                                padding = $(this).outerHeight() - 
                                        $(this).height();
                            $(this).height(height - padding);                    
                        });
                    
                if (self.currentPlugin && self.currentPlugin.resize) {
                    self.currentPlugin.resize();
                }
            }
        });
                
    },
    
    _ui: function() {
        return {
            element: this.element,
            originalSize: this.options.originalSize,
        };
    }    
});


// Plugin prototype
$.hz.superimage.plugin = function(name, prototype) {
    $.hz.superimage.plugins = $.hz.superimage.plugins || {};
    $.hz.superimage.plugins[name] = function(element, panel, options) {
        this.element = element;
        this.name = name;
        this.panel = panel;
        this.options = $.extend({}, options);
    }
    $.hz.superimage.plugins[name].prototype = 
            $.extend($.hz.superimage.plugin, prototype);
}

$.hz.superimage.plugin.prototype = {
    id: 'pluginPrototype',
    label: 'Default Prototype for Plugins',
    
    init: function() {
        console.log('default init');
    },
};




$.hz.superimage.plugins.thumbnail = 

/*
var thumbnail = {
    id:     'thumbnail',
    label:  'Thumbnails',
    init:  function(panel, image, size) {
        var self = this;
        
        self.container = $('<div />')
            .css({overflow: 'auto', height: '100%'})
            .appendTo(panel);
            
        
        self.fields = $(['x1', 'y1', 'x2', 'y2', 'w', 'h', 'title'])
            .each(function() {
                    $('<input />')
                        .attr({
                                type: 'text',
                                name: this,
                            })
                        .appendTo(self.container);
                });
            
        self.resize = function() {
            if (image.crop) {
                image.crop('update');
            }
        };
        
        console.log('init');
    },
    
    _addThumbnail: function() {
        
    },
    
    activate: function(inst) {
        console.log('activate');
        //inst.bind('resize', this.resizeHandler);
    },
    deactivate: function(inst) {
        console.log('deactivate');
        //inst.unbind('resize', this.resizeHandler);
    },
};
*/


$.extend($.hz.superimage, {
    version: '0.1',
    eventPrefix: 'superimage',
    defaults: {
        originalSize: false,
        plugins: ['thumbnail', 'resize'],
    }
});


})(jQuery);