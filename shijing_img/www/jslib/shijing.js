'use strict';


function generateList(data_url,appendDataNode){
    $.getJSON(data_url)
    .done(
        function(data){
            appendDataNode(data);
        })
        .fail(
        function(jqxhr,textStatus,error){
            var err = textStatus + "," + error;
            console.log( "Request Failed:" + err );
        }
        );

}
