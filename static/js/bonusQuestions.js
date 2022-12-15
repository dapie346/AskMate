// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    let currentTheme = document.documentElement.getAttribute("data-theme");
    let switchToTheme = currentTheme === "light-to-dark" ? "dark-to-light" : "light-to-dark";
    document.documentElement.setAttribute("data-theme", switchToTheme);
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