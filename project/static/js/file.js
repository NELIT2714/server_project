if(!("konan" in window))konan={};
konan.File=function(url){
this.method='GET';
this.url=url;
this.asynch=true;
this.enctype='application/x-www-form-urlencoded';
this.param={};
this.open=function(f){
  var p='';
  var a=Array.prototype.slice.call(arguments,1);
  var r=new XMLHttpRequest();
  r.open(this.method,this.url,this.asynch);
  r.setRequestHeader('Content-Type',this.enctype);
  r.onreadystatechange=function(){
    if(r.readyState==4)f.apply(f,[r.responseText].concat(a));
    }
  for(var i in this.param)p+='&'+i+'='+encodeURIComponent(this.param[i]);
  if(p.length>0)p=p.substring(1);
  r.send(p);
  }
}
function f_post(url,p,fn){
var f=new konan.File(url);
f.method='POST';
f.param=p;
f.open.apply(f,Array.prototype.slice.call(arguments,2));
}
function f_get(url,fn){
var f=new konan.File(url);
f.open.apply(f,Array.prototype.slice.call(arguments,1));
}
f_open=f_get;
