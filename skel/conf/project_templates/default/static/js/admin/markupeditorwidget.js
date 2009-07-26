$(function() {
    $('textarea.hz-markupedit').each(function() {
        var self = $(this), name = self.attr('name'),
            select = $('select[name=' + name + '_markup]');
            
            select.closest('.form-row').hide();
    
        self.markupeditor({
            split: true, 
            select: function(e, ui) {
                    select.children('[value=' + ui.markup.id + ']')
                        .attr({selected: true});
                },
            initial: select.val(),
        });
    });
});