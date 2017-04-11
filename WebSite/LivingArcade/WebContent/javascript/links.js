// links.js
// Chris Peabody
// Living Arcade

function pongDirect() {
		document.location.href = "PongDirect";

	}

var main = function() {
	$('#linkHome').click(function() {
		window.location = "index.jsp";
	});

	$('#linkPopulation').click(function() {
		window.location = "population.html";
	});

	$('#linkAbout').click(function() {
		window.location = "about.html";
	});

	$('#linkBlog').click(function() {
		window.location = "blog.html";
	});

	$('#linkAccount').click(function() {
		window.location = "account.html";
	});
}

$(document).ready(main);