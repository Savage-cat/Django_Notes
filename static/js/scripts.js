// Обработка клика по ссылке избранное
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

// Обработка клика по по ссылке убрать из избранного
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

$('#feedbackForm').on('submit', function (e) {
    e.preventDefault();
    let baseUrl = 'http://localhost:8000/';

    $.ajax({
        type: 'POST',
        url: baseUrl + $(this).attr('action'),
        data: {
            name: $('#id_name').val(),
            text: $('#id_text').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            $('.main-content').text('Обратная свзяь отправлена!')
        },
        error: function(response){
            const errors = response.responseJSON.errors
            let err = ''
            for (let field in errors) {
                for (let error of errors[field]) {
                        err += '<p>' + error + '</p>'
                }
            }
            $('.formErrors').html(err)

        }
    })
})