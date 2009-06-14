var $ = function(callback) {

    var callbacks = [callback];

    $ = function(callback) {
        callbacks.push(callback);
    }

    google.setOnLoadCallback(function() {
        $(callbacks).each(function() { $(this); });
    });

    google.load('jquery', '1.3.2', {uncompressed:true});
    google.load('jqueryui', '1.7.2', {uncompressed:true});
}