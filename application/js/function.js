$("#review_form").submit(function(e){
    e.preventDefault();
    console.log('submit')
    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),
        
        dataType: "json",

        success: function(response){
            console.log("review saved");
            if(response.bool == true){
                $("#reviewres").html("Review added")
                $(".review_form").hide()
                $(".remove-add").hide()
                
               
            }
        }

    })
})
