$(document).ready(function(){
    $('img').attr('draggable', false);
    $("#print").click(function(){
        $('#print').hide();
        $('.user-info').hide();
        $('.student-name').html(`${$('#name').val()}`);
        $('#course-name').html(`${$("#course option:selected").html()}`);
        var names = $('#name').val().split(' ');
        console.log(names);
        $('#id-name').html(`${names[0]}`);
        window.print();
        $("#print").show();
        $('.user-info').show();
    });
    document.onkeydown = function(e) {
        if (e.ctrlKey && 
            (e.keyCode === 67 || 
             e.keyCode === 86 || 
             e.keyCode === 85 || 
             e.keyCode === 117)) {
            return false;
        } else {
            return true;
        }
};
    $(document).keypress("u",function(e) {
        if(e.ctrlKey) {
            return false;
        }
        else {
            return true;
        }
    });
});