
function updateStars(elem) {
    elem.addClass('fas');
    elem.removeClass('far');
    elem.prevAll().addClass('fas');
    elem.prevAll().removeClass('far');
    elem.nextAll().addClass('far');
    elem.nextAll().removeClass('fas');
}

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

    // when you hover over individual stars, update star display
    $('.star-rating').hover(function() {
        updateStars($(this))


    });

     $('.star-rating').click(function(){
         this.form.submit();
     })

     // when you leave the star rating div, restore to selected star
     $('.star-ratings').mouseleave(function() {
         var selectedStar = $('input[name=stars]:checked', this);
         console.log(selectedStar);
         updateStars(selectedStar);

     });




});











