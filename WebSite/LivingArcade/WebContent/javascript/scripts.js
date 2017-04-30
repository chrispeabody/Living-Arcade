//scripts.js
//William Baumer
//Test scripts (Fix this comment)

function changeElement1(elementID) {
	document.getElementById(elementID).style.font='Times New Roman';
}

function changeElement2(elementID){
	document.getElementById(elementID).style.font='Arial';
}

function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}
/* When the user clicks on the button, 
 toggle between hiding and showing the dropdown content */
function myFunction() {
	document.getElementById("myDropdown").classList.toggle("show");
}

function setCookie(id, imgurl, email, isLoggedOn){
	document.cookie = "ID=" + id;
	document.cookie = "ImageURL=" + imgurl;
	document.cookie = "Email=" + email;
	document.cookie = "L_On=" + isLoggedOn;			
}
// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
	if (!e.target.matches('.dropbtn')) {

		var dropdowns = document
				.getElementsByClassName("dropdown-content");
		for (var d = 0; d < dropdowns.length; d++) {
			var openDropdown = dropdowns[d];
			if (openDropdown.classList.contains('show')) {
				openDropdown.classList.remove('show');
			}
		}
	}
}
function onSignIn(googleUser) {
	var id_token = googleUser.getAuthResponse().id_token;
	var profile = googleUser.getBasicProfile();
	setCookie(profile.getId(), profile.getImageUrl(), profile.getEmail(), "True");
	/*var cook = "ID=" + profile.getId() + "; ImageURL="
			+ profile.getImageUrl() + "; Email=" + profile.getEmail()
			+ "; L_On=True"*/
	console.log("ID=" + getCookie("ID"));
	console.log("ImageURL=" + getCookie("ImageURL"));
	console.log("Email=" + getCookie("Email"));
	console.log("L_On=" + getCookie("L_On"));
	console.log(profile.getEmail());
}

function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(
			function() {
				document.cookie = "L_On=False;";
				console.log(document.cookie);
			});
}
function IsSignedIn() {
	var S_on = getCookie("L_On");
	if (S_on == "True") {
		console.log("yay");
		return true;
	} else {
		console.log("boo");
		return false;
	}
}