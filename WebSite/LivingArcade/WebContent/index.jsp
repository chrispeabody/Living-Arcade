<!-- index.jsp -->
<!-- Living Arcade -->
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<%@ page import="org.jsoup.nodes.*"%>
<%@ page import="org.jsoup.select.*"%>
<%@ page import="org.jsoup.*"%>
<html>

<head>
<title>Living Arcade</title>
<link href="css/style.css" rel="stylesheet" type="text/css">
<link href="css/colorscheme.css" rel="stylesheet" type="text/css">
<script src="javascript/jquery-3.1.1.js"></script>
<script src="javascript/links.js"></script>
<script src="javascript/index.js"></script>
<script src="javascript/scripts.js"></script>
<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id"
	content="1052657695220-3tvej8vfhmgjtvhdbmqjolppi5s579hb.apps.googleusercontent.com">
<style>
ul {
	list-style-type: none;
	margin: 0;
	padding: 0;
	overflow: hidden;
	background-color: #333;
}

li {
	float: left;
}

li a, .dropbtn {
	display: inline-block;
	color: white;
	text-align: center;
	padding: 14px 16px;
	text-decoration: none;
}

li a:hover, .dropdown:hover .dropbtn {
	background-color: red;
}

li.dropdown {
	display: inline-block;
}

.dropdown-content {
	display: none;
	position: absolute;
	background-color: #f9f9f9;
	min-width: 160px;
	box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
	z-index: 1;
}

.dropdown-content a {
	color: black;
	padding: 12px 16px;
	text-decoration: none;
	display: block;
	text-align: left;
}

.dropdown-content a:hover {
	background-color: #f1f1f1
}

.show {
	display: block;
}
</style>
</head>
<body>

	<ul>
		<li class="dropdown"><a href="javascript:void(0)" class="dropbtn"
			onclick="myFunction()">Menu</a>
			<div class="dropdown-content" id="myDropdown">
				<div class="link" id="linkHome">Home</div>
				<div class="link" id="linkPopulation">Population</div>
				<div class="link" id="linkAbout">About</div>
				<div class="link" id="linkBlog">Blog</div>
				<div class="link" id="linkAccount">Account</div>
			</div></li>
	</ul>
	<div class="g-signin2" style="float: right" data-onsuccess="onSignIn"></div>
	<div id="signOutbutton">
		<a href="#" onclick="signOut();">Sign out</a>
	</div>
	<div id ="MyWelcome" style ="float: right"></div>
	
	     




	<script>
	function MyChecker()
	{
		console.log("yup");
		if (IsSignedIn()) {
			changeElement2("signOutbutton");
		} else {
			changeElement1("signOutbutton");
		}
		if (IsSignedIn()) {
			changeElement2("MyWelcome");
		} else {
			changeElement1("MyWelcome");
		}
	}
	MyChecker();
	</script>
	<div class="titlebox">
		<h1>Living Arcade</h1>
	</div>
	<div class="wrapper">
		<div class="mainSection">
			<h2 class="sectionHead">Welcome</h2>
			<div class="content" id="welcome">
				Welcome to the Living Arcade! We're a work in progress at the
				moment, but keep your eye on this page! Our goal is to create
				web-based arcade games using evolutionary algorithms.<br> <br>
			</div>
			<h2 class="sectionHead">News</h2>
			<div class="content" id="news">
				<%
					Document doc = Jsoup.connect("http://thelivingarcade.tumblr.com/").get();
					Element body = doc.select("div.body-text").first();
					out.println(body.text());
					out.println("<br><a href=\"http://thelivingarcade.tumblr.com\">View the blog!</a>");
				%>
			</div>
			<h2 class="sectionHead">Newly generated games</h2>
			<div class="content" id="newgames">
				<div class="gameframe" id="linkPong" onclick="pongDirect()">
					<img src="images/tempgame.png" alt=""> Pong
				</div>
				<div class="gameframe">
					<img src="images/tempgame.png" alt=""> Name
				</div>
				<div class="gameframe">
					<img src="images/tempgame.png" alt=""> Name
				</div>
			</div>
		</div>
	</div>
</body>

</html>