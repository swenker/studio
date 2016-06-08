
upload photo:
nginx/shijing.conf :client_max_body_size
cgi.maxlen

tips:
~/software/uwsgi-2.0.3/uwsgi web.ini


--why html+ajax instead of python render?
for big pages,this can speed up the page loading

two types of design:
public pages:
http://pages/list.html
   html--js-get json from python

admin/private pages:
http://p/adm/new_article...
   python --check session--load data from db- html

issues encountered:
1.what to be primary key? why the id is odds? it's due to db configuration.
2.title field for image or not when upload?
  not so easy to add it when using dropzone like framework?
  how to design image upload function?


db:refactor--using prepared statements instead of direct string assignments.

put new and edit into the same form(using js to populate the form?).

classified by date in a given album?

jquery:
http://learn.jquery.com/using-jquery-core/selecting-elements/


1.for convenience ,edit pages should be put into templates

http://yinyushijing.cn
http://yinyushijing.cn/


implementation rules:
log info are recorded in service layer instead of controller [action?]

zip -9 abc.zip *.JPG

one question:
what to do if the system was broken when processing order images?