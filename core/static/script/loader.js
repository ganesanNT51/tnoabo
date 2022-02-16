$(document).ajaxStart(function(){
    // alert("ajax started")
    StartLoader()
});

$(document).ajaxStop(function(){
    // alert("ajax stoped")
    StopLoader();
});

function StartLoader()
{

    // <div id="loader">
    //         <div id="loader_block">
    //         </div>
    //         <div class="row">
    //             <div class="col-md-12">
    //                 <div class="loader align-middle">
    //                     <p>Loading...</p>
    //                     <div class="loader-inner"></div>
    //                     <div class="loader-inner"></div>
    //                     <div class="loader-inner"></div>
    //                 </div>
    //             </div>
    //         </div>
            
    //     </div>

    var str= "";
    str +="<div id=\"loader\">";
    str +="    <div id=\"loader_block\">";
    str +="    </div>";
    str +="    <div class=\"row\">";
    str +="        <div class=\"col-md-12\">";
    str +="            <div class=\"loader align-middle\">"
    str +="                <p> Loading Please wait...</p>"
    str +="                <div class=\"loader-inner\"></div>"
    str +="                <div class=\"loader-inner\"></div>"
    str +="                <div class=\"loader-inner\"></div>"
    str +="            </div>"
    str +="        </div>"
    str +="    </div>"
    str +="</div>"
    $("body").append(str)
}


function StopLoader()
{
    $( "#loader" ).remove();
}

