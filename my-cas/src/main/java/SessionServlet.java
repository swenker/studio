

import javax.servlet.*;
import javax.servlet.http.*;
import java.io.IOException;

public class SessionServlet extends HttpServlet {

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String attributeName = req.getParameter("nam");
		String attributeValue = req.getParameter("val");
		req.getSession().setAttribute(attributeName, attributeValue);
		resp.sendRedirect(req.getContextPath() + "/gets.jsp");
	}

	private static final long serialVersionUID = 2878267318695777395L;
}
