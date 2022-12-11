function randomColorGenerator() {
    var color = "#";
    var letters = "0123456789ABCDEF";

    for(var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)]
    }
    console.log(color)
    return color;

}

function changeColor(cssTag) {
    doc = document.querySelector(cssTag)
    doc.style.color = randomColorGenerator();
}

setInterval("changeColor('h1')", 500);