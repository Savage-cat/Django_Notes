// Обработка клика по кнопке лайка
$('#FavoriteButton').click(function(e) {
    e.preventDefault();
    let baseUrl = 'http://localhost:8000/';

    $.ajax({
        type: 'GET',
        url: baseUrl + $(this).attr('href'),
        success: function(response) {

            $('#FavoriteButton').hide()
            $('#UnfavoriteButton').show()
        }

    })
})

// Обработка клика по кнопке снятия лайка
$('#UnfavoriteButton').click(function(e) {
    e.preventDefault();
    let baseUrl = 'http://localhost:8000/';

    $.ajax({
        type: 'GET',
        url: baseUrl + $(this).attr('href'),
        success: function(response) {

            $('#FavoriteButton').show()
            $('#UnfavoriteButton').hide()
        }
    })
})