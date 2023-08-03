const width = 650;
const height = 300;
const marginTop = 30;
const marginRight = 30;
const marginBottom = 30;
const marginLeft = 30;

for(let index = 0; index < datasets.length; index++){
    datasets[index]["date"] = new Date(datasets[index]["date"])
}
console.log(datasets)


const x = d3.scaleTime()
    .range([0, width])
    .domain(d3.extent(datasets, d => d.date));
const y = d3.scaleLinear()
    .range([height,0])
    .domain([d3.min(datasets, d => d.value), d3.max(datasets, d => d.value)]);

const svg = d3.select("#stockChart")
    .append("svg")
        .attr("width", width + marginRight + marginLeft)
        .attr("height", height + marginTop + marginBottom)
    .append("g")
        .attr("transform", `translate(${marginLeft}, ${marginRight})`);


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
    .call(d3.axisLeft(y)
        .ticks(5)
    )
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
const line = d3.line()
    .x(d => x(d.date))
    .y(d => y(d.value));

svg.append("path")
    .datum(datasets)
    .attr("fill", "none")
    .attr("stroke", "#adb5bd")
    .attr("stroke-width", 1)
    .attr("d", line);

