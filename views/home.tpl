% rebase('components/base.tpl')

<div class="row snake-img-container">
  <div class="snake-img"></div>
</div>

<form name="snake_query" action="http://localhost:8080/" method="GET">
    <div class="row">
      <div class="col-lg-12">
        <div id="query-group" class="input-group">
          <input id="query" type="text" name="keywords" type="text" class="form-control" placeholder="Search for...">
        </div><!-- /input-group -->
      </div><!-- /.col-lg-6 -->
    </div><!-- /.row -->
    <div class="row">
        <div class="col-lg-12">
            <input value="Search" type="submit" class="btn btn-lg btn-success query-btn center-block" />
        </div>
    </div>
</form>

<!-- % include('./views/table.tpl', title="Andrew", wordDict = {'word':1, 't':2}) -->