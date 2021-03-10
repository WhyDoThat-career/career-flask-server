    $(document).ready(function(){
		$('#email').keyup( function(e){
            var email = $('#email').val();

            if(email != ''){
      
               $.ajax({
                  url: '/checkemail',
                  type: 'post',
                  data: {email: email},
                  success: function(response){
                        if (response == "No User"){
                      $('#uname_response').html('가입 가능!').css({'color':'blue', 'text-align':'right'});
                      $('#button').removeAttr('disabled');
                        }else if (response == 'Not@'){
                           $('#uname_response').html('잘못된 형식의 이메일 주소 입니다.').css({'color':'red', 'text-align':'right'});
                        }
                        else{
                            $('#uname_response').html('중복된 이메일이 존재 합니다.').css({'color':'red', 'text-align':'right'});
                        }
                   }
               });
            }else{
               $("#uname_response").html("");
            }
		})
	})