// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    // console.log(items)
    // console.log(sortField)
    // console.log(sortDirection)

    if (sortDirection === "asc") {
        items.sort(function (a,b){
            if (isNaN(a[sortField]))
                return a[sortField].localeCompare(b[sortField]);
            else
                return parseInt(a[sortField]) - parseInt(b[sortField]);
        });
    } else {
        items.sort(function (a,b){
            if (isNaN(a[sortField]))
                return a[sortField].localeCompare(b[sortField]);
            else
                return parseInt(a[sortField]) - parseInt(b[sortField]);
        }).reverse();
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    if (filterValue[0] === '!'){
        filterValue = filterValue.substring(1);
        if(filterValue.includes('Description:')){
            filterValue = filterValue.split(":").pop();
            items = items.filter(function (obj){
                return !obj.Description.includes(filterValue);})
        }
        else if(filterValue.includes('Title:')){
            filterValue = filterValue.split(":").pop();
            items = items.filter(function (obj){
                return !obj.Title.includes(filterValue);})
        }
        else {
            items = items.filter(function (obj) {
                return !obj.Title.includes(filterValue) && !obj.Description.includes(filterValue);
            })
        }
    }

    else {
        if(filterValue.includes('Description:')){
            filterValue = filterValue.split(":").pop();
            items = items.filter(function (obj){
                return obj.Description.includes(filterValue);})
        }
        else if(filterValue.includes('Title:')){
            filterValue = filterValue.split(":").pop();
            items = items.filter(function (obj){
                return obj.Title.includes(filterValue);})
        }
        else {
            items = items.filter(function (obj) {
                return obj.Title.includes(filterValue) || obj.Description.includes(filterValue);
            })
        }
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
}

function getFontSizes(elements) {
    const sizes = [];
    for (const element of elements) {
        let style = window.getComputedStyle(element, null).getPropertyValue('font-size');
        let fontSize = parseFloat(style);
        sizes.push(fontSize);
        }
    return sizes;
}


function increaseFont() {
    let elements = document.body.querySelectorAll('*');
    let sizes = getFontSizes(elements);
    if (sizes.some(el => el <= 15)) {
        for (const element of elements) {
            let style = window.getComputedStyle(element, null).getPropertyValue('font-size');
            let fontSize = parseFloat(style);
            element.style.fontSize = (fontSize + 1) + 'px';
            }
        }
    console.log("increaseFont");
}

function decreaseFont() {
    let elements = document.body.querySelectorAll('*');
    let sizes = getFontSizes(elements);
    if (sizes.every(el => el >= 3)) {
        for (const element of elements) {
            let style = window.getComputedStyle(element, null).getPropertyValue('font-size');
            let fontSize = parseFloat(style);
            element.style.fontSize = (fontSize - 1) + 'px';
            }
        }
    console.log("decreaseFont");
}