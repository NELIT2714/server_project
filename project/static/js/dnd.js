Dnd=function(id){
	var t=this;
	var e=t.element=typeof(id)=='string'?document.querySelector(id):id;
	for(var n in Dnd.objects)if(Dnd.objects[n].element==e)return Dnd.objects[n];
	Dnd.objects.push(t);
	t.drag=function(ev){
		if(ev.preventDefault)ev.preventDefault();
		t.x=ev.clientX;
		t.y=ev.clientY;
		t.onup=document.onmouseup;
		t.onmove=document.onmousemove;
		document.onmouseup=t.drop;
		document.onmousemove=t.move;
	}
	t.drop=function(ev){
		document.onmouseup=t.onup;
		document.onmousemove=t.onmove;
		t.target=ev.target?ev.target:ev.srcElement;
		if(t.ready!=undefined)return t.ready();
	}
	t.move=function(ev){
		t.left=e.currentStyle?e.currentStyle["marginLeft"]:window.getComputedStyle(e,"").getPropertyValue("margin-left");
		t.top=e.currentStyle?e.currentStyle["marginTop"]:window.getComputedStyle(e,"").getPropertyValue("margin-top");
		if(!parseInt(t.left))t.left=0;
		if(!parseInt(t.top))t.top=0;
		e.style.marginLeft=parseInt(t.left)+ev.clientX-t.x+"px";
		e.style.marginTop=parseInt(t.top)+ev.clientY-t.y+"px";
		t.x=ev.clientX;
		t.y=ev.clientY;
		if(t.action!=undefined)return t.action();
	}
}
Dnd.objects=[];
function dnd(ev,id,fn){
	if(id==undefined||id==0)id=ev.target?ev.target:ev.srcElement;
	var d=new Dnd(id);
	if(fn!=undefined){
		var a=Array.prototype.slice.call(arguments,3);
		d.ready=function(){fn.apply(fn,a)};
	}
	d.drag(ev);
}
