const canvas = document.getElementById('canvas-container');
const ctx = canvas.getContext('2d');
const brushSizeRange = document.getElementById('brush-size-range');
const slider = document.getElementById('slider-value');
const predictButton = document.getElementById('predict-button');
const clearButton = document.getElementById('clear-button');
const modelSelect = document.getElementById('model-select');

let brushSize = 10;
let selectedModel = 0;
setBrushSize();
changeModel();

brushSizeRange.addEventListener('input', function() {
    brushSize = parseInt(this.value);
    setBrushSize();
});

modelSelect.addEventListener('change', function() {
    selectedModel = parseInt(this.value);
    console.log(this.value);
    changeModel();
});

function changeModel() {
    if (selectedModel === 0) {
        canvas.width = 1000;
    } else {
        canvas.width = 350;
    }
}

function setBrushSize() {
    slider.innerHTML = "Value: " + brushSize;
}


let isDrawing = false;
let lastX, lastY;

canvas.addEventListener('mousedown', function(e) {
    isDrawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
});

canvas.addEventListener('mousemove', function(e) {
    if (isDrawing) {
        ctx.beginPath();
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'white';
        ctx.lineWidth = brushSize;
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        lastX = e.offsetX;
        lastY = e.offsetY;
    }
});

canvas.addEventListener('mouseup', function() {
    isDrawing = false;
});

predictButton.addEventListener('click', function() {
    
});

clearButton.addEventListener('click', function() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});