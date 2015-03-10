// pfm.js - JavaScript library for PFM
// Mario R. De Tore, SLAC National Accelerator Laboratory

function getSelectedText(el) {
    if (typeof el.selectionStart == "number") {
        return el.value.slice(el.selectionStart, el.selectionEnd);
    } else if (typeof document.selection != "undefined") {
        var range = document.selection.createRange();
        if (range.parentElement() == el) {
            return range.text;
        }
    }
    return "";
}

function copySelected() {
    var srcTextarea = document.getElementById("converted");
    var destTextarea = document.getElementById("original");
    destTextarea.value = getSelectedText(srcTextarea);
}

function updateChainArgs()
{
	var chain = document.getElementById("chain");
    var args = document.getElementById("args");
    
    current = chain[chain.selectedIndex].text
    if (current.indexOf(" ") > -1)
    {
    	current = current.substring(0,current.indexOf(" "));
    }
    
    chain[chain.selectedIndex].text = current + " " + args.value
    chain[chain.selectedIndex].value = current + " " + args.value
}

function updateArgsBox()
{
	var chain = document.getElementById("chain");
    var args = document.getElementById("args");
    if (chain.value.indexOf(" ") > -1)
    {
    	args.value = chain.value.substring(chain.value.indexOf(" ") + 1);
	}
	else
	{
		args.value = ""
	}
}

function toggleHeader()
{
	footer = document.getElementById("footer");
	row2 = document.getElementById("row2");
	minimize = document.getElementById("minimize");
	info = document.getElementById("alertDiv");
	
	if (row2.style.display != "none")
	{
		row2.style.display = "none";
		footer.style.display = "none";
		minimize.style.display = "none";
		info.style.display = "none";
	}
	else
	{
		row2.style.display = "block";
		footer.style.display = "block";
		minimize.style.display = "block";
    	if (info.innerHTML != "")
    	{
    		info.style.display = "block";
    	}
	}
}

function saveChain()
{
	var xmlhttp;

  	xmlhttp=new XMLHttpRequest();

	var output = "";
	var chain=document.getElementById("chain")
	for (var i=0; i<chain.length; i++){
		output += btoa(chain.options[i].text) + ",";
	}
	output = btoa(output.substring(0,output.length - 1));
	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		alert(document.URL.substring(0,document.URL.indexOf(".py") + 3 ) + xmlhttp.responseText);
    	}
  	}
	xmlhttp.open("GET","pfm.py?savechain=" + output,true);
	xmlhttp.send();
}

function hideInput()
{
	document.getElementById("original").style.display = "none";
	document.getElementById("btnInputHide").style.display = "none";
	document.getElementById("btnInputFile").style.display = "none";
	document.getElementById("btnInputClear").style.display = "none";
	document.getElementById("btnInputShow").style.display = "inline";
}

function showInput()
{
	document.getElementById("original").style.display = "inline";
	document.getElementById("btnInputHide").style.display = "inline";
	document.getElementById("btnInputFile").style.display = "inline";
	document.getElementById("btnInputClear").style.display = "inline";
	document.getElementById("btnInputShow").style.display = "none";
}

function clearInput()
{
	document.getElementById("original").value = "";
	document.getElementById("btnInputFile").value = null
	document.getElementById('original').disabled = false;
}

function moveToInput()
{
	input = document.getElementById("original");
	output = document.getElementById("converted");
	
	input.value = output.value
	output.value = ""
	
	document.getElementById("output").style.display = "none";
	showInput();
	autoGrow(input);
	if (input.clientHeight > 312)
		{
			input.style.height = 298 + "px";
		}
}

function autoGrow (oField) 
{
	if (oField.scrollHeight > oField.clientHeight) {
		oField.style.height = oField.scrollHeight + "px";
	}
}

function toggleText()
{
	converted = document.getElementById("converted");
	info = document.getElementById("alertDiv");
	input = document.getElementById("original");
	output = document.getElementById("output");
	if (converted.value == "")
	{
		output.style.display = "none";
	}
	else {
		output.style.display = "inline";
		input.style.height = "1px";
		autoGrow(input);
		if (input.clientHeight > 312)
		{
			input.style.height = 298 + "px";
		}
		
		autoGrow(document.getElementById("converted"));
		//document.getElementById("input").style.display = "none";
	}

	if (converted.value == "" && input.value != "")
    {
    	alert("Conversion failed! Check input.");
    }
    
    if (info.innerHTML != "")
    {
    	info.style.display = "inline";
    }
}

function checkSize()
{
	chain = document.getElementById("chain");
	if (chain.length == 0){
		chain.style.width = "55px";
	}
	else {
		chain.style.width = "";
	}
}

function selectAll() 
{ 
	chain = document.getElementById("chain");
	chain.multiple = true;
	for (var i = 0; i < chain.length; i++) 
	{ 
		if (chain[i].value == "0"){
			continue;
		}
		else {	
			chain[i].selected = true;
		} 
	} 
}

function moveUp(){
	try {
		var chain = document.getElementById("chain");
		var index = chain.selectedIndex;
		var temp = chain[index - 1].value;
		var temp_txt = chain[index - 1].text;
		chain[index - 1].value = chain[index].value;
		chain[index - 1].text = chain[index].text;
		chain[index].value = temp;
		chain[index].text = temp_txt;
		chain.selectedIndex = index - 1;
	}
	catch(err){}
}

function moveDown(){
	try {
		var chain = document.getElementById("chain");
		var index = chain.selectedIndex;
		var temp = chain[index + 1].value;
		var temp_txt = chain[index + 1].text;
		chain[index + 1].value = chain[index].value;
		chain[index + 1].text = chain[index].text;
		chain[index].value = temp;
		chain[index].text = temp_txt;
		chain.selectedIndex = index + 1;
	}
	catch(err){}
}

function remove_from_chain(){
	try{
		var chain = document.getElementById("chain");
		index = chain.selectedIndex
		chain.remove(index);
		chain.selectedIndex = index - 1;
		checkSize();
	}
	catch(err){}

}

function clearChain(){
	var chain = document.getElementById("chain");
	var length = chain.length;
	for (i = length; i >= 0; i--) { 
    	chain.remove(i);
	}
	checkSize();
}

function AddToChain(head) {
    var dropdown = document.getElementById("select" + head);
    var opt_text = dropdown.options[dropdown.selectedIndex].text
    var chain = document.getElementById("chain");
    var args = document.getElementById("args");
    try {
    	if (chain[0].value == "0"){
    		clearChain();
    	}
    }
    catch(err) {}
    var option = document.createElement("option");
    
    if (args.value == "" && opt_text.indexOf(" *") != -1){
    	popup(dropdown.value);
    	return;
    }
    
    option.text = opt_text.replace(" *", "") + " " + args.value;
    chain.add(option);
    dropdown.selectedIndex = "0";
    args.value = "";
    checkSize();
}

function toggle(div_id) {
	var el = document.getElementById(div_id);
	if ( el.style.display == 'none' ) {	el.style.display = 'block';}
	else {el.style.display = 'none';}
}

function blanket_size() {
	if (typeof window.innerWidth != 'undefined') {
		viewportheight = window.innerHeight;
	} else {
		viewportheight = document.documentElement.clientHeight;
	}
	if ((viewportheight > document.body.parentNode.scrollHeight) && (viewportheight > document.body.parentNode.clientHeight)) {
		blanket_height = viewportheight;
	} else {
		if (document.body.parentNode.clientHeight > document.body.parentNode.scrollHeight) {
			blanket_height = document.body.parentNode.clientHeight;
		} else {
			blanket_height = document.body.parentNode.scrollHeight;
		}
	}
	var blanket = document.getElementById('blanket');
	blanket.style.height = blanket_height + 'px';
}

function popup(text) 
{
	var windowname = document.getElementById('popUpDiv');
	text = text + windowname.innerHTML;
	windowname.innerHTML = text;
	blanket_size();
	toggle('blanket');
	toggle('popUpDiv');
	document.getElementById("popupargs").focus();
	// Bug: user can tab out of popup and interact with the page leading to unexpected
	// input.
}

function closePopup() 
{
	var windowname = document.getElementById("popUpDiv");
	var text = windowname.innerHTML;
	text = text.substring(text.indexOf("<br>"));
	
	
	var dropdown = document.getElementById("selectDo");
	var args = document.getElementById("args");
	args.value = document.getElementById("popupargs").value;
	windowname.innerHTML = text;
	toggle('blanket');
	toggle('popUpDiv');	
	
	if (args.value == ""){
    	alert(dropdown.value);
    	dropdown.selectedIndex = "0";
    	return;
    }
	else {
		AddToChain("Do");
	}	
}

function theTime(gmt) {

	var timefield = document.getElementById("header");
	now=new Date();
	if (gmt) {
		now.setTime(gmt);
	}
	hour=now.getUTCHours();
	min=now.getUTCMinutes();

	if (min<=9) { min="0"+min; }

	timefield.innerHTML = ((hour<=9) ? "0"+hour : hour) + ":" + min + " GMT";

	setTimeout("theTime()", 1000);
}
