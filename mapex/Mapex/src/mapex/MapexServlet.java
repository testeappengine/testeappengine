package mapex;

import java.io.IOException;
import java.net.URL;

import javax.servlet.http.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import java.util.logging.Logger;

import org.w3c.dom.Document;


@SuppressWarnings("serial")
public class MapexServlet extends HttpServlet {
	private static final Logger log = Logger.getLogger(MapexServlet.class.getName());
	private static final String ipInfoDbKey = "f22015b122128905ac18abbfcfeb5b1376727ce5a588f8521ab39a8345c9ec63";
	public void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		String ip = req.getParameter("ip");
		
		String URL = "http://api.ipinfodb.com/v3/ip-city/?key=" + ipInfoDbKey + "&ip="+ip+"&format=XML";
		String latitude = "0";
		String longitude = "0";
		try {
			DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
			DocumentBuilder db = dbf.newDocumentBuilder();
			Document doc = db.parse(new URL(URL).openStream());
			latitude = doc.getElementsByTagName("latitude").item(0).getChildNodes().item(0).getNodeValue();
			longitude = doc.getElementsByTagName("longitude").item(0).getChildNodes().item(0).getNodeValue();
		}
		catch (Exception e) {
			log.info("Excecao!");			
		}
		
		resp.sendRedirect(resp.encodeRedirectURL("map.jsp?lat="+latitude+"&long="+longitude));
	}
}
