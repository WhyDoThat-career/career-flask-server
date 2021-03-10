$(document).ready(function(){
    $('#email').change( function(e){
        var email = $('#email').val();
        if(email != ''){
  
           $.ajax({
              url: '/checkemail',
              type: 'post',
              data: {email: email},
              success: function(response){
                    if (response == "No User"){
                        $('#uname_response').html("없는 이메일 입니다.").css({'color':'red', 'text-align':'right'});
                        $('#button').prop('disabled', true);
                    }
                    else if (response == "Not@"){
                        $('#uname_response').html("잘못된 형식 입니다.").css({'color':'red', 'text-align':'right'});
                        $('#button').prop('disabled', true);
                    }
                    else{
                        $('#uname_response').html("");
                        $('#button').removeAttr('disabled');
                    }
               }
           });
        }else{
           $("#uname_response").html("");
        }
    })
})