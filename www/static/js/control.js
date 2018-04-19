<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Quizing</title>
    <link href="styles/bootstrap.min.css" rel="stylesheet">
    <link href="styles/bootstrap-theme.min.css" rel="stylesheet">
    <link href="styles/mystyles.css" rel="stylesheet"/>
</head>

<body>
    <!--header-->
    <div class="head fixed-top">
        <div class="container">
            <div class="jumbotrons">
                <p id='p1' class="text-center"><strong>QUIZING</strong></p>
                <p id='p2'class="text-center">TEST YOUR SELF, JUST FOR FUN!</p>
            </div>
        </div>
   </div>

    <div class="container">
        <div class="row center">
            <ul class="nav navbar-nav" role="navigation">
                <li><a href="#"><strong>Start</strong></a></li>
                <li><a href="#"><strong>Ranking</strong></a></li>
                <li><a href="#"><strong>Restart</strong></a></li>
                <li><a href="#"><strong>Exit</strong></a></li>
            </ul>
        </div>
    </div>

    <!--mdiddle part-->
    <div class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-2">
                <div class="sidebar">
                    <h3>Profile:</h3>
                    <p>Name:</p>
                    <p>Score:</p>
                    <p>Rank:</p>
                </div>
            </div>

            <div class="col-xs-12 col-sm-8">
                <div class="main-box">
                    <div class="container">
                        <div class="row">
                            <div class="col-xs-12 col-sm-6 col-sm-offset-1">
                                <h3>Please input your user name to start quizing:</h3>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-xs-12 col-sm-3 col-sm-offset-2">
                                <input type="text" class="form-control" id="name">
                                </input><br>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-offset-3">
                                <button class="btn btn-success">START</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="row-footer">
        <h5 class="text-center"> This is a footer sentence!</h5>
    </footer>
</body>

</html>
