$(document).ready(function() {
    $('.tr-link').click(function() {
        window.location.href = $(this).data('href');
    });
});
