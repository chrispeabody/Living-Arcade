package controllers;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import model.MyJDBCConnectionHelper;

/**
 * Servlet implementation class UnityServlet
 */
@WebServlet("/UnityServlet")
public class UnityServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public UnityServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String ID = (String)request.getParameter("ID");
		String JSON = "";
		try{
			Connection conn = MyJDBCConnectionHelper.getConnection();
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT gameJSON FROM Games WHERE gameID="+ID);
			if(rs.next()){
				JSON = rs.getString(1);
			}
			else{
				JSON = "Nothing Found!";
			}
			stmt.close();
			conn.close();
		}catch(Exception e){
			JSON = e.getMessage();
			e.printStackTrace();
		}
		response.getWriter().append(JSON);
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
