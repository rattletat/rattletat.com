function makeLissajous() {
    var width = window.innerWidth * .9;
    var height = window.innerHeight * .9;
    window.onresize = function () {
        width = window.innerWidth * .9;
        height = window.innerHeight *.9;
    };
    var svg = d3.select("#hero");
    var a = 3.2,
        b = 5.9; // Lissajous frequencies
    var phi,
        omega = (2 * Math.PI) / 30000; // 40 seconds per period

    var currentX = width + width * .05,
        currentY = height / 2 + height * .05;
    var previousX = currentX,
        previousY = currentY;

    var start_line = function (t) {
        // Calculate position
        phi = omega * t;
        currentX = width / 2 + (width / 2) * Math.cos(a * phi) + width * .05;
        currentY = height / 2 + (height / 2) * Math.sin(b * phi) + height * .05;

        // Fade out and remove lines that are barely visible
        svg.selectAll("line")
            .each(function () {
                this.bogus_opacity *= 0.97 + 0.03 * Math.random();
            })
            .attr("stroke-opacity", function () {
                return this.bogus_opacity;
            })
            .filter(function () {
                return this.bogus_opacity < 0.005;
            })
            .remove();

        // Add next step line
        line = svg.append("line")
            .each(function () {
                this.bogus_opacity = 1.0;
            })
            .attr("x1", previousX)
            .attr("y1", previousY)
            .attr("x2", currentX)
            .attr("y2", currentY)
            .attr("stroke-width", 10)
            .attr("stroke", "#ff410d");

        line.transition()
            .duration(2000)
            .attr("stroke", "#18cae6")
            .transition()
            .duration(2000)
            .attr("stroke", "green");

        // line.transition()
        //     .duration(4000)
        //     .attr("stroke-width", 0.1 * Math.random() * (currentX + currentY));

        // Exchange start & end point
        previousX = currentX;
        previousY = currentY;

        if (t > 5000e3) {
            timer.stop();
        } // after 120 seconds
    };

    d3.timer(start_line);
    d3.timer(start_line, 1500)
    d3.timer(start_line, 3000)
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
