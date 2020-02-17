$("#push_button").click(function(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/push",
        success: function(result) {
            alert(result);
        }
    });
});
