//declare all global variables..
var user_id = 0
var redirect_to = ""
var BaseUrl = document.location.origin

$( document ).ready(function() {
    get_signin_signup_page()
})


$(document).on("click",".alert .close",function(){
    $(this).parent().hide()
})

//--------------------------------------------------------------------------------------------------------------------------------------

//------------------------------------------ All Button on click function goes here ---------------------------------------------------

// on click function to get Registration page // 

$(document).on("click","#go_to_register_page",function(){
    get_register_page()
})

// on click function to redirect to Sign in / Sign up page from register page // 

$(document).on("click","#previous_in_register_page, #previous_login",function(){
    get_signin_signup_page()
})

// on click function to hide or show the register button and clearing out the text box fields when inputs are collapsed // 

$(document).on("click","#input_using_mem_no, #input_using_email_mobile",function(){
    var is_mem_expanded = $("#input_using_mem_no").attr("aria-expanded")
    var is_email_mobile_expanded = $("#input_using_email_mobile").attr("aria-expanded")
    $("#mem_no").val("")
    $("#email").val("")
    $("#mobile").val("")
    if (is_mem_expanded == 'false' && is_email_mobile_expanded =='false')
    {
        $("#register").hide()
    }
    else
    {
        $("#register").show()
    }
})

// on click function to hide or show the proceed button and clearing out the text box fields when inputs are collapsed // 

$(document).on("click","#input_using_mem_no_fp, #input_using_mobile_fp",function(){
    var is_mem_expanded = $("#input_using_mem_no_fp").attr("aria-expanded")
    var is_mobile_expanded = $("#input_using_mobile_fp").attr("aria-expanded")
    $("#mem_no").val("")
    $("#mobile").val("")
    if (is_mem_expanded == 'false' && is_mobile_expanded =='false')
    {
        $("#proceed").hide()
    }
    else
    {
        $("#proceed").show()
    }
})

// on click function to post the registration details //

$(document).on("click","#register",function(){
    post_register_page()
})

// on click function to post user profile details //

$(document).on("click","#submit",function(){
    post_user_profile_page()
})

// on click function to get otp page //

$(document).on("click","#alert_otp, #resend_otp", function(){
    get_otp_page()
})

// on click function to verify otp //

$(document).on("click","#otp_verify",function(){
    post_otp_page()
})

// on click function to get login page //

$(document).on("click","#go_to_login_page, #previous_in_fp, #previous_reset_paswd",function(){
    get_login_page()
})

// on click function to post login details // 

$(document).on("click","#login",function(){
    post_login_page()
})

// on click function to get forgot password page // 

$(document).on("click", "#forgot_password",function(){
    get_forgot_password_page()
})

// on click function to post forgot password details // 

$(document).on("click", "#proceed",function(){
    post_forgot_password_page()
})

// on click function to get user register form // 

$(document).on("click", "#alert_register_mem_no, #alert_register_mobile_no",function(){
    get_user_profile()
})

// on click function to post reset password details // 

$(document).on("click", "#save_new_password",function(){
    post_reset_pssword()
})
//------------------------------------------ End of all Button on click function -------------------------------------------------------

//---------------------------------------- Change functionfor dropdown options -------------------------------------------------------------------

$(document).on("change", "#country",function(){
    country_id = $("#country").val()
    select_states() 
})

//---------------------------------------- End of Change function -------------------------------------------------------------------

//---------------------------------------- All GET Functions goes here -----------------------------------------------------------------

// function to get Sign in / Sign up page //

function get_signin_signup_page()
{
    // alert("calling ajax")
    $.ajax({
        type: 'GET', // <-- get method of form
        url : BaseUrl + "/signin_signup", // <-- get action of form
        dataType: 'json',
        success: function(data){
            // alert(data.status)
            if(data.status == 1)
            {
                $("#content").html(data.html);
            }
        },
    })
}

// function to get Register page //

function get_register_page()
{
    $.ajax({
        type: 'GET', // <-- get method of form
        url : BaseUrl + "/register", // <-- get action of form
        dataType: 'json',
        success: function(data){
            if(data.status == 1)
            {
                $("#content").html(data.html);
            }
        },
    })
}

// function to get user profile page //

function get_user_profile()
{
    $.ajax({
        type: 'GET', // <-- get method of form
        url : BaseUrl + "/user_profile/"+user_id, // <-- get action of form
        dataType: 'json',
        success: function(data){
            if(data.status == 1)
            {
                $("#content").html(data.html);
            }
        },
    })
}

// function to get otp page //

function get_otp_page()
{
    $.ajax({
        type: 'GET', // <-- get method of form
        url : BaseUrl + "/otp/"+user_id, // <-- get action of form
        dataType: 'json',
        success: function(data){
            if(data.status == 1)
            {
                $("#content").html(data.html)
                $("#alert-warning").show()
                $("#alert-warning strong").html(data.message)
            }
        },
    })
}

// function to get Login page //

function get_login_page()
{

    $.ajax({
        type: 'GET', // <-- get method of form
        url : BaseUrl + "/login", // <-- get action of form
        dataType: 'json',
        // async:false,
        success: function(data){
            if(data.status == 1)
            {
                $("#content").html(data.html);
            }
        },
    })
}

// function to get forgot password page //

function get_forgot_password_page()
{
    $.ajax({
        type: 'GET', // <-- get method of form
        url: BaseUrl + "/forgot_password", // <-- get action of form
        // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',

        success: function(data){
            if(data.status == 1)
            {
                $("#content").html(data.html);
            }
        },

        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            //location.reload();  
        }  
    })
}

// function to get reset password page //

function get_reset_password_page()
{
    $.ajax({
        type: 'GET', // <-- get method of form
        url: BaseUrl + "/reset_password/"+user_id, // <-- get action of form
        // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',

        success: function(data){
            if(data.status == 1)
            {
                $("#content").html(data.html);
            }
        },

        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            //location.reload();  
        }  
    })
}
//------------------------------------------ End of all GET Functions -------------------------------------------------------------------

//---------------------------------------- All POST Functions goes here -----------------------------------------------------------------

// function to post registration details //

function post_register_page()
{
    $.ajax({
        type: 'POST', // <-- get method of form
        url: $("#user_register").attr('action'), // <-- get action of form
        data: $("#user_register").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',

        success: function(data){
            if(data.status == 1)
            {
                if(data.flag == "otp")
                {
                    user_id = data.user_id
                    get_otp_page()
                }
            }

            if((data.status == 0) || (data.status == 2))
            {
                $("#alert-danger").show()
                $("#alert-danger strong").html(data.message)
            }

        },
    })
}

// function to post user profile page //

function post_user_profile_page()
{
    user_profile_validation()

    if($("#user_profile").valid())
    {
        $.ajax({
            type: 'POST', // <-- get method of form
            url: $("#user_profile").attr('action'), // <-- get action of form
            data: $("#user_profile").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
            dataType: 'json',

            success: function(data){
                if(data.status == 1)
                {
                    get_login_page()
                }
                else
                {
                    $("#alert-danger").show()
                    $("#alert-danger strong").html(data.message)
                }
            }
        })
    } 
}

// function to post otp number //

function post_otp_page()
{
    $.ajax({
        type: 'POST', // <-- get method of form
        url: $("#otp_page").attr('action'), // <-- get action of form
        data: $("#otp_page").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',

        success: function(data){
            if(data.status == 1)
            {
                if (redirect_to == "reset_password") 
                {
                    get_reset_password_page()
                }
                else
                {
                    if(data.flag == "home_page")
                    {
                        window.location.replace(BaseUrl+"/")
                    }
                    if(data.flag == "user_profile")
                    {
                        user_id = data.user_id
                        get_user_profile()
                    }
                }
 
            }
            else
            {
                $("#alert-danger").show()
                $("#alert-danger strong").html(data.message)
            }
        }
    })
}

// function to post login details // 

function post_login_page()
{
    login_page_validation()

    if($("#login_details").valid())
    {
        $.ajax({
            type: 'POST', // <-- get method of form
            url: $("#login_details").attr('action'), // <-- get action of form
            data: $("#login_details").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
            dataType: 'json',
    
            success: function(data){
                if(data.status == 1)
                {
                    user_id = data.user_id
                    window.location.replace(BaseUrl+"/");
                }
                else
                {
                    $("#alert-danger").show()
                    $("#alert-danger strong").html(data.message)
                }
            }
        })
    }
}

// function to post forgot password page details //

function post_forgot_password_page()
{
    $.ajax({
        type: 'POST', // <-- get method of form
        url: $("#forgot_password_deatils").attr('action'), // <-- get action of form
        data: $("#forgot_password_deatils").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',

        success: function(data){
            if(data.status == 1)
            {
                if(data.flag == "otp")
                {
                    user_id = data.user_id
                    redirect_to = data.redirect
                    get_otp_page()
                }
                // if(data.flag == "register_form")
                // {
                //     user_id = data.user_id
                //     $("#alert-warning").show()
                //     $("#alert-warning").html(data.message)

                // }
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

// function to post reset password details //

function post_reset_pssword()
{
    validate_new_password()

    if($("#reset_password_details").valid())
    {
        $.ajax({
            type: 'POST', // <-- get method of form
            url: $("#reset_password_details").attr('action'), // <-- get action of form
            data: $("#reset_password_details").serialize(), // <-- serialize all fields into a string that is ready to be posted to your PHP file
            dataType: 'json',
    
            success: function(data){
                if(data.status == 1)
                {
                   user_id = data.user_id
                   get_login_page() 
                    
                }
                else
                {
                    $("#alert-danger").show()
                    $("#alert-danger strong").html(data.message)
                }
            }
        })        
    }
}

//------------------------------------------ End of all POST Functions -----------------------------------------------------------------

//------------------------------------------ function for dropdown of states based on country selected -----------------------------------------------------------------

function select_states()
{
    $.ajax({
        type: 'GET', // <-- get method of form
        url: BaseUrl + "/states_dropdown/"+country_id, // <-- get action of form
        // <-- serialize all fields into a string that is ready to be posted to your PHP file
        dataType: 'json',

        success: function(data){
            if(data.status == 1)
            {
                $('#state')
                    .find('option')
                    .remove()
                    .end()
                    .append(data.html)
                    ;
            }
        },

        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            //location.reload();  
        }  
    })
}

//------------------------------------------ end function for dropdown of states -----------------------------------------------------------------

//------------------------------------------ Validation function goes here -----------------------------------------------------------------

// function to validate user profile //

function user_profile_validation()
{
    errorclass : 'error',

    $("#user_profile").validate({
        rules : {
            prefix : "required",
            name : "required",
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
            password : {
                required : true,
                minlength : 4,
                maxlength : 8
            },
            confirm_password : {
                required : true,
                equalTo: '#password'
            }
        },

        messages : {
            prefix : "Please mention the Prefix",
            name : "Please enter the Name",
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
            password : {
                required : "Please enter the Password",
                minlength : "Password length must be at least 4 characters",
                maxlength : "Password too long. not more than 8 characters"
            },
            confirm_password : {
                required : "Please re enter the password for confirmation",
                equalTo : "Password doent match. Kindly re-enter"
            }
        }
    })
}

// function to validate Login //

function login_page_validation()
{
    errorclass : 'error',

    $("#login_details").validate({
        rules : {
            email :{
                required : true,
                email : true
            },
            password : "required"
        },

        messages :{
            email : {
                required : "Please enter the Email id",
                email : "Please provide valid Email Id"
            },

            password : "Please enter the password"
        }
    })
}

//function to validate reset password details // 

function validate_new_password()
{
    errorclass : 'error',

    $("#reset_password_details").validate({
        
        rules : {
            new_password : {
                required : true,
                minlength : 4,
                maxlength : 8
            },
            confirm_new_password : {
                required : true,
                equalTo: '#new_password'
            }
        },

        messages : {
            new_password : {
                required : "Please enter the new Password",
                minlength : "Password length must be at least 4 characters",
                maxlength : "Password too long. not more than 8 characters"
            },
            confirm_new_password : {
                required : "Please re enter the new password",
                equalTo : "Password doent match. Kindly re-enter"
            }
        }
    })
}

//------------------------------------------ Validation function goes here -----------------------------------------------------------------