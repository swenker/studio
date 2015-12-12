<%@ page language="java"%>
<%@ page pageEncoding="UTF-8" %>
<%@ page contentType="text/html; charset=UTF-8" %>
------------------
<%
   String sname = request.getParameter("sn");
   String svalue = request.getParameter("sv");

   session.setAttribute(sname,svalue);
   response.sendRedirect(request.getContextPath() + "/gets.jsp");

%>
------------------