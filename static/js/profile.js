$(document).ready(function() {



    $('.vote-button').hover(function() {

        var newText = $(this).text().replace(/(\d+)/, function(x) {return parseInt(x)+1})
        $(this).text(newText)
    }, function() {
        var newText = $(this).text().replace(/(\d+)/, function(x) {return parseInt(x)-1})
        $(this).text(newText)
    });

    $('#pro-tag-input').keypress(function(e) {
        if (e.which == 13) {
            this.form.submit()
        }
    });

     $('#con-tag-input').keypress(function(e) {
        if (e.which == 13) {
            this.form.submit()
        }
    })




});











