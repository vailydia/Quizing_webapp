
        port = '80'
        // document.domain: Returns the domain name of the server that loaded the document
        console.log('http://' + document.domain + ':' + port);
        var socket = io.connect('http://' + document.domain + ':' + port);

        var user = {};
        var answer = null;
        var id = 0;
        var question = null;
        var set = null;

        if (typeof(Storage) == "undefined") {
            console.log("Sorry, your browser does not support Web Storage...");
        }
        sessionStorage = window.sessionStorage;
        console.log($('#username').text());
        console.log($('#mode').text());
        sessionStorage.setItem("username", $('#username').text());
        sessionStorage.setItem("mode", $('#mode').text());
        //document.getElementById("result").innerHTML = sessionStorage.getItem("lastname");

        $(document).ready(function(){
            if(sessionStorage.getItem("mode") == 'single'){
                $("#choosezone").hide();
            }else{
                $("#queszone").hide();
            }
        });

        socket.on('connect', function() {
            // start the quiz loop
            if(sessionStorage.getItem("mode") == 'single'){
                socket.emit('start quiz', {
                      data:'start quiz',
                  username: sessionStorage.getItem("username"),
                      mode: sessionStorage.getItem("mode")
                });
            }
            if(sessionStorage.getItem("mode") == 'battle'){
                socket.emit('join room', {
                  username: sessionStorage.getItem("username"),
                      mode: sessionStorage.getItem("mode")
                });
            }
        });

        socket.on('handle wait userlists', function(waiting_users){
            console.log('receive wait list of user names.');
            console.log(waiting_users);
            // $( "#userlist" ).load( "/main #userlist" );
            // 待处理
        });

        function choose_user(battle_username){
            console.log(battle_username);
            sessionStorage.setItem('battle_username', battle_username);
            $("#choosezone").hide();
            $("#queszone").show();
            socket.emit('start quiz', {
                battle: battle_username,
                  data:'start quiz',
              username: sessionStorage.getItem("username"),
                  mode: sessionStorage.getItem("mode")
            });
        }

        // message handler for the 'join_room' channel
        socket.on('joined-room', function(response) {

            console.log("joined-room: ");
            console.log(response);
            if(sessionStorage.getItem("mode") == 'single'){
                $(".sidebar_battle").hide();
                $('#username').text(response.user.username);
                $('#score').text(response.user.score);
                $('#winRate').text(response.user.winRate);
            }else{
                $("#choosezone").hide();
                $("#queszone").show();
                sessionStorage.setItem("room", response.room);
                if(response.user.username == sessionStorage.getItem('username')){
                    $('#username').text(response.user.username);
                    $('#score').text(response.user.score);
                    $('#winRate').text(response.user.winRate);
                    $('#username_battle').text(response.battle_user.username);
                    $('#score_battle').text(response.battle_user.score);
                    $('#winRate_battle').text(response.battle_user.winRate);
                    sessionStorage.setItem('battle_username', response.battle_user.username);
                }else {
                    $('#username').text(response.battle_user.username);
                    $('#score').text(response.battle_user.score);
                    $('#winRate').text(response.battle_user.winRate);
                    $('#username_battle').text(response.user.username);
                    $('#score_battle').text(response.user.score);
                    $('#winRate_battle').text(response.user.winRate);
                    sessionStorage.setItem('battle_username', response.user.username);
                }
            }

            //renew the question
            question = response.question;
            id = response.id;

            $('#nid').text('    No.' + (id+1));
            $('#Q').text(question['question']);
            $('#A').html('&nbsp &nbsp' + question.answer[0]);
            $('#B').html('&nbsp &nbsp' + question.answer[1]);
            $('#C').html('&nbsp &nbsp' + question.answer[2]);
            $('#D').html('&nbsp &nbsp' + question.answer[3]);

            //using setInterval to realize a Countdown。
            (function() {
                var time = 10;
                set = setInterval(function() {
                    time--;
                    $('#time').text(time);
                    if(time === 0) {
                        clearInterval(set);
                        socket.emit('start quiz', {
                               ans: answer,
                                id: id,
                              data:'quiz process',
                          username: sessionStorage.getItem("username"),
                            battle: sessionStorage.getItem("battle_username"),
                              mode: sessionStorage.getItem("mode"),
                              room: sessionStorage.getItem("room")
                        });
                        document.getElementById(answer).setAttribute("active", false);
                        answer = null;
                    }
                }, 1000);
            })()
        });

        // handle the game over : show the score & rank; out room?? de connect?
        socket.on('game-over', function(response) {
            if(sessionStorage.getItem("mode") == 'single'){
              $('.main-box').html('<h1><center>✌️ ALL DONE ✌️</center></h1><br><h4><center>User name: '
                           + response.user.username + '</center></h4><h4><center>Score: '
                           + response.user.score + '</center></h4><h4><center>WinRate: '
                           + response.user.winRate + ' </center></h4><br>'
                           + '<center><button class="btn btn-success" onclick="newGame()">NEW START</button></center>');
            }else{
                //renew the current score
                var myScore = 0, battleScore = 0;
                if(response.user.username == sessionStorage.getItem('username')){
                    $('#score').html(response.user.score);
                    $('#winRate').text(response.user.winRate);
                    myScore = response.user.score;
                    $('#score_battle').html(response.battle_user.score);
                    $('#winRate_battle').text(response.battle_user.winRate);
                    battleScore = response.battle_user.score;
                }else{
                    $('#score').html(response.battle_user.score);
                    $('#winRate').text(response.battle_user.winRate);
                    myScore = response.battle_user.score;
                    $('#score_battle').html(response.user.score);
                    $('#winRate_battle').text(response.user.winRate);
                    battleScore = response.user.score;
                }
                var winnerInfo = "";
                if(myScore > battleScore){
                    winnerInfo = "✌️ Congrats, YOU WIN ✌️";
                }else if (myScore < battleScore) {
                    winnerInfo = "💪 YOU LOSE, KEEP ON 💪";
                }else{
                    winnerInfo = "🤝 Both sides TIE 🤝"
                }

                $('.main-box').html('<center><h1>' + myScore + '</h1>&nbsp &nbsp<h1>'
                                     + winnerInfo + '</h1>&nbsp &nbsp<h1>' + battleScore + '</h1></center><br><br>'
                                     + '<center><button class="btn btn-success" onclick="newGame()">NEW START</button></center>');

            }
        });

        function select(tab){
            answer = null;
            if (tab === 1) {
                document.getElementById('A').setAttribute("active", true);
                answer = 'A';
            }else if(tab === 2) {
                document.getElementById('B').setAttribute("active", true);
                answer = 'B';
            }else if(tab === 3) {
                document.getElementById('C').setAttribute("active", true);
                answer = 'C';
            }else {
                document.getElementById('D').setAttribute("active", true);
                answer = 'D';
            }
            console.log('select answer: ' + tab)
        }

        function submitAnswer(){
            if(answer != null){
                clearInterval(set);
                socket.emit('start quiz', {
                       ans: answer,
                        id: id,
                      data:'quiz process',
                  username: sessionStorage.getItem("username"),
                    battle: sessionStorage.getItem("battle_username"),
                      mode: sessionStorage.getItem("mode"),
                      room: sessionStorage.getItem("room")
                });
            }else{
                alert("Please choose a answer!");
            }
            //after submit, clear answer!
            answer = null;
        }

        socket.on('server response', function(data){
            document.getElementById("subbtn").disabled = true;
        });

        //start new round, clear all variable, out room, de connect...etc
        function newGame(){
            sessionStorage.clear();
            window.location.href = "/";
        }
