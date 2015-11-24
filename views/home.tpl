% rebase('components/base.tpl')

<div class="row snake-img-container">
  <div class="snake-img" id='snake-img'></div>
</div>

% include('snake_game.tpl')
<script>
    $('#snake-img').click(function(){
        console.log("HELLO")
    })
</script>

% include('components/search-bar.tpl')

