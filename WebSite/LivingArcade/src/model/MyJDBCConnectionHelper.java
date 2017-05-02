package model;

import java.sql.Connection;
import java.sql.SQLException;

import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;
public final class MyJDBCConnectionHelper {

	private static final String USER_ID = "theUser";
	private static final String USER_PWD = "newPass!!!123";

	private MyJDBCConnectionHelper() {
	}

	public static Connection getConnection() {
		Connection conn = null;
		MysqlDataSource ds = new MysqlDataSource();
		ds.setPassword(USER_PWD);
		ds.setPortNumber(3306);
		ds.setDatabaseName("LivingArcade");
		ds.setServerName("livingarca.de");
		ds.setUser(USER_ID);
		try {
			conn = ds.getConnection();

		} catch (SQLException e) {
			e.printStackTrace();
		}
		return conn;
	}
}
