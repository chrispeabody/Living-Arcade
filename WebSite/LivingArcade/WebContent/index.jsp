<!-- index.jsp -->
<!-- Living Arcade -->
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<html>

<head>
<title>Living Arcade</title>
<link href="css/style.css" rel="stylesheet" type="text/css">
<link href="css/colorscheme.css" rel="stylesheet" type="text/css">
<script src="javascript/jquery-3.1.1.js"></script>
<script src="javascript/links.js"></script>
<script src="javascript/index.js"></script>
</head>
<body>
	<div class="links">
		<div class="link" id="linkHome">Home</div>
		<div class="link" id="linkPopulation">Population</div>
		<div class="link" id="linkAbout">About</div>
		<div class="link" id="linkBlog">Blog</div>
		<div class="link" id="linkAccount">Account</div>
	</div>
	<div class="titlebox">
		<h1>Living Arcade</h1>
	</div>
	<div class="wrapper">
		<div class="mainSection">
			<h2 class="sectionHead">Welcome</h2>
			<div class="content" id="welcome">
				A brief description of what this site is should go here. A link to
				the about page will be located here, and the potential for a video
				is definitely there. This should be a brief but comprehensive
				explaination of what the site is all about, and its goals. "The
				generation of web-based arcade game through use of evolutionary
				algorithms."<br>
				<br> This section is currently dynamically sized to the
				information inside it. I figure the information located here won't
				change much, so fitting it directly to the information should work
				best.
			</div>
			<h2 class="sectionHead">News</h2>
			<div class="content" id="news">
				This section should house the first several lines of the latest blog
				post from the news/blog page. That page will have information on the
				latest developments for the site, where things are going, what's
				new, etc. In addition, to make it obvious that this is a preview, we
				should work on finding a "fade to grey" effect to put over the text,
				that gradually goes out toward the bottom. A link to the blog page
				should be apparent, where the latest post will be displayed. <br>
				<br> This area is a static size. Since the length of the blog
				posts will change, and the fade out effect and "more" buttons should
				be present, the actual size of this box shouldn't change, while how
				much content that fits into it will vary.
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