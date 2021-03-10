function loginSuccess() {
  toastr.success("Redirecting you to the dashboard")
  window.location.href = "/"
}

$("#login").submit(function () {
  $("#button").prop("disabled", true)
  $("#img").show()
  event.preventDefault()
  $.ajax({
    url: "/checkloginpassword",
    data: $(this).serialize(),
    type: "POST",
    success: function (response) {
      $("#img").hide()
      if (response === "correct") {
        setTimeout(loginSuccess, 5000)
        swal
          .fire({
            icon: "success",
            title: "로그인 성공",
          })
          .then((result) => {
            window.location.href = "/"
          })
      } else if (response === "wrong") {
        swal
          .fire({
            icon: "error",
            title: "로그인 실패",
            text: "이메일이 틀렸거나, 비밀번호가 틀립니다.",
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
