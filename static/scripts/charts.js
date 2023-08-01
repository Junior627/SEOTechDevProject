const width = 800;
const height = 400;
const marginTop = 40;
const marginRight = 40;
const marginBottom = 40;
const marginLeft = 200;

const datasets = [{ date: new Date("2022-01-01"), value: 200 }, { date: new Date("2022-01-02"), value: 400 }, { date: new Date("2022-01-03"), value: 300 }];
const dataset = [
{ date: new Date("2022-01-01"), value: 200 },
{ date: new Date("2022-02-01"), value: 250 },
{ date: new Date("2022-03-01"), value: 180 },
{ date: new Date("2022-04-01"), value: 300 },
{ date: new Date("2022-05-01"), value: 280 },
{ date: new Date("2022-06-01"), value: 220 },
{ date: new Date("2022-07-01"), value: 300 },
{ date: new Date("2022-08-01"), value: 450 },
{ date: new Date("2022-09-01"), value: 280 },
{ date: new Date("2022-10-01"), value: 600 },
{ date: new Date("2022-11-01"), value: 780 },
{ date: new Date("2022-12-01"), value: 320 }
];
const x = d3.scaleTime()
    .range([0, width])
    .domain(d3.extent(dataset, d => d.date));
const y = d3.scaleLinear()
    .range([height,0])
    .domain([0, d3.max(dataset, d => d.value)]);

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
    .attr("fill", "none")
    .attr("stroke", "white")
    .attr("stroke-width", 1)
    .attr("d", line);

