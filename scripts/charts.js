import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

const width = 100;
const height = 100;
const marginTop = 20;
const marginRight = 20;
const marginBottom = 20;
const marginLeft = 20;

const x = d3.scaleTime()
    .range([0, width])
    .domain(d3.extent(dataset, d => d.date));
const y = d3.scaleLinear()
    .range([height,0])
    domain([0, d3.max(dataset, d => d.value)]);

const svg = d3.select("#stockChart")
    .append("svg")
        .attr("width", width + marginRight + marginLeft)
        .attr("height", height + marginTop + marginBottom)
    .append("g")
        .attr("transform", 'translate($(marginLeft), $(marginRight))');

const dataset = [];

// x axis
svg.append("g")
    .attr("transform", 'translate(0,${height})')
    .call(d3.axisBottom(x)
        .ticks(d3.timeMonth.every(1))
        .tickFormat(d3.timeFormat("%b %Y")));

// y axis

svg.append("g")
    .call(d3.axisLeft(y))

const line = d3.line()
    .x(d => x(d.date))
    .y(d => y(d.value));

svg.append("path")
    .datum(dataset)
    .attr("d", line);
