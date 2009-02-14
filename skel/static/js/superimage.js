
(function($) {

$.widget('ui.superimage', {

    _new_thumb_counter: 0,
    
    _current_thumb: false,
    
    
    _init: function() {
        this._setup_image(true);
    },
    
    
    _edit_thumb: function(thumb_container) {
        var $tc = $(thumb_container);
        $tc.find('.ui-superimage-thumbnail-coords').show();
        $tc.find('input[disabled]').removeAttr('disabled');
    },
    

    _add_row: function() {
        var self = this;
        
        $new = self.$widget.find('.ui-superimage-thumbnail-template').clone();
        $new.find('.ui-superimage-thumbnail-coords').show().find('input').attr({enabled: true});
        $new.removeClass('ui-superimage-thumbnail-template').remove();
        $new.find('[id$=_template]').each(function() {
            var $this = $(this);
            var new_id = $this.attr('id').replace('_template', '_new' + self._new_thumb_counter);
            $this.attr({id: new_id});
        });
        $new.find('[name$=_template]').each(function() {
            var $this = $(this);
            var new_name = $this.attr('name').replace('_template', '_new' + self._new_thumb_counter);
            $this.attr({name: new_name});
        });
        $new.find('[for$=_template]').each(function() {
            var $this = $(this);
            var new_for = $this.attr('for').replace('_template', '_new' + self._new_thumb_counter);
            $this.attr('for', new_for});
        });
        
        $new.find('.ui-superimage-thumbnail-edit-delete .delete').toggle(function() {
            $(this).text('Undelete');
            return false;
        }, function() {
            $(this).text('Delete');
            return false;
        });
        
        $new.find('.ui-superimage-thumbnail-edit-delete .edit').toggle(function() {
            $(this).text('Done Editing');
            self._current_thumb = $(this).closest('.ui-superimage-thumbnail-container');
            return false;
        }, function() {
            // deactivate fields etc
            $(this).text('Edit');
            self._current_thumb = false;
            return false;
        });
        
        self.$widget.find('.ui-superimage-thumbnails > div:first-child').append($new);
        
        self._new_thumb_counter++;
    },

    
    _setup_image: function(init) {
        var self = this, o = this.options;
        
        self.$widget = self.element.closest('.ui-superimage-widget');
        self.$source = self.$widget.find('.ui-superimage-source');
        self.$source.tabs();
                
        self.element.Jcrop({
            onChange: function(c) {
                self._update_coords(c);
            },
            onSelect: function(c) {
                self._update_coords(c);
            },
        });
        
        self._fix_django();
        
        self.$widget.find('.ui-superimage-thumbnail-add').click(function() {
            try {
                        self._add_row();

            } catch(e) {
                console.log(e.description);
            }
            return false;
        });
        
        self.$widget.find('.ui-superimage-thumbnail-edit-delete .delete').toggle(function() {
            $(this).text('Undelete');
            $(this).next('input').removeAttr('disabled');
            return false;
        }, function() {
            $(this).text('Delete');
            $(this).next('input').attr({disabled: 'disabled'});
            return false;
        });
        
        self.$widget.find('.ui-superimage-thumbnail-edit-delete .edit').toggle(function() {
            $(this).text('Done Editing')
            self._current_thumb = $(this).closest('.ui-superimage-thumbnail-container');
            return false;
        }, function() {
            $(this).text('Edit');
            self._current_thumb = false;
            return false;
        });
    },
    

    _fix_django: function() {
        this.$widget.prev('label').hide();
    },
    
    
    _update_coords: function(c) {
        var self = this;
        
        if (self._current_thumb) {
            $coords = self._current_thumb.find('.ui-superimage-thumbnail-coords');

            $.each({
                x1: c.x,
                y1: c.y,
                x2: c.x2,
                y2: c.y2,
                 w: c.w,
                 h: c.h,
            }, function (name, val) {
                $(self._current_thumb.find('[name*=crop_' + name + ']').val(val))
            });
        }
    }
    
});

$(function() {
    $('.ui-superimage').superimage();
});

})(jQuery);