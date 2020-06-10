function makeLissajous() {
    var width = window.innerWidth;
    var height = window.innerHeight * .97;
    window.onresize = function () {
        width = window.innerWidth;
        height = window.innerHeight * .97;
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

        // Fade out and remove lines that are barely visible
        // svg.selectAll("line")
        //     // .each(function () {
        //     //     this.bogus_opacity *= 0.99;
        //     // })
        //     // .attr("stroke-opacity", function () {
        //     //     return this.bogus_opacity;
        //     // })
        // .filter(function (d) {
        //     return d.attr("opacity") < 0.7
        // })
        // .remove();

        // Add next step line
        line = svg.append("line")
            // .each(function () {
            //     this.bogus_opacity = 1.0;
            // })
            .attr("x1", previousX)
            .attr("y1", previousY)
            .attr("x2", currentX)
            .attr("y2", currentY)
            .attr("stroke-width", 30)
            .attr("stroke-opacity", 1)
            .attr("stroke", "white");

        line.transition()
            .duration(300)
            .attr("stroke", "red")
            .transition()
            .duration(25000)
            .attr("stroke-opacity", 0.03)
            .attr("stroke-width", 80)
            .attr("stroke", "blue")
            .remove();

        // Exchange start & end point
        previousX = currentX;
        previousY = currentY;

    };

    d3.interval(start_line, 40);
    // d3.timer(start_line, 800);
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
