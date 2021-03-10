function loginSuccess() {
  toastr.success("Redirecting you to the dashboard")
  window.location.href = "/login"
}

$("#forgot-password").submit(function () {
  $("#button").prop("disabled", true)
  $("#img").show()
  event.preventDefault()
  $.ajax({
    url: "/checkemail",
    data: $(this).serialize(),
    type: "POST",
    success: function (response) {
      $("#img").hide()
      if (response === "Exist") {
        setTimeout(loginSuccess, 5000)
        swal
          .fire({
            icon: "success",
            title: "메일 전송 성공",
          })
          .then((result) => {
            window.location.href = "/login"
          })
      } else if (response === "No User" || "Not@"){
        swal
          .fire({
            icon: "error",
            title: "메일 전송 실패",
            text: "가입되지 않은 이메일이거나 잘못된 형식 입니다.",
          })
          .then((result) => {
            $("#button").removeAttr("disabled")
          })
      }
    },
    error: function (error) {
      console.log(error)
    },
  })
})
