<head>
  <title>Javascript Snakes</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <link href="/static/snakes.css" rel="stylesheet" type="text/css"/>
</head>

<body>

  <div id="snakes">

    <div id='sound' class='on' title='toggle music and fx' style='display:none;'></div>

    <div id="score">
      <span class="current"><span class='label'>Score: </span><span class="value">000000</span></span>
      <span class="high"><span class='label'>High: </span><span class="value">000000</span></span>
    </div>

    <canvas id="canvas">
      <div class='unsupported'>
        Sorry, this example cannot be run because your browser does not support the &lt;canvas&gt; element
      </div>
    </canvas>

    <div id="overlay">

      <div id="loading" class='menu' style='display:none;'>
        <h1>Loading...</h1>
      </div>

      <div id="highscores" class='menu' style='display:none;'>
        <h1>High Scores</h1>
        <ul></ul>
      </div>

      <div id="credits" class='menu' style='display:none;'>
      </div>
    </div>

    <div id="help">
      ( use the arrow and enter keys for control )
    </div>

  </div>

  <script src="/static/snakes.js"></script>
  <script>
  Game.ready(function() {
    game = Snakes();
  });
  </script>

</body>
