$(document).ready(function(){
    $('#confirmpassword').keyup( function(e){
        var password = $('#password').val();
        var confirmpassword = $('#confirmpassword').val();
        console.log(password, confirmpassword)

        if(password != confirmpassword){
  
           $('#pass_response').html("입력한 비밀번호와 비밀번호 확인이 맞지 않습니다.").css({'color':'red', 'text-align':'right'});
           $('#button').prop('disabled', true);
        }else{
           $("#pass_response").html("");
           $('#button').removeAttr('disabled');
        }
    })
})