$(function(){

	var name_error = false;
	var pwd_error = false;
	if(error_name==1){
	    $('.user_error').html('用户名错误').show();
	}

	if(error_pwd==1){
	    $('.pwd_error').html('密码错误').show();
	}

	$('.name_input').blur(function(){
	    len = $('.name_input').val().length;
	    if(len==0){
	        $('.user_error').html('请填写用户名').show();
	        name_error = false;
	    }else{
	        $('.user_error').hide();
	        name_error = true;
	    }
	})

	$('.pass_input').blur(function(){
	    len = $('.pass_input').val().length;
	    if(len==0){
	        $('.pwd_error').html('请填写密码').show();
	        pwd_error = false;
	    }else{
	        $('.pwd_error').hide();
	        pwd_error = true;
	    }
	})

	$('form').submit(function(){

	})
})