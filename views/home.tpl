% rebase('components/base.tpl')

<div class="row snake-img-container">
  <div onclick="showSecret()" class="snake-img" id='snake-img'></div>
</div>

<div id="snake_game">
    % include('snake_game.tpl')
</div>

<script>
    document.getElementById('snake_game').hidden = true
</script>

<script>
    function showSecret() {

        if (document.getElementById('snake_game').hidden == true) {
            document.getElementById('snake-img').hidden = true
            document.getElementById('snake_game').hidden = false
        }
        else {
            document.getElementById('snake-img').hidden = false
            document.getElementById('snake_game').hidden = true
        }
    }
</script>

% include('components/search-bar.tpl')

