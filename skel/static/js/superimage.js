
(function($) {

$.widget('ui.superimage', {
    
    _init: function() {
        this._setup_image(true);
    },
    
    _setup_image: function(init) {
        var self = this, o = this.options;
        
        self.id_prefix = this.element.attr('id') + '-' + self.widgetBaseClass;
        
        self.original_size = [this.element.width(), this.element.height()];
        console.log(self.original_size);
        self.original_size = [640, 480];
                
        self.$widget = self.element.wrap('<div class="ui-superimage-widget"></div>').parent();
        
        self.$original = $('<div class="' + self.widgetBaseClass + '-original"><ul><li><a href="#' + self.id_prefix +
            '-current" class="' + self.widgetBaseClass + '-current-tab" title="Current Image"><span>Current</span></a></li>' +
            '<li><a href="#' + self.id_prefix + '-upload" class="' + self.widgetBaseClass + '-upload-tab" title="Upload">' +
            '<span>Upload</span></a></li>' + '</ul>'+
            '<div id="' + self.id_prefix + '-current" class="' + self.widgetBaseClass + '-current"></div>' +
            '<div id="' + self.id_prefix + '-upload" class="' + self.widgetBaseClass + '-upload"><p>upload</p></div>' +
        '</div>');
        self.$plugins = $('<div class="' + self.widgetBaseClass + '-plugins"><ul></ul></div>');

        self.$widget.append(self.$original);
        self.$widget.append(self.$plugins);
            
        self.$original.find('.ui-superimage-current').append(this.element);
        this.element.css({width: '100%'});


    
        self.$widget.splitpane({
            resize: function(e, ui) {
                self._trigger('resize', null, self._ui());
            },
        });
        
        $.each(o.plugins, function() {
            self.$plugins.find('ul').append(
                '<li><a href="#' + self.id_prefix  + '-' + this.id + 
                '" class="' + self.widgetBaseClass + '-' + this.id + '-tab" title="' + 
                this.label + '"><span>' + this.label + '</span></a></li>'
            ).after(
                '<div id="' + self.id_prefix  + '-' + this.id + '"></div>'
            );
            this._init(self._ui());
        });
        self._trigger('plugin_init', null, self._ui());
        
        self.$original.tabs();
        self.$plugins.tabs();
        
    },
        
    _ui: function() {
        return {
            widget: this.$widget,
            element: this.element,
            id_prefix: this.id_prefix,
            prefix: this.widgetBaseClass,
            original_size: this.original_size,
        };
    }    
});


var thumbnail = {
    id:     'thumbnail',
    label:  'Thumbnails',
    _init:  function(ui) {
    
        $(ui.element).wrap('<div></div>').crop({ original_size: ui.original_size });
        var image = ui.element;
        ui.widget.bind('resize', function(e, ui) {
            image.crop('resize');
        });
    },
};

$.extend($.ui.superimage, {
    getter: '',
    version: '0.1',
    eventPrefix: 'superimage',
    defaults: {
        plugins: [
            thumbnail,
            {   id:     'resize',
                label:  'Resize',
                _init:  function(superimage) {
                },
            },
        ]
    }
});


$(function() {
    $('.ui-superimage').superimage();
});

})(jQuery);