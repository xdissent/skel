(function($) {

module('crop: events');

test('select', function() {
	ok(false, 'missing test - untested code is broken code.');
});

test('load', function() {
	ok(false, 'missing test - untested code is broken code.');
});

test('show', function() {
	expect(3);

	var uiObj;
	el = $('#tabs1').tabs({
		show: function(event, ui) {
			uiObj = ui;
		}
	});
	equals(uiObj.tab, $('#tabs1 a')[0], 'should have tab as DOM anchor element');
	equals(uiObj.panel, $('#tabs1 div')[0], 'should have panel as DOM div element');
	equals(uiObj.index, 0, ' should have index');
	
});

test('add', function() {
	ok(false, 'missing test - untested code is broken code.');
});

test('remove', function() {
	ok(false, 'missing test - untested code is broken code.');
});

test('enable', function() {
	ok(false, 'missing test - untested code is broken code.');
});

test('disable', function() {
	ok(false, 'missing test - untested code is broken code.');
});

})(jQuery);