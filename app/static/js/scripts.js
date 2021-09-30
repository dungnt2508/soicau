
$("#item_soibaucua").on("click",function(e){
        //Getting Value
        $('#direct_chat_messages').append('<div class="direct-chat-msg"><div class="direct-chat-infos clearfix"><span class="direct-chat-name float-left">Snake</span><span class="direct-chat-timestamp float-right">time</span></div><img class="direct-chat-img" src="static/dist/img/user1-128x128.jpg" alt="message user image"><div class="direct-chat-text" id="messages_bot">Bạn đã chọn soi bầu cua</div>	</div>');
        $("#dashboard_taixiumd5").hide();
        $("#dashboard_baucua").show();

});


$("#item_soitaixiumd5").on("click",function(e){
        //Getting Value
        $('#direct_chat_messages').append('<div class="direct-chat-msg"><div class="direct-chat-infos clearfix"><span class="direct-chat-name float-left">Snake</span><span class="direct-chat-timestamp float-right">time</span></div><img class="direct-chat-img" src="static/dist/img/user1-128x128.jpg" alt="message user image"><div class="direct-chat-text" id="messages_bot">Bạn đã chọn soi tài xỉu md5</div>	</div>');
        $("#dashboard_baucua").hide();
        $("#dashboard_taixiumd5").show();

//        $.ajax({
//                url: "/taixiumd5/predict",
//                type: "GET",
//                dataType: "json",
//                success: function(resp){
//                    console.log(resp)
//                    $("#taixiumd5_phien").val(resp.phien);
//                    $("#taixiumd5_xx123").val(resp.kq_number);
//                    $("#taixiumd5_kq").val(resp.kq);
//                    $("#taixiumd5_kq_str").val(resp.kq_str);
//                },
//                error: function(resp){
//                    console.log(resp)
//
//                }
//            })

});

