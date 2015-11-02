
upload photo:
1.convert img to small ones using cmd tool.
2.put to /var/shijing/img/raw?
3.click load on webpage.

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


images handler:
 choose images from album?
 insert into content directly at the same time into album?


steps:
1.basic metadata without images:
2.album
3.column
4.content with images
  html editor
5.comment
6.user management

choose a html editor

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