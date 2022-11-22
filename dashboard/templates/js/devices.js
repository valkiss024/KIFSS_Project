$('.checkbox').click(function() {

    if ($(this).hasClass("check-off")) {

        $(this).removeClass('check-off');
        $(this).addClass('check-on');

    } else if ($(this).hasClass("check-on")) {

        $(this).removeClass('check-on');
        $(this).addClass('check-off');
        
    }
});