$(document).ready(function () {
    $('.left_menu_link').toggleClass('mdl-navigation__link--current');
   
    $('.del-user').click(function() {
        $(this).closest("tr")
            .children('td, th')
            .animate({ margin: 0, padding: '12px 0px' })
            .wrapInner('<div />')
            .children()
            .slideUp(function () { $(this).closest('tr').remove();
        });
        for (i = 1; i<=3; i++) {
        $('#remove'+i+$(this).attr('id'))
            .children('td, th')
            .animate({ margin: 0, padding: '12px 0px' })
            .wrapInner('<div />')
            .children()
            .slideUp(function () {  $('#remove'+i+$(this).attr('id'));
        });
        $('#remove'+i+$(this).attr('id')).remove();
    }
       $.post("{{ url_for('admin_bp.delete_user') }}", { user_id: $(this).attr('id') })
        .done(function (data) {
            //  console.log("Delete Response Was: " + data);
        });
    })

})