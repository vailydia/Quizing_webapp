        sessionStorage.clear();
        
        // when START button click, cancel the default and using ajax to submit
        $("#login").click(function(){
            $.ajax({
              url: "/login",
              data: {mode: $('input[name=mode]:checked', '#sign').val(), username: $('#username').val()},
              success: function(response){
                  if(response.status == 302){
                      window.location.replace(response.relocate + "?username=" + response.username+ "&mode=" + response.mode);
                  }
            }});
        });
