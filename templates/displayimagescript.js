var dataImage = localStorage.getItem('imgData');
var outputImg = document.getElementById('output-image');
outputImg.src = "data:image/png;base64," + dataImage;
