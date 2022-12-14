checkFontCookie()
function setCookie(cname,cvalue) {
    document.cookie = cname+"="+cvalue+";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i=0; i<ca.length; i++)
      {
      let c = ca[i].trim();
      if (c.indexOf(name)===0) return c.substring(name.length,c.length);
      }
    return "";
}

function checkFontCookie() {
    document.getElementById("top-div").style.fontSize = getCookie("font-size");
    selectImplementedOption();
}

let changeFontStyle = function (font) {
    document.getElementById("top-div").style.fontSize = font.value;
    setCookie("font-size", font.value);
}

function selectImplementedOption() {
    let optionFromCookies = getCookie("font-size");
    let listToSelectFrom = document.getElementById('input-font');

    for(let option, option_index = 0; option = listToSelectFrom.options[option_index]; option_index++) {
        if(option.value === optionFromCookies) {
            listToSelectFrom.selectedIndex = option_index;
            break;
        }
    }
}