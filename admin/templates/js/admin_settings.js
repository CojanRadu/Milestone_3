$(document).ready(function () {
   
    ex = ['add', 'substract', 'multiply', 'divide'];
    'use strict';
        window['counter'] = 0;
        var snackbarContainer = document.querySelector('#demo-toast-example');
        ex.forEach(function(item) {
        const slider = document.querySelector('#'+item+'-slider-tool');
        slider.addEventListener("input", function () {
        document.getElementById(item+"-tooltip").textContent = slider.value;
        document.getElementById(item+"-badge1").setAttribute('data-badge', slider.value);
         }, false);
      
        var showToastButton = document.querySelector('#'+item+'-update-btn');
        showToastButton.addEventListener('click', function (event) {
            'use strict';
            var data = { message: 'Update Settings {{ user.name }} - '+ item +' (' + ++counter + ')' };
            snackbarContainer.MaterialSnackbar.showSnackbar(data);

            var str = $("#"+item+"-update-form").serialize();
            event.preventDefault();
            $.post("{{ url_for('admin_bp.update_settings') }}", { str })
                .done(function (data) {
                    // console.log("Response Was: " + data);
                });
        });
    });
})