function randomHero() {
    // heros = [makeLissajous, makeLorenz]
    heros = [makeLissajous, makeLorenz]
    var hero = heros[Math.floor(Math.random() * heros.length)];
    hero()
}

function makeLissajous() {

    // Sizing
    var width = window.innerWidth;
    var height = window.innerHeight * .975;

    window.onresize = function () {
        width = window.innerWidth;
        height = window.innerHeight * .975;
    };

    var svg = d3.select("#hero").style('background', 'black');

    // Color
    svg.append("linearGradient")
        .attr("id", "line-gradient")
        .selectAll("stop")
        .data([
            {offset: "0%", color: "#b2182b"},
            {offset: "100%", color: "#2166ac"}
        ])
        .enter().append("stop")
        .attr("offset", function (d) {return d.offset;})
        .attr("stop-color", function (d) {return d.color;});

    var line = d3.line()
        .curve(d3.curveCardinal)
        .x(d => d[0])
        .y(d => d[1]);

    var track = svg.append("path")
        .attr("stroke-width", 8);

    var data = [];
    function draw(currentX, currentY) {
        data.push([currentX, currentY]);
        track.attr("d", line(data)).attr("stroke", "url(#line-gradient)");
    }

    // Lissajous
    var a = 3.2,
        b = 5.9,
        t = 0,
        omega = (2 * Math.PI) / 1000;
    function lissajous() {
        t += 5;
        if (2500 <= t && t < 6570) {
            t = 6570;
        } else if (7500 <= t && t < 8200) {
            t = 8440;
        } else if (t >= 10000) {
            interval.stop()
        }
        phi = omega * t;
        draw(
            currentX = width / 2 + (width / 2) * Math.cos(a * phi),
            currentY = height / 2 + (height / 2) * Math.sin(b * phi)
        );
    }

    interval = d3.interval(lissajous, 30);
}

function makeLorenz() {

    // Sizing
    var width = window.innerWidth;
    var height = window.innerHeight * .975;

    window.onresize = function () {
        width = window.innerWidth;
        height = window.innerHeight * .975;
    };

    var svg = d3.select("#hero").style('background', 'black');

    // Color
    svg.append("linearGradient")
        .attr("id", "line-gradient")
        .selectAll("stop")
        .data([
            {offset: "20%", color: "#b2182b"},
            {offset: "80%", color: "#2166ac"}
        ])
        .enter().append("stop")
        .attr("offset", function (d) {return d.offset;})
        .attr("stop-color", function (d) {return d.color;});


    var track = svg.append("path")
        .attr("stroke-width", 8);

    var line = d3.line()
        .curve(d3.curveCardinal)
        .x(d => d[0])
        .y(d => d[1]);


    var rho = 2 * 28.0,
        sigma = 10.0,
        beta = 8.0 / 3.0,
        x = 0,
        y = z = 1,
        t = 0.01,
        data = [];

    function draw(x, y, z) {
        data.push([(width / 2 + 40 * x), (3/2 * height + 15 * -z)]);
        track.attr("d", line(data)).attr("stroke", "url(#line-gradient)");
    }

    function lorentz() {
        draw(
            x += t * (sigma * (y - x)),
            y += t * (x * (rho - z) - y),
            z += t * (x * y - beta * z)
        );
    }

    interval = d3.interval(lorentz, 30);
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
