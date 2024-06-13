// get value of country field and store it in a variable
let countrySelected = $('#id_default_country').val();
if (!countrySelected) {
    // if country selected is false, set to placeholder colour 
    $('#id_default_country').css('color', '#aab7c4');
}
// every time the box changes, get the value of it
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if (!countrySelected) {
        // set the colour
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
})