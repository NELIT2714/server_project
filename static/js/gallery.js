Gallery=function(id){
	var t=this;
	this.open=function(k,c){
		this.nom=k;
		var c=c!=undefined?(c):"dialog-center";
		dialog(this.a[k].src,{title:this.a[k].title,id:this.id+"_dialog",tpl:this.tpl,class:c},function(){t.load()});
	}
	this.next=function(k){
		var n=this.nom+k;
		var c=k>0?"dialog-next":"dialog-prev";
		if(this.a[n])this.open(n,c);
	}
	this.load=function(){
		document.querySelector("#"+this.id+"_dialog .dialog-next").style.display=this.a[this.nom+1]?"block":"none";
		document.querySelector("#"+this.id+"_dialog .dialog-prev").style.display=this.a[this.nom-1]?"block":"none";
	}
	this.init=function(){
		var a=document.querySelectorAll("#"+this.id+" a."+this.class);
		for(var i=0;i<a.length;i++){
			this.a[i]={'src':a[i].href,'title':a[i].title};
			a[i].href="javascript:Gallery.objects['"+this.id+"'].open("+i+")";
		}
	}
	this.id=id||"gallery";
	this.class="img";
	this.nom=0;
	this.a=[];
	this.tpl='<div class="dialog" id="{id}"><a onclick="Dialog.objects[\'{id}\'].close()" class="dialog-close"></a><a onmousedown="dnd(event,\'#{id}\')" class="dialog-move"></a><div class="dialog-title">{title}</div><div class="dialog-data"><a class="dialog-next" href="javascript:Gallery.objects[\''+this.id+'\'].next(1)"></a><a class="dialog-prev" href="javascript:Gallery.objects[\''+this.id+'\'].next(-1)"></a>{data}</div><div class="dialog-caption">{caption}</div></div>';
	return Gallery.objects[this.id]=this;
}
Gallery.objects=[];
function gallery(id,n){
	var d=new Gallery(id);
	if(n!=undefined)d.class=n;
	d.init();
}