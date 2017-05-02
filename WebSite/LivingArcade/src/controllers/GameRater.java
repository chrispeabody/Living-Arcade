package controllers;

import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


import model.MyJDBCConnectionHelper;

/**
 * Servlet implementation class GameRater
 */
@WebServlet("/GameRater")
public class GameRater extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public GameRater() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		Integer rating = Integer.parseInt((String)request.getParameter("star"));
		String gameID = (String)request.getParameter("gameID");
		try{
			Connection conn = MyJDBCConnectionHelper.getConnection();
			//retrieve current rating
			Statement stmt = conn.createStatement();
			PreparedStatement pStmt = conn.prepareStatement("UPDATE Games SET rating = ? WHERE gameID='"+gameID+"'");
			String query = "SELECT rating FROM Games WHERE gameID='" + gameID +"'";
			ResultSet rs = stmt.executeQuery(query);
			Integer currentRating;
			if(rs.next()){
				currentRating=rs.getInt(1);
				currentRating += rating;
				pStmt.setInt(1, currentRating);
				pStmt.executeUpdate();
			}
			conn.close();
			//Statement stmt = conn.prepareStatement("INSERT INTO Games (rating) VALUES(" + rating + ")");
			
		}
		catch(Exception e){
			e.printStackTrace();
		}
		request.getRequestDispatcher("index.jsp").forward(request, response);
	}
	

}
