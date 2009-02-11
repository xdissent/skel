/*
 * Markup Editor
 *
 * Depends:
 *  ui.core.js
 *	ui.tabs.js
 */
(function($) {

$.widget('ui.markupeditor', {
    
    _init: function() {
        this._setup_editor(true);
    },
    
    add_markup: function(markup) {
        var self = this, o = this.options;
        
        var anchor = '#ui-markupeditor-markup-' + markup.id;
        self.$edit_pane.tabs('add', anchor, markup.label);
        
        var $tab = self.$edit_pane.find('a[href$=' + anchor + ']');        
        var $toolbar = self.$edit_pane.find(anchor);
        
        $tab.data('markup', markup);
        
        $(markup.buttons).each(function() {
            var button = '<button class="ui-state-default ui-corner-all" type="button">' +
                '<span class="ui-icon ui-icon-' + this + '">' + this + '</span></button>';
            $(button).click(function() {
                //console.log(this);
                // TODO: define button actions in toolbars
            }).appendTo($toolbar);
        });
    },
    
    set_markup: function(markup) {
        console.log(markup);
        var self = this, o = this.options;
        
        var old_markup = self.current_markup || {};
        $(o.markups).each(function() {
            if (this.id == markup) {
                self.current_markup = this;
            }
        });
        if (old_markup != self.current_markup) {
            
            self.$markup_field.children('[value=' + markup + ']').attr({selected: true});
            
            //self.$edit_pane.tabs('select', '#ui-markupeditor-markup-' + markup);
        }

    },
    
    _setup_editor: function(init) {
        var self = this, o = this.options;
        
        if (init) {
            var $editor = $('<div class="ui-markupeditor ui-widget ui-helper-clearfix"></div>');
            var $edit_pane = $('<div class="ui-markupeditor-edit"><ul></ul></div>');
            var $preview_pane = $('<div class="ui-markupeditor-preview"><ul></ul></div>');
            
            self.$markup_field = $([]);
            
            self._fix_django();
        
            self.element.wrap($editor);
            
            self.$editor = $editor = self.element.parent();
            self.$edit_pane = $edit_pane;
            self.$preview_pane = $preview_pane;
            
            $editor.append($edit_pane).append($preview_pane);
                        
            /*/ Create Edit pane's tabs with 'set_markup' select event.
            *|  Event Reloads Preview pane.
            */
            $edit_pane.tabs({
                select: function(e, ui) {
                    self.set_markup($(ui.tab).data('markup').id);
                    self._load_preview();
                }
            });
            
            
            /*/ Add all markups from options
            */
            $(o.markups).each(function() {
                self.add_markup(this);
            });
                        
            
            /*/ Hijack textarea
            */
            this.element.remove();
            $edit_pane.append(this.element);
            // TODO: review these styles
            this.element.wrap('<div class="ui-markupeditor-edit-container ' +
                    'ui-helper-clearfix ui-tabs-panel ui-widget-content ' +
                    'ui-corner-bottom"></div>');
                    
                    
            /*/ Create Preview pane tabs with '_load_preview' on click.
            */
            $preview_pane.tabs({ 
                add: function(e, ui) {
                    $(ui.tab).click(function() {
                        self._load_preview();
                        return false;
                    });
                }
            });
            
            
            /*/ Populate Preview pane tabs. Automatically creates the panels.
            */
            $preview_pane.tabs('add', '#ui-markupeditor-markup-preview', 'Preview');
            $preview_pane.tabs('add', '#ui-markupeditor-markup-source', 'Source');
            
            
            /*/ Find the panels by anchor. Should change this to class immediately.
            */
            self.$preview = $editor.find('#ui-markupeditor-markup-preview');
            self.$source = $editor.find('#ui-markupeditor-markup-source').append($('<pre><code></code></pre>'));
            
            
            /*/ Install keyboard events that trigger preview request.
            */
            this.element.keyup(function() {
                self._request_preview();
            });
            
            
            /*/ Initiate values from form.
            */
            var markup = self.$markup_field.children(':selected').val();
            if (markup == '' || markup == undefined) {
                self.$edit_pane.tabs('select', '#ui-markupeditor-markup-markdown');
                self.set_markup('markdown');
//                $.data(ui.tab, 'load.tabs');
                
//                self.set_markup(self.$edit_pane.tabs().data('selected.tabs').data('markup').id);
            } else {
                // HACK!
                if (markup == 'markdown') {
                    self.set_markup('markdown');
                }
                self.$edit_pane.tabs('select', '#ui-markupeditor-markup-' + markup);
            }
            //self.$markup_field.children(':selected').val();            
           
            self._load_preview();
            self._init_resize();
        
            //self.resize();
            self.typing = false;
            self.updating = false;
            
        }
    },
    
    _init_resize: function() {
        var self = this, o = this.options;
        
        // TODO: clean this up accounting for margins/padding
        // determine editor's half-width
        // set width of panes to 50%
        // get width of edit_pane when preview_pane is o.minPaneWidth wide
        var halfWidth = (self.$editor.width() / 2) - 20;
        var maxWidth = halfWidth + o.minPaneWidth;
        
        self.$edit_pane.width(halfWidth);
        self.$preview_pane.width(halfWidth);
        
        var $container = self.$editor.find('.ui-markupeditor-edit-container').addClass('ui-helper-clearfix');
        
        self.$edit_pane.resizable({
            minWidth: o.minPaneWidth,
            maxWidth: maxWidth,
            resize: function(e, ui) {
                self.$preview_pane.height(self.$edit_pane.height()).width((halfWidth * 2) - ui.element.width());
                
                $container.height(self.$edit_pane.height() - $container.position().top - 20);
                
                //self.$preview.height(self.$edit_pane.height() - 40);
            }
        });
    },
    
    resize: function() {
        var height = this.element.css('height');
        this.$preview.css({ height: height });
    },
    
    _load_preview: function() {
        var self = this;
        
        $.post(self.current_markup.url, {
                content: self.element.val()
            }, function(data) {
                self.$preview.html(data);
                $('code', self.$source).text(data);
        });
    },
    
    _request_preview: function() {
        var self = this, o = this.options;
        
        if (self.typing) {
            clearTimeout(self.typing);
        } else {
            self.updating = setInterval(function() {
                self._load_preview();
            }, o.updateInterval);
        }
        
        self.typing = setTimeout(function() {
            clearTimeout(self.updating);
            self._load_preview();
            self.updating = false;
            self.typing = false;
        }, o.typingTimeout);

    },
    
    _fix_django: function() {
        
        this.$markup_field = $('#' + this.element.attr('id') + '_markup');
        this.$markup_field.closest('.form-row').hide();
    }
    
});

$.extend($.ui.markupeditor, {
    getter: '',
    version: '0.1',
    eventPrefix: 'markup',
    defaults: {
        minPaneWidth: 300,
        typingTimeout: 1500,
        updateInterval: 1000,
        markups: [
            {
                id:     'markdown',
                label:  'Markdown',
                url:    '/markupeditor/preview/markdown/',
                buttons:[
                    'scissors',
                    'copy',
                    'bold',
                    'italic',
                    'image',
                    'link',
                ],
            },
            
            {
                id:     'rest',
                label:  'restructuredText',
                url:    '/markupeditor/preview/rest/',
                buttons:[
                    'italic',
                    'image',
                    'link',
                ],
            },
            
            {
                id:     'xhtml',
                label:  'XHTML',
                url:    '/markupeditor/preview/xhtml/',
                buttons:[
                    'cut',
                    'copy',
                    'bold',
                    'italic',
                    'image',
                    'link',
                ],
            },
        ],
    }
});

$(function() {
    $('textarea').markupeditor();    
});

})(jQuery);