// type 0 - neutral; before question answered, type 1 - correct; half green chart, type 2 - wrong; half red chart
console.log("Main javascript loaded")

console.log("Hello World from js");
console.log("Main javascript loaded")
const width = 650;
const height = 300;
const marginTop = 30;
const marginRight = 30;
const marginBottom = 30;
const marginLeft = 30;

var svg = d3.select("#stockChart")
.append("svg")
    .attr("width", width + marginRight + marginLeft)
    .attr("height", height + marginTop + marginBottom)
.append("g")
    .attr("transform", `translate(${marginLeft}, ${marginRight})`);


var area, line, horizontalLines;
function drawbasic(data, xSpacing, color){
    for(let index = 0; index < data.length; index++){
        data[index]["date"] = new Date(data[index]["date"])
    }
    console.log(data);
    startDate = d3.min(data, d => d.date);
    endDate =  d3.max(data, d => d.date);
    startValue = d3.min(data, d => d.value);
    endValue =  d3.max(data, d => d.value);
    var x = d3.scaleTime([startDate, endDate], [0, width]);
    var y = d3.scaleLinear([startValue, endValue], [height,0]);
    
    // x axis
    if(xSpacing === "every8"){
        svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .style("font-size", "12px")
        .call(d3.axisBottom(x)
            .ticks(d3.timeDay.every(d3.extent(data, d => d.date)))
            .tickFormat(d3.timeFormat("%b %d")))
        .selectAll(".tick line")
        .style("stroke", "#6c757d");
    }
    if(xSpacing === "every4"){
        svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .style("font-size", "12px")
        .call(d3.axisBottom(x)
            .ticks(d3.timeDay.every(4))
            .tickFormat(d3.timeFormat("%b %d")))
        .selectAll(".tick line")
        .style("stroke", "#6c757d");
    }
    svg.selectAll(".domain")
        .styles({ fill:"none", stroke:"#6c757d",  "stroke-width":"1" });
    // y axis
    svg.append("g")
        .call(d3.axisLeft(y).ticks(5))
        .style("font-size", "12px")
        .call(g => g.select(".domain").remove())
        .selectAll(".tick line")
        .style("stroke-opacity", 0)

    svg.selectAll(".tick text")
        .attr("fill", "#6c757d");
    // grid lines
    horizontalLines = svg.selectAll("gH")
        .data(y.ticks().slice(1))
        .join("line")
        .attr("y1", d => y(d)).attr("y2", d => y(d))
        .attr("x1", 0).attr("x2", width)
        .attr("stroke", "#6c757d")
        .attr("stroke-width", 0.5);
    //gradient 
    if (color === "red")
    {var gradient = svg.append("defs")
    .append("linearGradient")
    .attr("id", "gradient")
    .attr("gradientTransform", "rotate("+90+")")
    gradient.append("stop").attr("offset", "50%").attr("stop-color", "#eeb3a3");
    gradient.append("stop").attr("offset", "80%").attr("stop-color", "grey");}
    if (color === "green")
    {var gradient = svg.append("defs")
    .append("linearGradient")
    .attr("id", "gradient")
    .attr("gradientTransform", "rotate("+90+")")
    gradient.append("stop").attr("offset", "50%").attr("stop-color", "#aeeea3");
    gradient.append("stop").attr("offset", "80%").attr("stop-color", "grey");}
    // area under line
    area = d3.area()
        .x(d => x(d.date))
        .y0(height)
        .y1(d => y(d.value));
    line = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.value));
}
function chart1(){
    drawbasic(data1, "every4", "null");
    areaChart = svg.append("path")
        .data([data1])
        .attr("fill", "#adb5bd")
        .style("opacity", 0.6)
        .attr("d", area);

    lineChart = svg.append("path")
        .data([data1], )
        .attr("fill", "none")
        .attr("stroke", "#adb5bd")
        .attr("stroke-width", 1)
        .attr("d", line);
}
function chart2(color){
    drawbasic(data2, "every8", color)
    if(color === "grey"){
        areaChart = svg.append("path")
            .data([data2])
            .style("opacity", 0.6)
            .attr("d", area)
            .attr("fill", "#adb5bd");
    }
    areaChart = svg.append("path")
        .data([data2])
        .style("opacity", 0.6)
        .attr("d", area)
        .attr("fill",  "url(#gradient)");

    if(color === "grey"){
        lineChart = svg.append("path")
        .data([data2])
        .attr("fill", "none")
        .attr("stroke-width", 1)
        .attr("d", line)
        .attr("stroke", "#a3beee");
    }
    else if(color === "green"){
        lineChart = svg.append("path")
        .data([data2])
        .attr("fill", "none")
        .attr("stroke-width", 1)
        .attr("d", line)
        .attr("stroke", "#aeeea3");
    }
    else{
    lineChart = svg.append("path")
        .data([data2])
        .attr("fill", "none")
        .attr("stroke-width", 1)
        .attr("d", line)
        .attr("stroke", "#eeb3a3");
    }
}
function removeChart(){
    svg.selectAll("path").remove();
    svg.selectAll("g").remove();
    svg.selectAll(".domain").remove();
    horizontalLines.remove();
}

function updateHTMLInfo(){  
    var changeInfo = "" + changePrice + "% Past Month";
    var priceBought = "Price Bought " + closeCurrent + "";

    document.getElementById("mainPrice").innerText = closeFuture;
    document.getElementById("stockDateFuture").innerText = dateFuture;
    document.getElementById("change").innerText = changeInfo;
    document.getElementById("priceBought").innerText = priceBought;
    document.getElementById("closeFuturePrice").innerText = closeFuture;
    document.getElementById("openFuturePrice").innerText = openFuture;
    document.getElementById("highFuturePrice").innerText = highFuture;
    document.getElementById("lowFuturePrice").innerText = lowFuture;
    document.getElementById("volumeFuture").innerText = volumeFuture;
}



function nextButton(){
    var nextButton = document.createElement("button");
    nextButton.setAttribute("type", "button");
    nextButton.setAttribute("class", "btn nextButton")
    nextButton.setAttribute("onclick", "window.location.reload()")
    nextButton.textContent = "Next"
    var nextPosition = document.getElementById('nextButton');
    nextPosition.appendChild(nextButton);
}

chart1();

function answered() {
    var button1 = document.getElementById('button1');
    var button2 = document.getElementById('button2');
    var button3 = document.getElementById('button3');
    console.log("clicked")
    console.log(changePrice)
    document.querySelector('#button1').disabled = true;
    document.querySelector('#button2').disabled = true;
    document.querySelector('#button3').disabled = true;
    removeChart();

    if (changePrice < -50){
        button1.classList.replace("buttonUnanswered", "buttonWrong");
        button2.classList.replace("buttonUnanswered", "buttonWrong");
        button3.classList.replace("buttonUnanswered", "buttonCorrect");
        console.log("third")
        chart2("red");
    }
    else if (changePrice < 40 && changePrice > -50){
        button1.classList.replace("buttonUnanswered", "buttonWrong");
        button2.classList.replace("buttonUnanswered", "buttonCorrect");
        button3.classList.replace("buttonUnanswered", "buttonWrong");
        console.log("second")
        chart2("grey")
    }
    else {
        button1.classList.replace("buttonUnanswered", "buttonCorrect");
        button2.classList.replace("buttonUnanswered", "buttonWrong");
        button3.classList.replace("buttonUnanswered", "buttonWrong");
        console.log("first")
        chart2("green")
    }

    updateHTMLInfo();
    nextButton();
}
