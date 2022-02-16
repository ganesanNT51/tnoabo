$( document ).ready(function() {
    country_id = $("#country").val()
    select_states() 
    
})

//------------------------- All Button on click function goes here ------------------------------------------------------------------//

// on click function to update user profile //

$(document).on("click","#save",function(){
    post_edit_profile_info()
    $("#alert-success").hide()
    $("#alert-danger").hide()
    
})

//------------------------- End all Button on click function goes here ------------------------------------------------------------------//

//------------------------- Change function for country and states goes here ------------------------------------------------------------------//

$(document).on("change", "#country",function(){
    country_id = $("#country").val()
    select_states() 
})

//------------------------- End all change function  ----------------------------------------------------------------------------------//

//------------------------- Function to select state dropdown based on country selected ------------------------------------------------------------------//

function select_states()
{

    $.ajax({
        type: 'GET', // <-- get method of form
        url: "http://127.0.0.1:5000/states_dropdown/"+country_id, // <-- get action of form
        // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',
        async : true,
   
        success: function(data){
            if(data.status == 1)
            {
                $('#state')
                    .find('option')
                    .remove()
                    .end()
                    .append(data.html)
                    ;
                $("#state").val(state_id)    
            }
        },

        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            //location.reload();  
        }  
    })
}

//------------------------- End of select state drop down function ------------------------------------------------------------------//

//------------------------- All Post function goes here ----------------------------------------------------------------------------//

// function to update profile info //

function post_edit_profile_info()
{

    validate_edit_user_profile()

    if($("#edit_profile_info").valid())
    {
    
        $.ajax({
            type: 'POST', // <-- get method of form
            url: $("#edit_profile_info").attr('action'), // <-- get action of form
            data: $("#edit_profile_info").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
            dataType: 'json',

            success: function(data){
                if(data.status == 1)
                {
                    $("#alert-success").show()
                    $("#alert-success strong").html(data.message)

                }
                else
                {
                    $("#alert-danger").show()
                    $("#alert-danger strong").html(data.message)
                }
                
            },

            error: function(XMLHttpRequest, textStatus, errorThrown) { 
                //location.reload();  
            }  
        })
    }
}

//------------------------- End of all Post function ----------------------------------------------------------------------------------//

//------------------------- All validation function goes here ----------------------------------------------------------------------------//

// function to validate user profile info in home page //

function validate_edit_user_profile()
{

    errorclass : 'error',

    $("#edit_profile_info").validate({
        rules : {
            username : "required",
            email : {
                required : true,
                email : true
            },
            mobile : {
                required : true,
                minlength : 1,
                maxlength : 15
            },
            address : "required",
            city : "required",
            state : "required",
            country : "required",
            
        },

        messages : {
            username : "Please enter the Name",
            email : {
                required : "Please enter the Email id",
                email : "Please provide valid Email Id"
            },
            mobile : {
                required : "Please provide Mobile number",
                maxlength : "Mobile number provided is too long"
            },
            address : "Please mention the Address",
            city : "Please enter the City",
            state : "Please select the State",
            country : "Please select the Country",
            
        }
    })
       
}

//------------------------- End of all validation function goes here ----------------------------------------------------------------------------//