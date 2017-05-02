<!doctype html>
<html lang="en-us">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Unity WebGL Player | Pseudo-Pong Game</title>
<link href="css/style.css" rel="stylesheet" type="text/css">
<link href="css/colorscheme.css" rel="stylesheet" type="text/css">
<link rel="shortcut icon" href="TemplateData/favicon.ico" />
<script src="TemplateData/UnityProgress.js"></script>
</head>
<body class="template">
	<div class="template-wrap clear">
		<canvas class="emscripten" id="canvas"
			oncontextmenu="event.preventDefault()" height="720px" width="1280px"></canvas>
		<br>
		<div class="logo"></div>
		<div class="fullscreen">
			<img src="TemplateData/fullscreen.png" width="38" height="38"
				alt="Fullscreen" title="Fullscreen" onclick="SetFullscreen(1);" />
		</div>
		<div class="title">Pseudo-Pong Game</div>
	</div>
	<script type='text/javascript'>
		var Module = {
			TOTAL_MEMORY : 268435456,
			errorhandler : null, // arguments: err, url, line. This function must return 'true' if the error is handled, otherwise 'false'
			compatibilitycheck : null,
			backgroundColor : "#222C36",
			splashStyle : "Light",
			dataUrl : "Release/pongHTML.data",
			codeUrl : "Release/pongHTML.js",
			asmUrl : "Release/pongHTML.asm.js",
			memUrl : "Release/pongHTML.mem",
		};
	</script>
	<script src="Release/UnityLoader.js"></script>

</body>
</html>