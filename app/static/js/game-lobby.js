$(document).ready(function() {

    var socket = io.connect(
        'http://' + document.domain + ':' + location.port + '/'
    );
    
    socket.on('kicked', function(data) {
        window.location.href = '/getKicked/' + data;
    });

    socket.on('made host', function(data) {
        window.location.href = '/becomeHost/' + data;
    });

    socket.on('player joined', function() {
        window.location.reload();
    });

});
