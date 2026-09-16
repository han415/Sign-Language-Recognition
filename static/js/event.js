function post_data_text() {

    var form_data = new FormData();
    form_data.append('sentence', $("#input_text").val());

    $.ajax({
        url: "/predict_text",
        data: form_data,
        type: "post",
        dataType: "json",
        processData: false,//用於對data參數進行序列化處理 這裏必須false
        contentType: false, //必須
        success: function (data) {
            console.log(data.result)
           document.getElementById("result_text").innerHTML=data.result
        },
        error: function(xhr, status, error){
            $('#response').text('Error: ' + error);
        }
    })
}

function post_data_image() {


    $.ajax({
        url: "/predict_image",
        type: "GET",
        dataType: "json",
        processData: false,//用於對data參數進行序列化處理 這裏必須false
        contentType: false, //必須
        success: function (data) {
            console.log(data.result)
        //    document.getElementById("result_image").innerHTML=data.result
           $('#input_text').val(data.result)
        },
        error: function(xhr, status, error){
            $('#response').text('Error: ' + error);
        }
    })
}