// type 0 - neutral; before question answered, type 1 - correct; half green chart, type 2 - wrong; half red chart
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

for(let index = 0; index < data.length; index++){
    data[index]["date"] = new Date(data[index]["date"])
}
for(let index = 0; index < data.length; index++){
    updatedData[index]["date"] = new Date(updatedData[index]["date"])
}
console.log(data)

var x = d3.scaleTime([d3.min(data, d => d.date), d3.max(data, d => d.date)], [0, width])
var y = d3.scaleLinear([0, 300], [height,0]);
// x axis
svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .style("font-size", "12px")
    .call(d3.axisBottom(x)
        .ticks(d3.timeDay.every(8))
        .tickFormat(d3.timeFormat("%b %d")))
    .selectAll(".tick line")
    .style("stroke", "#6c757d");
    
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
svg.selectAll("horizontalLines")
    .data(y.ticks().slice(1))
    .join("line")
    .attr("y1", d => y(d))
    .attr("y2", d => y(d))
    .attr("x1", 0)
    .attr("x2", width)
    .attr("stroke", "#6c757d")
    .attr("stroke-width", 0.5);

// area
var area = d3.area()
    .x(d => x(d.date))
    .y0(height)
    .y1(d => y(d.value));

var line = d3.line()
    .x(d => x(d.date))
    .y(d => y(d.value));

function drawChart(){
    areaChart = svg.append("path")
        .data([data])
        .attr("fill", "#adb5bd")
        .style("opacity", 0.6)
        .attr("d", area);
    lineChart = svg.append("path")
        .data([data])
        .attr("fill", "none")
        .attr("stroke", "#adb5bd")
        .attr("stroke-width", 1)
        .attr("d", line);
}
function removeChart(){
    d3.selectAll("path").remove()
}
function updateChart(){
    console.log(updatedData)
    areaChart = svg.append("path")
        .data([updatedData])
        .attr("fill", "#adb5bd")
        .style("opacity", 0.6)
        .attr("d", area);
    lineChart = svg.append("path")
        .data([updatedData])
        .attr("fill", "none")
        .attr("stroke", "#adb5bd")
        .attr("stroke-width", 1)
        .attr("d", line);
    
}
// function answered() {
//     var button1 = document.getElementById('button1');
//     var button2 = document.getElementById('button2');
//     var button3 = document.getElementById('button3');
//     console.log("clicked")
//     if (changePrice < 0){
//         button1.classList.replace("buttonUnanswered", "buttonWrong");
//         button2.classList.replace("buttonUnanswered", "buttonWrong");
//         button3.classList.replace("buttonUnanswered", "buttonCorrect");
//         console.log("third")
//     }
//     else if (changePrice < 0.04 && changePrice > 0){
//         button1.classList.replace("buttonUnanswered", "buttonWrong");
//         button2.classList.replace("buttonUnanswered", "buttonCorrect");
//         button3.classList.replace("buttonUnanswered", "buttonWrong");
//         console.log("second")
//     }
//     else {
//         button1.classList.replace("buttonUnanswered", "buttonCorrect");
//         button2.classList.replace("buttonUnanswered", "buttonWrong");
//         button3.classList.replace("buttonUnanswered", "buttonWrong");
//         console.log("first")
//     }
//     document.querySelector('#button1').disabled = true;
//     document.querySelector('#button2').disabled = true;
//     document.querySelector('#button3').disabled = true;
//     removeChart();
//     updatedChart();
// }
