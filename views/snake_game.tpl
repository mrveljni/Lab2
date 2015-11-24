<doctype html>
<html>
<head>
  <title>Javascript Snakes</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <link href="/static/snakes.css" media="screen, print" rel="stylesheet" type="text/css" />
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
        <ul>
          <li class='author'>Created by <a target="_credits" href="http://codeincomplete.com/posts/2011/8/5/starting_snakes/">Jake Gordon</a></li>
          <li><span class='key'>            Logo </span> <a class='value' target="_credits" href="http://codeincomplete.com/posts/2011/7/16/quest_for_indy_font/">Jake Gordon</a></li>
          <li><span class='key'>           Fonts </span> <a class='value' target="_credits" href="http://www.dafont.com/sf-fedora.font">SF Fedora</a></li>
          <li><span class='key'>       Watermark </span> <a class='value' target="_credits" href="http://www.istockphoto.com/file_closeup.php?id=4788598">VichanChairat</a></li>
          <li><span class='key'>           Music </span> <a class='value' target="_credits" href="http://luckylionstudios.com/royalty-free-video-game-music-library/">Lucky Lion Studios</a></li>
          <li><span class='key'>        Sound FX </span> <a class='value' target="_credits" href="http://www.premiumbeat.com/">Premium Beat</a></li>
          <li><span class='key'>JS state machine </span> <a class='value' target="_credits" href="https://github.com/jakesgordon/javascript-state-machine">Jake Gordon</a></li>
          <li><span class='key'>     JS selector </span> <a class='value' target="_credits" href="http://sizzlejs.com/">Sizzle</a></li>
          <li><span class='key'>        JS audio </span> <a class='value' target="_credits" href="https://github.com/jakesgordon/javascript-audio-fx">Jake Gordon</a></li>
          <li><span class='key'>    JS animation </span> <a class='value' target="_credits" href="http://berniesumption.com/software/animator/">Bernie Sumption</a></li>
        </ul>
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
</html>
