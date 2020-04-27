

let is_ajax = false; //USE this to check if page load or ajax update exercise
let current_retry = 1; //used for multiple tries
let user_options; // keep options as global var
let wait_time = 2000; //delay before getting new exercise or try again  

let current_ex_nr = []; // use this to keep nr of each exercise type 
current_ex_nr['add'] = 1;
current_ex_nr['substract'] = 1;
current_ex_nr['multiply'] = 1;
current_ex_nr['divide'] = 1;

$(document).ready(function () {

    // KEYpad
    $(".keypad").click(function () {
        event.preventDefault();
        let val = $(this).attr('data-nr');
        if ($.isNumeric(val)) {
            let new_val = $('#answer').val() + val;
            $('#answer').val(new_val);
            if (!is_ajax) {
                {% if user['exercise'][ex_type]['opt_auto_submit'] %}
                if (is_correct_answer() || ($('#correct_answer').val().length) == (new_val).length) {
                    submit_form();
                }
                {% endif %}
            } else { // ajax reload
                if (user_options['opt_auto_submit']) {
                        if (is_correct_answer() || ($('#correct_answer').val().length) == (new_val).length) {
                            submit_form();
                        }
                    }
            }
        }
        else if (val == 'ok') {
            submit_form();
        }
        else {
            var str = $('#answer').val();
            var res = str.substring(0, str.length - 1);
            $('#answer').val(res);
        }
        $("#answer").focus();
    })

    $('#hint_link').click(function () {
        set_chip('hint_nr');
    })
});
//END document ready

// used for async sleep
function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

// blocks the form - used while sleeping    
function form_lock(lock) {
    $.each($("#ex_form :input[type!='hidden']"), function (index, el) {
        if (!$(el).next().children('span').first().hasClass("grey")) {
            $(el).prop("disabled", lock);
        }
    });
}

function is_correct_answer() {
    return ($('#answer').val() == $('#correct_answer').val());
}

// top menu tabs
$('.mdl-layout__tab-manual-switch').click(function () {
    if (!$(this).hasClass('is-active')) {
            ex_type = $(this).prop('id');
        get_new_exercise(ex_type);
    }
})

// updates snackbar (correct, wrong, keep trying)
function show_snack(correct) {
    var snackbarContainer = document.querySelector('#demo-toast-example');
    if (correct == 'retry') {
        var data = { message: 'Keep Trying', timeout: wait_time };
        snackbarContainer.style.background = '#00bcd4';
    }
    else if (correct) {
        var data = { message: 'Well Done', timeout: wait_time };
        snackbarContainer.style.background = '#00d45a';
    } else {
        var data = { message: 'Whoops, it was ' + $('#correct_answer').val(), timeout: wait_time*2 };
        snackbarContainer.style.background = '#ff5252';
    }
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
}


// updates chips
function set_chip(chip_name) {
    let chip_val;
    if (chip_name == 'ex_curr_nr') {
        ex_type = $('#ex_type').val();
        chip_val = current_ex_nr[ex_type] + 1;
        current_ex_nr[ex_type]++;
    } else {
        chip_val = parseInt($('#' + chip_name).html()) + 1;
    }
    $('#' + chip_name).html(chip_val);
    $('input[name="' + chip_name + '"]').val(chip_val);
}

//radio boxes
$('.mdl-switch__input').click(function () {
    let check = 0;
    let el1 = $(this);
    if (el1.prop('checked'))  {
        check++;
        $('#answer').val((el1).val());
        {% if user['exercise'][ex_type]['opt_auto_submit'] %}
        if (!is_ajax) {
            setTimeout(submit_form, 500);
            return;
        }
        {% endif %}
        if (is_ajax && user_options['opt_auto_submit']) {
            submit_form();
        }
    }
    $.each($('.mdl-switch__input'), function (index, el) {
        var btn = $(this);
        if ((el1.prop('id') !== $(el).prop('id')) && ($(this).prop('checked'))) {
            btn.trigger("click");
            check++;
        }
    })
    if (check == 0) $('#answer').val('');
});

// gets new exercie values, answer, hint, checkbox values, user options for exercise type
function get_new_exercise(ex_type) {
    is_ajax = true;
    $.get("{{ url_for('exercise_bp.get_exercise') }}", { ex_type: ex_type })
        .done(function (data) {
            let response = jQuery.parseJSON(data);
            user_options = response[6];
            current_retry = 1;

            // set nex exercise values and reset hint and retry 
            $('.ex_0').html(response[0]);
            $('.ex_1').html(response[1] + ' = ');
            $('.ex_3').html(response[3]);

            $('#ex_curr_nr').html(current_ex_nr[ex_type]);
            $('#hint_nr').html('0');
            $('#ex_retry').html('1');

            $('#answer').val('');
            $('#correct_answer').val(response[2]);
            $('#ex_type').val(ex_type);
            $('#ex_retry_nr').val(user_options['opt_retry_nr']);

            $('#total_exercise').val(user_options['opt_exercise_nr']);

            $('#hint_content').html('<li class="mdl-list__item hint">Hint</li><li class="mdl-list__item  hint">' + response[4].join('</li><li class="mdl-list__item  hint">'));

            if (user_options['opt_retry_nr'] == 1) {
                $('.retry_nr_div').addClass('hidden_content');
            } else {
                $('#ex_total_retry').html(user_options['opt_retry_nr']);
                $('.retry_nr_div').removeClass('hidden_content');
            }

            if (user_options['opt_exercise_nr'] == 0) {
                $('.exercise_nr_div').addClass('hidden_content');
            } else {
                $('#ex_total_nr').html(user_options['opt_exercise_nr']);
                $('.exercise_nr_div').removeClass('hidden_content');
            }

            if (user_options['opt_auto_submit']) {
                $('.auto_submit_div').addClass('hidden_content');
            } else {
                $('.auto_submit_div').removeClass('hidden_content');
            }

            // show answer if option
            if (user_options['opt_show_answer']) $('.ex_2').attr("placeholder", response[2]);
            else $('.ex_2').attr("placeholder", '');

            // update radio boxes values for multiple answer types (3 or 5)
            if (user_options['opt_answer_type'] > 1) {
                let options = response[5];
                for (let i = 0; i <= (options.length); i++) {
                    $('#checkbox_answer' + i).html(options[i]);
                    the_switch = $('#switchX' + i);
                    the_switch.val(options[i]);
                    if (the_switch.prop('checked')) {
                        the_switch.trigger('click');
                    }
                }

                for (i = 0; i < 5; i++) {
                    if (i >= options.length) {
                        $('label[for="switchX' + i + '"]').addClass('hidden');
                    } else {
                        $('label[for="switchX' + i + '"]').removeClass('hidden');
                    }
                }
                $('span .grey').removeClass('grey');
                $( ":checkbox" ).prop('disabled', false)

                $('#show_keypad').addClass('hidden_content');
                $('#show_check_options').removeClass('hidden_content');
            } else {
                $('#show_check_options').addClass('hidden_content');
                $('#show_keypad').removeClass('hidden_content');
            }
        });
} //end get_new_exercise

//points are saved for user collection, exercise results are saved on exercise collection
function save_points() {
    $.get("{{ url_for('exercise_bp.add_point') }}", { 'user_id': "{{ user['_id'] }}" })
        .done(function (data) {
            // console.log("Response Was: " + data);
        });
}

// submits exercise form, redirect for last exercise
function submit_answer() { 
    let data_object = $("#ex_form").serialize();
        $.post("{{ url_for('exercise_bp.submit_answer') }}", { data_object })
        .done(function (response) {
            if (response.redirect) {
                window.location.href = response.redirect;
            } 
        });             
}

//wrong answer - TODO - maybe update values after waiting time
async function submit_wrong() {
    let ex_type_val = $('#ex_type').val();
    set_chip('ex_curr_nr');
    submit_answer();
    show_snack(false);
    $("#answer").focus();
    form_lock(true);
    await sleep(wait_time);
    form_lock(false);
    get_new_exercise(ex_type_val);
    }

//correct answer - TODO - maybe update values after waiting time    
async function submit_correct() {
    let ex_type_val = $('#ex_type').val();
    set_chip('unicorn_points');
    save_points();
    set_chip('ex_curr_nr');
    submit_answer();
    show_snack(true);
    $("#answer").focus();
    form_lock(true);
    await sleep(wait_time);
    form_lock(false);
    get_new_exercise(ex_type_val);
}

//wrong answer - there are still retries left
async function retry_one(answer_type) {
    set_chip('ex_retry');
    show_snack('retry');
    form_lock(true);
    await sleep(wait_time);
    form_lock(false);
    reset_options(answer_type);
}

//resets checkboxes and answer text field
function reset_options(op_type) {
    if (op_type > 1) {
        $.each($('.mdl-switch__input'), function (index, el) {
            var btn = $(this);
            if ($(this).prop('checked')) {
                btn.trigger("click");
                btn.prop( "disabled", true );
                btn.next().children('span').first().addClass("grey");
            } 
        })
    }
    $('#answer').val('');
}

//evaluates how to submit form - correct or wrong or keep trying
function submit_form() {
    if ($.isNumeric($("#answer").val())) {
        let ex_type_val = $('#ex_type').val();
        if (is_correct_answer()) {
            submit_correct();
        } else { // NOT CORRECT
            if (!is_ajax) {
                {% if user['exercise'][ex_type]['opt_retry_nr'] > 1 %}
                    if (parseInt($('#ex_retry').html()) >= {{ user['exercise'][ex_type]['opt_retry_nr'] }}) {
                submit_wrong();
            } else {
                retry_one({{user['exercise'][ex_type]['opt_answer_type']}});
            }
            {% else %}
            submit_wrong();
            {% endif %}
        } else { // is ajax = true, wrong answer
            if (user_options['opt_retry_nr'] > 1) {
                if (parseInt($('#ex_retry').html()) >= user_options['opt_retry_nr']) {
                    submit_wrong();
                } else {
                    retry_one(user_options['opt_answer_type']);
                }
            } else {
                submit_wrong();
            }
        }
    }
} else {

    //HACK for not triggering keyboard on tablet
    //and to show built-in HTML validator mressage
    //will not work on older browsers    

    $("#answer").prop('required', true);
    $("#answer").prop('readonly', false);
    let form = document.querySelector('form');
    form.reportValidity();

    setTimeout(function () { $("input").prop('readonly', true); }, 1000);
    }
}

// Main button
$('#submit_form').click(function () {
    submit_form();
});

//display message on refresh page ?
// NOT used
// window.onbeforeunload = function () {
    // return "you can not refresh the page";
// }