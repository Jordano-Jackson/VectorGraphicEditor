//canvasWrap id를 갖는 html div에서 호출함. 현재 선택된 그리기 도구(tool)에 따라 서로 다른 함수(createRect, createCircle, createText, createLine)를 호출합니다.
var elementCounter = 1; // Element IDs 초기화

function createObject(obj){
    if (tool == 'fill') 
    {
        fill(obj);
    } else if (tool == 'rect') 
    {
        createRect();
    } else if (tool == 'circle') 
    {
        createCircle();
    } else if (tool == 'text') {
        createText();
    } else if (tool == 'line') {
        createLine();
    } else if (tool == 'select') {
        selectObject(obj);
    }
}
//Text 버튼을 눌렀을 시, text를 SVG 캔버스에 추가하는 함수입니다.
function createText(){
        var svg = document.getElementById("canvas"); //id=canvas를 변수 svg에 할당.
        var text2 = document.createElementNS("http://www.w3.org/2000/svg", "text"); //새로운 svg를 생성해 text2에 할당
        var textId = "text_" + elementCounter; // Create a unique ID
        text2.setAttribute("id", textId); // Set the ID
        text2.setAttribute("y", document.querySelector("#y").value); //text2의 y속성 설정, y속성은 Y좌표이며 이는 html 문서에서 id="y"인 값이다.
        text2.setAttribute("x", document.querySelector("#x").value);
        var textContent = document.createTextNode(document.querySelector("#textin").value);
        text2.appendChild(textContent);
        svg.appendChild(text2);
        elementCounter++; // Element counter +1
}   
// 원을 SVG 캔버스에 추가하는 함수로, 원의 속성(좌표, 반지름, 색상 등)을 설정합니다.
function createCircle(){
        var svg = document.getElementById("canvas"); // id를 통한 element 할당
        var circle2 = document.createElementNS("http://www.w3.org/2000/svg", "circle"); //새로운 element를 생성해 text2에 할당
        var circleId = "circle_" + elementCounter; // Create a unique ID
        circle2.setAttribute("id", circleId); // Set the ID
        circle2.setAttribute("y", document.querySelector("#y").value);
        circle2.setAttribute("x", document.querySelector("#x").value);
        circle2.setAttribute("cy", document.querySelector("#y").value);
        circle2.setAttribute("cx", document.querySelector("#x").value);
        circle2.setAttribute("stroke", document.querySelector("#stroke").value);
        circle2.setAttribute("stroke-width", document.querySelector("#stSize").value);
        circle2.setAttribute("fill", document.querySelector("#color").value);
        circle2.setAttribute("r", document.querySelector("#r").value);
        circle2.setAttribute("onmousedown", "fill(this);");
        svg.appendChild(circle2); //svg에 추가함
        elementCounter++; // Element counter +1
} 
// 직사각형을 SVG 캔버스에 추가하는 함수로, 직사각형의 속성(좌표, 높이, 너비, 색상 등)을 설정합니다.
function createRect(){
        var svg = document.getElementById("canvas");
        var rect2 = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        var rectId = "rect_" + elementCounter; // Create a unique ID
        rect2.setAttribute("id", rectId); // Set the ID
        // Other attributes setup
        rect2.setAttribute("y", document.querySelector("#y").value);
        rect2.setAttribute("x", document.querySelector("#x").value);
        rect2.setAttribute("height", document.querySelector("#height").value);
        rect2.setAttribute("width", document.querySelector("#width").value);
        rect2.setAttribute("fill", document.querySelector("#color").value);
        rect2.setAttribute("stroke", document.querySelector("#stroke").value);
        rect2.setAttribute("stroke-width", document.querySelector("#stSize").value);
        rect2.setAttribute("onmousedown", "fill(this);");
        svg.appendChild(rect2);
        elementCounter++; // Element counter +1
}
// 선을 SVG 캔버스에 추가하는 함수로, 선의 속성(좌표, 선의 속성 등)을 설정합니다.
function createLine(){
        var svg = document.getElementById("canvas");
        var line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
        var lineId = "line_" + elementCounter; // Create a unique ID
        line2.setAttribute("id", lineId); // Set the ID
        line2.setAttribute("y1", document.querySelector("#y").value);
        line2.setAttribute("x1", document.querySelector("#x").value);
        line2.setAttribute("y2", document.querySelector("#height").value);
        line2.setAttribute("x2", document.querySelector("#width").value);
        line2.setAttribute("stroke", document.querySelector("#stroke").value);
        line2.setAttribute("stroke-width", document.querySelector("#stSize").value);
        line2.setAttribute("onmousedown", "fill(this);");
        svg.appendChild(line2);
        elementCounter++; // Element counter +1
}
// 마우스 클릭 위치를 감지하여 좌표를 입력 폼에 채우는 함수입니다.
function click_in(event){
    pos_x1 = event.offsetX?(event.offsetX):event.pageX-document.getElementById("canvas").offsetLeft;
    pos_y1 = event.offsetY?(event.offsetY):event.pageY-document.getElementById("canvas").offsetTop;
    document.querySelector("#x").value = pos_x1;
    document.querySelector("#y").value = pos_y1;
}
// 마우스 클릭 해제 위치를 감지하여 그리기 도구에 따라 추가 속성을 설정하는 함수입니다.
function click_out(event){
    pos_x2 = event.offsetX?(event.offsetX):event.pageX-document.getElementById("canvas").offsetLeft;
    pos_y2 = event.offsetY?(event.offsetY):event.pageY-document.getElementById("canvas").offsetTop;
    if (tool == "rect") {
    if (pos_x2 >= document.querySelector("#x").value) {
        document.querySelector("#width").value = pos_x2 - document.querySelector("#x").value;
        document.querySelector("#height").value = pos_y2 - document.querySelector("#y").value;
    } else {
        return false;
    }
} else if (tool == "circle") {
    document.querySelector("#r").value = pos_y2 - document.querySelector("#y").value;
} else if (tool == "line") {
    document.querySelector("#y").value = pos_y1;
    document.querySelector("#x").value = pos_x1;
    document.querySelector("#height").value = pos_y2;
    document.querySelector("#width").value = pos_x2;
}
}
//Element의 색상을 채우는 함수로, onmousedown 이벤트에서 호출되며 주로 createObejcet에서 생성된다.
function fill(obj) {
    if (tool == 'fill') {
    obj.style.fill = document.querySelector('#color').value;
    obj.style.stroke = document.querySelector('#stroke').value;
}}
// 그리기 도구(tool)를 변경하는 함수로, 텍스트 입력 도구를 선택하는 경우 텍스트 입력란을 활성화합니다.
function swTool(tooln) {
    tool = tooln;
    if (tool == "text") {
        document.querySelector('#textin').style.display="block";
    } else {
        document.querySelector('#textin').style.display="none";
    }
}

function selectObject(obj) {
    if (tool == 'select') {
    obj.style.fill = document.querySelector('#color').value;
    obj.style.stroke = document.querySelector('#stroke').value;
}}