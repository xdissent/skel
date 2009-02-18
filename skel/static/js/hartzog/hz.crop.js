(function($) {

$.widget('hz.crop', $.extend({}, $.ui.mouse, {


    _coords: [0, 0, 0, 0],
    _screenCoords: [0, 0, 0, 0],

    
    _init: function() {
        var self = this, o = this.options;
        
        // TODO: could float work?
        self.element.css({
                    display: 'block',
                    margin: 0
                });
                
        // TODO: broken in safari
        self.originalSize = o.originalSize || [
            self.element.outerWidth(),
            self.element.height(),
        ];
    
        console.log(self.originalSize);
        self.widget = self.element.wrap($('<div />')
            .css({position: 'relative'}))
            .parent()
            .addClass(self.widgetBaseClass + ' ' +
                    'ui-widget ')
            .attr({tabIndex: -1})
            .css({
                    outline: 0,
                    cursor: o.cursor,
                })
            .keydown(function(e) {
                    // TODO: handle keys to move selection
                    (o.keysEnabled && e.keyCode && 
                     e.keyCode == $.ui.keyCode.ESCAPE && 
                     console.log('esc pressed'));
                });
            
        self.selection = $('<div />')
            .addClass(self.widgetBaseClass + '-selection')
            .css({
                    position: 'absolute',
                    border:'1px dashed #fff',
                    top: 0,
                    left: 0,
                    width: 100,
                    height: 100,
                })
            .hide()
            .appendTo(self.widget)
        
        self._makeDraggable();
        self._makeResizable();
        
        self._mouseInit();
    },
    
    
    _mouseCapture: function(e) {
        var self = this, o = this.options;
        if (self.element.get(0) == e.target) {
            self.deselect();
            return true;
        }
        return false;
    },
    
    
    _mouseStart: function(e) {
        var self = this, o = this.options,
            x = e.pageX - self.element.offset().left,
            y = e.pageY - self.element.offset().top;
            
        self._screenCoords = [x, y, x, y];
                
        self.selection.css({
                    left: x,
                    top: y,
                    width: 0,
                    height: 0,
                })
            .show();
        self._updateCoords();
        self._trigger('select', null, self._ui());
    },
    
    
    _mouseDrag: function(e) {
        var self = this, o = this.options,
            x = e.pageX - self.element.offset().left,
            y = e.pageY - self.element.offset().top;
                    
        self.selection.css({
            width: x - self._screenCoords[0],
            height: y - self._screenCoords[1],
        });
        
        self._screenCoords[2] = x;
        self._screenCoords[3] = y;
        
        self._updateCoords();
        self._trigger('select', null, self._ui());
    },
    
    
    _updateCoords: function() {
        var self = this, o = this.options,
            ratios = [
                self.originalSize[0] / self.element.width(),
                self.originalSize[1] / self.element.height(),
            ];
        $.each(self._screenCoords, function(i) {
            self._coords[i] = Math.round(self._screenCoords[i] * ratios[i % 2]);
        });
    },
    
    
    _updateScreenCoords: function() {
        var self = this, o = this.options,
            ratios = [
                self.originalSize[0] / self.element.width(),
                self.originalSize[1] / self.element.height(),
            ];
        $.each(self._coords, function(i) {
            self._screenCoords[i] = Math.round(self._coords[i] / ratios[i % 2]);
        });
    },
    
    
    _makeDraggable: function() {
        var self = this, o = this.options;
        self.selection.draggable({
            containment: 'parent',
            drag: function(e, ui) {
                self._screenCoords = [
                    ui.position.left,
                    ui.position.top,
                    ui.position.left + self.selection.width(),
                    ui.position.top + self.selection.height(),
                ];
                
                self._updateCoords();
                self._trigger('select', null, self._ui());
            },
            cursor: 'move',
        });
    },
    
    
    _makeResizable: function() {
        var self = this, o = this.options;
        self.selection.resizable({
            containment: 'parent',
            resize: function(e, ui) {
                self._screenCoords = [
                    ui.position.left,
                    ui.position.top,
                    ui.position.left + self.selection.width(),
                    ui.position.top + self.selection.height(),
                ];
                
                self._updateCoords();
                self._trigger('select', null, self._ui());
            },
            handles: 'all',
        });
    },
    
       
    deselect: function() {
        this.selection.hide();
    },
    
    
    select: function(coords) {
        var self = this, o = this.options;
        self._coords = coords;
        self._updateScreenCoords();
        if (!self._isSelected()) {
            self.selection.css({
                left: self._screenCoords[0],
                top: self._screenCoords[1],
                width: self._screenCoords[2] - self._screenCoords[0],
                height: self._screenCoords[3] - self._screenCoords[1],
            });
            self.selection.show();
        } else {
            self.selection.animate({
                left: self._screenCoords[0],
                top: self._screenCoords[1],
                width: self._screenCoords[2] - self._screenCoords[0],
                height: self._screenCoords[3] - self._screenCoords[1],
            })
        }
        self._trigger('select', null, self._ui());
    },
    
    
    _isSelected: function() {
        return !this.selection.is(':hidden');
    },
    
    
    _ui: function() {
        return {
            element: this.element,
            coords: this._coords,
        };
    },
    
}));


$.extend($.hz.crop, {
    version: '0.1',
    eventPrefix: 'crop',
    defaults: {
        cursor: 'crosshair',
        originalSize: false,
        keysEnabled: true,
        cancel: null,
    	distance: 1,
    	delay: 0
    }
});
    

})(jQuery);