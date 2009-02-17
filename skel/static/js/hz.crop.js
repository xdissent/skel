(function($) {

$.widget('hz.crop', {
    
    _init: function() {
        this._setup_image(true);
    },
    
    
    _screen_coords: [0, 0, 0, 0],
    
    _image_coords: [0, 0, 0, 0],
    
    // coords
    select: function(image_coords) {
        var self = this, o = this.options;

        this._image_coords = image_coords;
        self._screen_coords = [
            image_coords[0] * self.element.width() / o.original_size[0],
            image_coords[1] * self.element.height() / o.original_size[1],
            image_coords[2] * self.element.width() / o.original_size[0],
            image_coords[3] * self.element.height() / o.original_size[1],
        ];
        
        self.$selection.css({
            left: self._screen_coords[0],
            top: self._screen_coords[1],
            width: self._screen_coords[2] - self._screen_coords[0],
            height: self._screen_coords[3] - self._screen_coords[1],
        });
        this._trigger('select', null, this._ui());
    },
    
    
    _select: function(screen_coords) {
        var self = this, o = this.options;
        
        self._screen_coords = screen_coords;
        self._image_coords = [
            screen_coords[0] * o.original_size[0] / self.element.width(),
            screen_coords[1] * o.original_size[1] / self.element.height(),
            screen_coords[2] * o.original_size[0] / self.element.width(),
            screen_coords[3] * o.original_size[1] / self.element.height(),
        ];
    },
    
    
    _setup_image: function(init) {
        var self = this, o = this.options;
        
        if (init) {
            self.element.css({display: 'block', margin: 0});
        
            self.$widget = self.element.wrap($('<div class="' + self.widgetBaseClass + '"></div>')
                .css({position: 'relative'}))
                .parent().click(function() {
                    console.log('click');
                });
                
            self.$selection = $('<div class="' + self.widgetBaseClass + '-selection"></div>')
                .appendTo(self.$widget)
                .css({position: 'absolute', border:'1px solid #f00', top: 0, left: 0})
                //.resizable({containment: 'parent'})
                .draggable({
                    containment: 'parent',
                    drag: function(e, ui) {
                        self._select([
                            ui.position.left, 
                            ui.position.top, 
                            ui.position.left + ui.helper.width(), 
                            ui.position.top + ui.helper.height(),
                        ]);
                    },
                })
                .resizable({
                    aresize: function(e, ui) {
                        console.log(ui.size);
                    },
                });
                
            self.select([0, 0, 100, 100]);
        }
    },
    
    
    resize: function() {
        console.log('callin me');
        var self = this, o = this.options;
        //self.select(self._image_coords);
    },
    
    
    _ui: function() {
        return {
            element: this.element,
            coords: this._coords,
        };
    },
    
});


$.extend($.hz.crop, {
    version: '0.1',
    eventPrefix: 'crop',
    defaults: {
        original_size: [0, 0],
    }
});
    

})(jQuery);