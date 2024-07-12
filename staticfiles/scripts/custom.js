$(document).ready(function(){
    // add to selection function
    $('.add-to-selection').on("click", function(){
        let button = $(this)
        let id = button.attr("data-index")
        let hotel_id = $("#id").val()
        let room_id = $(`.room_id_${id}`).val()
        let room_number  = $(`.room_number_${id}`).val()
        let room_type =  $("#room_type").val()
        let hotel_name = $("#hotel_name").val()
        let room_name = $("#room_name").val()
        let room_price = $("#room_price").val()
        let number_of_beds = $("#number_of_beds").val()
        let checkin = $("#checkin").val()
        let checkout = $("#checkout").val()
        let adult = $("#adult").val()
        let children = $("#children").val()

        // Debugging: Log the collected data
        console.log("Check-in date:", checkin)
        console.log("Check-out date:", checkout)

        // Send data via ajax
        $.ajax({
            url: '/booking/add_to_selection/',
            data: {
                "id":id,
                "hotel_id": hotel_id,
                "room_id": room_id,
                "room_number":room_number,
                "hotel_name":hotel_name,
                "room_name":room_name,
                "room_type":room_type,
                "room_price":room_price,
                "number_of_beds":number_of_beds,    
                "checkin":checkin,
                "checkout":checkout,
                "adult":adult,
                "children":children,
                
            },
            dataType: "json",
            beforeSend: function() {
                console.log("Sending data to server");
                button.html("<i class='fas fa-spinner fa-spin' </i> Processing")
            },
            success: function(response){
                console.log(response)
                $(".room-count").text(response.total_selected_items)
                button.html("<button class='button border' <i class='sl sl-icon-basket'></i>Selected </button>")
            }
        })
    })
})

// Delete items
$(document).on("click", ".delete-item", function(){
    console.log("Hello world")
    let id = $(this).attr("data-item")
    let button = $(this)

    $.ajax({
        url: "/booking/delete_selection/",
        data: {
            "id":id
        },
        dataType: "json",
        beforeSend: function() {
            button.html("<i class='fas fa-spinner fa-spin' </i> ")
        },
        success: function(res){
            $(".selection-list").html(res.data)
        }
    })

})


// Update room status
function makeAjaxCall(){
    $.ajax({
        url: "/update_room_status/",
        type: "GET",
        success: function(data) {
            console.log("AJAX call successful.");
        },
    });
}

setInterval(makeAjaxCall, 3600000); // Call the function every one hour (3600000 milliseconds = 1 hour) or 60000 milli