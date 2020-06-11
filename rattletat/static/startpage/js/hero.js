function makeLissajous() {
    var width = window.innerWidth;
    var height = window.innerHeight * .975;
    window.onresize = function () {
        width = window.innerWidth;
        height = window.innerHeight * .975;
    };
    var svg = d3.select("#hero");
    var a = 3.2,
        b = 5.9; // Lissajous frequencies
    var phi,
        omega = (2 * Math.PI) / 6000;

    var currentX = width + width * .05,
        currentY = height / 2 + height * .05;
    var previousX = currentX,
        previousY = currentY;

    var start_line = function (t) {
        // Calculate position
        phi = omega * t;
        currentX = width / 2 + (width / 2) * Math.cos(a * phi);
        currentY = height / 2 + (height / 2) * Math.sin(b * phi);

        // Add next step line
        line = svg.append("line")
            .attr("x1", previousX)
            .attr("y1", previousY)
            .attr("x2", currentX)
            .attr("y2", currentY)
            .attr("stroke-width", 20)
            .attr("stroke-opacity", 1)
            .attr("stroke", "white");

        line.transition()
            .duration(300)
            .attr("stroke", "red")
            .transition()
            .duration(12000)
            .attr("stroke-opacity", 0.03)
            .attr("stroke-width", 100)
            .attr("stroke", "blue")
            .remove();

        // Exchange start & end point
        previousX = currentX;
        previousY = currentY;

    };

    d3.interval(start_line, 40);
}

function bounceArrow() {
    var arrow = d3.select("#arrow").select("path");
    repeat();
    function repeat() {
        arrow
            .transition()
            .duration(2000)
            .ease(d3.easeBackInOut)
            .attr("transform", "translate(0," + -1.5 + ")")
            .transition()
            .attr("transform", "translate(0," + 1.5 + ")")
            .on("end", repeat);
    }
}
