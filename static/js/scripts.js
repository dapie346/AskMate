checkFontCookie()
function setCookie(cname,cvalue)
{
    document.cookie = cname+"="+cvalue+";path=/";
}

function getCookie(cname)
{
let name = cname + "=";
let ca = document.cookie.split(';');
for(let i=0; i<ca.length; i++)
  {
  let c = ca[i].trim();
  if (c.indexOf(name)==0) return c.substring(name.length,c.length);
  }
return "";
}

function checkFontCookie()
{
    document.getElementById("top-div").style.fontSize = getCookie("font-size");
}

let changeFontStyle = function (font) {
    document.getElementById("top-div").style.fontSize = font.value;
    setCookie("font-size", font.value);
}