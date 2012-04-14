<%@ page contentType="text/html;charset=UTF-8" language="java"%>
<!DOCTYPE html>
<html>
    <head>
        <title>Localiza&ccedil;&atilde;o do IP fornecido</title>
        <meta charset="utf-8">
        
        <!--  Form escondido para pegar os argumentos por URL -->
        <FORM NAME="args">
		<INPUT TYPE="hidden" NAME="args">
		</FORM>
		
        <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
        <script type="text/javascript">
        
	    // Funcoes de tratamento de string para pegar os argumentos
            function getLatArg(str) {
            	theleft = str.indexOf("=") + 1;
            	theright = str.lastIndexOf("&");
            	return(str.substring(theleft, theright));
            }
            function getLongArg(str) {
            	theleft = str.lastIndexOf("=");
            	return(str.substring(theleft+1,str.length));
            }
            var locate = window.location;
            document.args.args.value = locate;
            var text = document.args.args.value;
            var lat = getLatArg(text);
            var longi = getLongArg(text);
            
            // Usa a API do google maps para apontar a localizacao
            var map;
            var initialLocation = new google.maps.LatLng(lat,longi);
            function init() {
                var duckOptions = {
                    zoom: 12,
                    center: initialLocation,
                    mapTypeId: google.maps.MapTypeId.HYBRID
                };
                map = new google.maps.Map(document.getElementById("map_canvas"), duckOptions);
                var marker = new google.maps.Marker({
                    position: initialLocation,
                    map: map
                });
            }
        </script>
    </head>
    <body  onload="init()">
        <h1>Localiza&ccedil;&atilde;o do IP fornecido</h1>
        <div id="map_canvas" style="width:100%;height:800px"></div>
    </body>
</html>
