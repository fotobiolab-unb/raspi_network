$("#push_button").click(function(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/push",
        success: function(result) {
            alert(result);
            location.reload();
        }
    });
});

$("#new_batch").click(function(e){
  e.preventDefault();
  let data =eval($("#text_matrix")[0].value);
  $.ajax({
    type: "POST",
    url: "/assignments",
    data: JSON.stringify({"matrix": data}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(msg){
      console.log("ok")
      location.reload();
    }
  })
})
