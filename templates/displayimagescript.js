var loadFile = function (event) {
    var file = document.getElementById('output');
    file.src = URL.createObjectURL(event.target.files[0]);
};