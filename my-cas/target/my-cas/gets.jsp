<%@ page language="java"%>
<%@ page pageEncoding="UTF-8" %>
<%@ page contentType="text/html; charset=UTF-8" %>
------------------
<%
java.util.Enumeration names = session.getAttributeNames();
while(names.hasMoreElements()){
   String sname = (String)names.nextElement();
   String svalue = (String)session.getAttribute(sname);

   out.println("sname:"+sname+";"+svalue);
   out.println("<br>");
}
%>
------------------