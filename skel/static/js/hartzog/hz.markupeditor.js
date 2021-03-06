/*
 * Markup Editor
 *
 * Depends:
 *  ui.core.js
 *	ui.tabs.js
 *  hz.core.js
 *  hz.splitpane.js
 */
(function($) {

$.widget('hz.markupeditor', {
    
    _init: function() {
        var self = this, o = this.options;
                
        self.idPrefix = self.element.attr('id');
        
        self.widget = self.element.wrap('<div />').parent()
            .addClass(self.widgetBaseClass + ' ' + 'ui-widget');
            
    
        // Setup edit pane
        
        self.editPane = $('<div><ul /></div>')
            .addClass(self.widgetBaseClass + '-edit-pane')
            .appendTo(self.widget)
            .tabs();
        
        $(o.markups).each(function() {
            var markup = this, id = '#' + self.idPrefix + '-' + this.id;
            
            self.editPane.tabs('add', id, this.label)
                .find('a[href=' + id + ']')
                .click(function() {
                        self.markup(markup);
                        return false;
                    });
                        
            var toolbar = self.editPane.find(id).addClass('hz-markupeditor-toolbar ui-helper-clearfix');
            $(this.buttons).each(function() {
                var cmd = this;
                $('<a href="#" class="ui-corner-all"><span class="ui-icon ui-icon-' + cmd + '">' + cmd + '</span></a>')
                    .css({float: 'left'})
                    .click(function() {
                            markup.run(cmd);
                        })
                    .appendTo(toolbar);
            });
            
        });
        
        self.editPane.append(this.element);
        this.element.css({width: '100%', height: '100%', resize: 'none' })
            .wrap('<div class="ui-tabs-panel ui-widget-content ui-corner-bottom" style="padding-top: 0px" />');
        

        // Setup preview pane
        
        self.previewPane = $('<div><ul /></div>')
            .addClass(self.widgetBaseClass + '-preview-pane')
            .appendTo(self.widget)
            .tabs({
                    select: function() {
                        self.preview();
                    }
                });
            
        // TODO: double check var declarations. This one had semicolon on 1st line.
        $(['Preview', 'Source']).each(function() {
            var label = this, name = this.toLowerCase(),
                anchor = '#' + self.idPrefix + '-' + name;
            self.previewPane.tabs('add', anchor, label);
            self[name + 'Tab'] = self.previewPane.find(anchor);
            // Add wrapper to contain scrollers for large content
            $('<div />').css({overflow: 'auto', height: '100%'})
                .appendTo(self[name + 'Tab']);
        });
        self.sourceTab.children().append('<pre><code></code></pre>');
        
        
        if (o.split) {
            // TODO: Move this into hz.splitpane.js
            // Create splitpane with trickery to get tabs to scale automatically
            self.widget.splitpane({
                resize: function(e, ui) {
                    ui.element.find('.hz-splitpane-pane > .ui-tabs')
                        .add('.hz-splitpane-pane > .ui-tabs > .ui-tabs-panel')
                        .not('.hz-markupeditor-toolbar')
                        .each(function() {
                            var $this = $(this);
                            var height = $this.parent().height() - $this.position().top;
                            var padding = $(this).outerHeight() - $(this).height();
                            $(this).height(height - padding);            
                        });
                }
            
            });
        } else {
            self.editPane.add(self.previewPane).resizable({


                minWidth: self.widget.width(),
                maxWidth: self.widget.width(),
                // TODO: Move this into hz.splitpane.js
                resize: function(e, ui) {
                    ui.element.find('.ui-tabs')
                        .add('.ui-tabs > .ui-tabs-panel')
                        .not('.hz-markupeditor-toolbar')
                        .each(function() {
                            var $this = $(this);
                            var height = $this.parent().height() - $this.position().top;
                            var padding = $(this).outerHeight() - $(this).height();
                            $(this).height(height - padding);            
                        });
                }
            }).css({position: 'relative'});
        }
        
        this.element.keyup(function() {
            self.preview();
        });
        
        if (o.initial) {
            self.markup(self._markupFromId(o.initial));
        } else {
            self.markup(o.markups[0]);
        }

    },
    
    
    _markupFromId: function(id) {
        var markup = {};
        $(this.options.markups).each(function() {
            if (this.id == id) markup = this;
        });
        return markup;
    },
    

    preview: function() {
        var self = this, o = this.options;
        if (self.typing) {
            clearTimeout(self.typing);
        } else {
            self.updating = setInterval(function() {
                self._loadPreview();
            }, o.updateInterval);
        }
        
        self.typing = setTimeout(function() {
            clearTimeout(self.updating);
            self._loadPreview();
            self.updating = false;
            self.typing = false;
        }, o.typingTimeout);
    },
        
        
    _loadPreview: function() {
        var self = this;
                                
        if (!self.currentMarkup) {
            self.previewTab.children().html(self.element.val());
            self.sourceTab.find('code').text(self.element.val());
            return;
        }
                
        $.post(self.currentMarkup.url, {
                content: self.element.val()
            }, function(data) {
                self.previewTab.children().html(data);
                self.sourceTab.find('code').text(data);
        });
    },
    
    
    markup: function(markup) {
        // externally exposed setter to change markup by passing an id
        // internally exposed setter to change by markup instance
        // if markup is string, markup = _lookupmarkup(markup)
        this.currentMarkup = markup;
        this.editPane.tabs('select', '#' + this.idPrefix + '-' + markup.id);
        this.preview();
        this._trigger('select', null, this._ui());
    },
    
    
    _ui: function() {
        return {
            element: this.element,
            markup: this.currentMarkup,
        };
    },
    
});

$.extend($.hz.markupeditor, {
    version: '0.1',
    eventPrefix: 'markup',
    defaults: {
        split: true,
        initial: false,
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
                run: function(command) {
                    console.log(this.label + ': ' + command);
                },
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
                run: function(command) {
                    console.log(this.label + ': ' + command);
                },
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
                run: function(command) {
                    console.log(this.label + ': ' + command);
                },
            },
        ],
    }
});

})(jQuery);