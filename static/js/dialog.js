Dialog=function(a){
	this.style=function(){
		var l=document.getElementsByTagName('link');
		var e=document.createElement("link");
		e.setAttribute("type","text/css");
		e.setAttribute("rel","stylesheet");
		e.setAttribute("href",Dialog.path+this.css);
		for(var i in l)if(l[i].rel=="stylesheet"&&e.href==l[i].href)e=l[i];
		document.body.appendChild(e);
		return e;
	}
	this.type=function(){
		if(/^\w+$/g.test(this.url))this.url=document.getElementById(this.url);
		if(typeof(this.url)!="string")return 2;
		var p=this.url.substring(this.url.lastIndexOf(".")+1).toLowerCase();
		return (p=="jpg"||p=="png"||p=="jpeg"||p=="gif")?1:0;
	}
	this.open=function(){
		var t=this;
		if(t.window&&t.window.style.display=="none")return t.show();
		var b=['<iframe id="'+t.id+'_data" onload="Dialog.objects[\''+t.id+'\'].onload()" src="'+t.url+'"></iframe>',
		'<img id="'+t.id+'_data" onload="Dialog.objects[\''+t.id+'\'].onload()" src="'+t.url+'">',
		'<div id="'+t.id+'_data"></div>'];
		var p=t.tpl.replace("{data}",b[t.type()]).replace(/\{id\}/g,t.id);
		p=p.replace("{title}",t.title||"").replace("{caption}",t.caption||"");
		if(!t.bg||!t.bg.parentNode)t.bg=Dialog.add("a");
		t.bg.className="dialog-bg dialog-load";
		t.bg.onclick=function(){t.close()};
		if(!t.window||!t.window.parentNode)t.window=Dialog.add("div");
		t.window.innerHTML=p;
		t.window.style.display="none";
		if(t.type()==2){
			document.getElementById(t.id+"_data").innerHTML=t.url.innerHTML;
			t.onload();
		}
	}
	this.onload=function(){
		var t=this;
		var d=document.getElementById(t.id+"_data");
		var s=t.window.firstElementChild.style;
		t.bg.className="dialog-bg";
		t.window.style.display="block";
		var w=t.width&&t.width.toString().indexOf("%")>0?Math.round(parseInt(t.width)*innerWidth/100):t.width;
		var h=t.height&&t.height.toString().indexOf("%")>0?Math.round(parseInt(t.height)*innerHeight/100):t.height;
		var x=t.x&&t.x.toString().indexOf("%")>0?Math.round(parseInt(t.x)*innerWidth/100):t.x;
		var y=t.y&&t.y.toString().indexOf("%")>0?Math.round(parseInt(t.y)*innerHeight/100):t.y;
		var dw=t.window.firstElementChild.offsetWidth-d.offsetWidth;
		var dh=t.window.firstElementChild.offsetHeight-d.offsetHeight;
		if(!h&&!w&&d.offsetWidth>(innerWidth-dw)&&(d.offsetWidth/innerWidth>=d.offsetHeight/innerHeight))w=innerWidth-dw*2;
		if(!h&&!w&&d.offsetHeight>(innerHeight-dh)&&(d.offsetWidth/innerWidth<d.offsetHeight/innerHeight))h=innerHeight-dh*2;
		if(x)s.left=x+"px";
		if(y)s.top=y+"px";
		if(w)d.style.width=w+"px";
		if(h)d.style.height=h+"px";
		t.window.className=t.class;
		if(t.fn)return t.fn.apply(t.fn,t.arg);
	}
	this.hide=function(){
		this.window.style.display="none";
		this.bg.className="";
	}
	this.show=function(){
		this.window.style.display="block";
		this.bg.className="dialog-bg";
	}
	this.close=function(){
		var b=document.body;
		b.removeChild(this.bg);
		b.removeChild(this.window);
	}
	this.id=a.id||"dialog";
	var d=Dialog.objects[this.id]?Dialog.objects[this.id]:this;
	var p='url,fn,arg,width,height,x,y,title,caption,css,html,tpl,class'.split(",");
	for(var i in p)d[p[i]]=a[p[i]]!=undefined?a[p[i]]:undefined;
	if(!d.tpl)d.tpl='<div class="dialog" id="{id}"><a onclick="Dialog.objects[\'{id}\'].close()" class="dialog-close"></a><a onmousedown="dnd(event,\'#{id}\')" class="dialog-move"></a><div class="dialog-title">{title}</div><div class="dialog-data">{data}</div><div class="dialog-caption">{caption}</div></div>';
	if(!d.css)d.css="../css/dialog.css";
	if(!d.class)d.class=(a.x||a.y)?"dialog-open":"dialog-center";
	d.link=d.style();
	return Dialog.objects[d.id]=d;
}
Dialog.add=function(n){
	var e=document.createElement(n);
	document.body.appendChild(e);
	return e;
}
Dialog.inc=function(a){
	var s=document.createElement("script");
	s.src=a;
	document.getElementsByTagName("head")[0].appendChild(s);
}
Dialog.path=function(){
	var p, r="", s=document.getElementsByTagName('script');
	for(var i in s)if(s[i].src&&s[i].src.indexOf('dialog.js')>0)p=s[i].src.split("/").slice(0,-1);
	var d=location.href.split("/").slice(0,-1);
	for(var i in d)if(d[i]!=p[i])r+="../";
	for(var i in p)if(d[i]!=p[i])r+=p[i]+"/";
	return r;
}();
Dialog.init=function(){
	if(!("f_get" in window))Dialog.inc(Dialog.path+"file.js");
	if(!("dnd" in window))Dialog.inc(Dialog.path+"dnd.js");
}();
Dialog.objects=[];
function dialog(url,a,fn){
	if(!a)a={};
	a.url=url;
	a.fn=fn;
	a.arg=Array.prototype.slice.call(arguments,3);
	var d=new Dialog(a);
	d.html?f_get(Dialog.path+d.html,function(t){d.tpl=t;d.open.call(d);}):d.open();
}
