'use strict';

var imgBaseURL = '';
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

function appendImage(data){
    var right_img = $("#right_img");
    for(var i=0;i<data.rlist.length;i++){
        var img = data.rlist[i];
        var imgNode = $('<img src="'+imgBaseURL+img.thumbnail+'" alt="" width="205" class="img-border img-indent-2">');
        right_img.append(imgNode);
    }

}


function randomPic(imgBaseURL){
    generateList('/p/site/rpic',appendImage);
}