<doctype html>
<html>
	<head>
		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
		<link rel="stylesheet" href="/static/style.css">
		<link rel="stylesheet" href="https://cdn.datatables.net/1.10.10/css/jquery.dataTables.min.css">
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
		<script src="https://cdn.datatables.net/1.10.10/js/jquery.dataTables.min.js"></script>
		<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
		<title> snake search | for all your word counting needs </title>
		<script> (document).ready(function(){('pageranked_urls').DataTable({pageLength: 5})})</script>
	</head>
	<body>
		 <div class="container">
		      <div class="header clearfix">
		        <nav>
		          <ul class="nav nav-pills pull-right">
					% if logged_in:
						<li role="presentation"><a class="unclickable">{{user_email}}</a></li>
					% else:
						<li role="presentation"><a href="/signin">Sign In</a></li>
					% end
					
					% if logged_in: 
						<li role="presentation"><a href="/signout">Sign Out</a></li>
					% end
		          </ul>
		        </nav>
		        <h3 class="text-muted">snake search</h3>
		      </div>

		      {{!base}}

		 </div> <!-- /container -->
	</body>
</html>


