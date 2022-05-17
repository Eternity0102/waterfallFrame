$(function(){
	$("#frmLogin").submit(function(){
		var uphone = $("[name=uphone]").val();
		var upwd = $('[name=upwd]').val();
		if (uphone && upwd==''){
			return false;
		}
		return true;
	})
})