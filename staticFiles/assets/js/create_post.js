$(document).ready(function () {
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  
    const csrftoken = getCookie('csrftoken');
  
    $('#create-post-form').on('submit', function (e) {
      e.preventDefault();
  
      let formData = new FormData(this);
  
      $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          $('#success-message')
            .text('✅ ' + response.message)
            .css('color', 'green');
          $('#create-post-form')[0].reset();
        },
        error: function (xhr) {
          const errorText = xhr.responseJSON?.errors 
            ? Object.values(xhr.responseJSON.errors).join(', ')
            : '❌ Failed to create post.';
          $('#success-message')
            .text(errorText)
            .css('color', 'red');
        }
      });
    });
  });
  