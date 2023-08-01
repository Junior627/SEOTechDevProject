const width = 650;
const height = 300;
const marginTop = 40;
const marginRight = 40;
const marginBottom = 40;
const marginLeft = 200;

for(let index = 0; index < datasets.length; index++){
    datasets[index]["date"] = new Date(datasets[index]["date"])
}
console.log(datasets)


const x = d3.scaleTime()
    .range([0, width])
    .domain(d3.extent(datasets, d => d.date));
const y = d3.scaleLinear()
    .range([height,0])
    .domain([30, d3.max(datasets, d => d.value)]);

const svg = d3.select("#stockChart")
    .append("svg")
        .attr("width", width + marginRight + marginLeft)
        .attr("height", height + marginTop + marginBottom)
    .append("g")
        .attr("transform", `translate(${marginLeft}, ${marginRight})`);


// x axis
svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x)
        .ticks(d3.timeDay.every(5))
        .tickFormat(d3.timeFormat("%b %d")));

// y axis

svg.append("g")
    .call(d3.axisLeft(y))

const line = d3.line()
    .x(d => x(d.date))
    .y(d => y(d.value));

svg.append("path")
    .datum(datasets)
    .attr("fill", "none")
    .attr("stroke", "white")
    .attr("stroke-width", 1)
    .attr("d", line);

