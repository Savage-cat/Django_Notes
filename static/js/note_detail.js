

function loadComments(){
    let baseUrl = 'http://127.0.0.1:8000/';
    let noteId = $('.container-post').data('note-id')

    $.ajax({
        type: 'GET',
        url: baseUrl + `/api/notes/${noteId}/comments`,
        success: function(response) {
            let comments = ''
            $.each(response.comments, function(index, comment) {
                comments += '<div class="comment">'
                comments += '<p class="comment-author">' + comment.profile +  '</p>'
                comments += '<p class="comment-text">' + comment.text + '</p>'
                comments += '</div>'
            })

            $('.comments-section').html(comments);
        }
    })
}

// Обработка клика по кнопке отправить комментарий
$('#CommentForm').on('submit', function (e) {
    e.preventDefault();
    let baseUrl = 'http://127.0.0.1:8000/';

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: {
            text: $('#id_text').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            loadComments()
            $('#CommentForm')[0].reset()
            $('.formErrors').html('')
        },
        error: function(response){
            const errors = response.responseJSON
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

//$(document).ready(function (){
//    loadComments();
//})