function randomHero() {
  heros = [makeLissajous, makeLorenz, makeDots];
  var hero = heros[Math.floor(Math.random() * heros.length)];
  hero();
}

function makeLissajous() {
  // Sizing
  var width = window.innerWidth;
  var height = window.innerHeight * 0.975;

  window.onresize = function () {
    width = window.innerWidth;
    height = window.innerHeight * 0.975;
  };

  var svg = d3.select("#hero").style("background", "black");

  // Color
  svg
    .append("linearGradient")
    .attr("id", "line-gradient")
    .selectAll("stop")
    .data([
      { offset: "0%", color: "#b2182b" },
      { offset: "100%", color: "#2166ac" },
    ])
    .enter()
    .append("stop")
    .attr("offset", function (d) {
      return d.offset;
    })
    .attr("stop-color", function (d) {
      return d.color;
    });

  var line = d3
    .line()
    .curve(d3.curveCardinal)
    .x((d) => d[0])
    .y((d) => d[1]);

  var track = svg.append("path").attr("stroke-width", 8);

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
      interval.stop();
    }
    phi = omega * t;
    draw(
      (currentX = width / 2 + (width / 2) * Math.cos(a * phi)),
      (currentY = height / 2 + (height / 2) * Math.sin(b * phi))
    );
  }

  interval = d3.interval(lissajous, 30);
}

function makeLorenz() {
  // Sizing
  var width = window.innerWidth;
  var height = window.innerHeight * 0.975;

  window.onresize = function () {
    width = window.innerWidth;
    height = window.innerHeight * 0.975;
  };

  var svg = d3.select("#hero").style("background", "black");

  // Color
  svg
    .append("linearGradient")
    .attr("id", "line-gradient")
    .selectAll("stop")
    .data([
      { offset: "20%", color: "#b2182b" },
      { offset: "80%", color: "#2166ac" },
    ])
    .enter()
    .append("stop")
    .attr("offset", function (d) {
      return d.offset;
    })
    .attr("stop-color", function (d) {
      return d.color;
    });

  var track = svg.append("path").attr("stroke-width", 8);

  var line = d3
    .line()
    .curve(d3.curveCardinal)
    .x((d) => d[0])
    .y((d) => d[1]);

  var rho = 2 * 28.0,
    sigma = 10.0,
    beta = 8.0 / 3.0,
    x = 0,
    y = (z = 1),
    t = 0.01,
    data = [];

  function draw(x, y, z) {
    data.push([width / 2 + 30 * x, (3 / 2) * height + 17 * -z]);
    track.attr("d", line(data)).attr("stroke", "url(#line-gradient)");
  }

  function lorentz() {
    draw(
      (x += t * (sigma * (y - x))),
      (y += t * (x * (rho - z) - y)),
      (z += t * (x * y - beta * z))
    );
  }

  interval = d3.interval(lorentz, 30);
}

function makeDots() {
  // Sizing
  var width = window.innerWidth;
  var height = window.innerHeight * 0.975;
  const numberBlueDots = Math.round((width * height) / 1000);
  const growthRate = 0.01;
  const initialBlueDotSpeed = 3;
  const wallRepulsionDistance = 100;
  const escapeThreshold = 100;
  let maxDistance = Math.sqrt(width * width + height * height) * 0.75;
  let colorScale = d3
    .scalePow()
    .domain([0, maxDistance])
    .range(["white", "black"]);

  window.onresize = function () {
    width = window.innerWidth;
    height = window.innerHeight * 0.975;
  };

  var svg = d3.select("#hero").style("background", "black");

  // Initialize red dot
  let redDot = { x: width / 2, y: height / 2, r: 20, speed: 3.5 };

  // Initialize blue dots
  let blueDots = d3.range(numberBlueDots).map(() => {
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      r: 15,
      speed: initialBlueDotSpeed,
    };
  });

  // Redraw function
  function redraw() {
    // Update red dot
    let red = svg.selectAll(".red-dot").data([redDot]);
    red
      .enter()
      .append("circle")
      .attr("class", "red-dot")
      .merge(red)
      .attr("r", (d) => d.r)
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y)
      .attr("fill", "#ff410d");

    // Update blue dots
    let blue = svg.selectAll(".blue-dot").data(blueDots);
    blue
      .enter()
      .append("circle")
      .attr("class", "blue-dot")
      .merge(blue)
      .attr("r", (d) => d.r)
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y)
      .attr("fill", (d) => {
        let distance = Math.hypot(redDot.x - d.x, redDot.y - d.y);
        return colorScale(distance);
      });
    blue.exit().remove();
  }

  // Game loop
  d3.timer(() => {
    // Initialize Quadtree
    let quadtree = d3
      .quadtree()
      .x((d) => d.x)
      .y((d) => d.y)
      .addAll(blueDots);

    // Move blue dots
    blueDots.forEach((dot, i) => {
      let dx = 0,
        dy = 0;

      // Calculate distance from red dot
      let rx = dot.x - redDot.x;
      let ry = dot.y - redDot.y;
      let redDist = Math.hypot(rx, ry);

      // If the blue dot is close to the red dot, it runs away
      if (redDist < escapeThreshold + redDot.r) {
        dx += (rx / redDist) * dot.speed;
        dy += (ry / redDist) * dot.speed;
      }

      // Calculate repulsion from other blue dots using the Quadtree
      quadtree.visit((node, x1, y1, x2, y2) => {
        if (!node.length) {
          // This node is a leaf
          let otherDot = node.data;

          if (dot !== otherDot) {
            // Don't compare a dot to itself
            let odx = dot.x - otherDot.x;
            let ody = dot.y - otherDot.y;
            let distToOther = Math.hypot(odx, ody);

            if (distToOther < dot.r + otherDot.r && distToOther > 0) {
              // If dots are overlapping and we're not dividing by zero
              dx +=
                ((dot.r + otherDot.r - distToOther) * odx) / distToOther / 3;
              dy +=
                ((dot.r + otherDot.r - distToOther) * ody) / distToOther / 3;
            }
          }
        }

        // Return false to continue visiting nodes; if true is returned, the traversal of this branch will stop
        return (
          x1 > dot.x + dot.r ||
          x2 + dot.r < dot.x - dot.r ||
          y1 > dot.y + dot.r ||
          y2 + dot.r < dot.y - dot.r
        );
      });

      // Calculate repulsion from walls
      if (dot.x < wallRepulsionDistance)
        dx += (wallRepulsionDistance - dot.x) / wallRepulsionDistance;
      if (dot.y < wallRepulsionDistance)
        dy += (wallRepulsionDistance - dot.y) / wallRepulsionDistance;
      if (dot.x > width - wallRepulsionDistance)
        dx -= (dot.x - width + wallRepulsionDistance) / wallRepulsionDistance;
      if (dot.y > height - wallRepulsionDistance)
        dy -= (dot.y - height + wallRepulsionDistance) / wallRepulsionDistance;

      // Update position
      dot.x = Math.min(Math.max(dot.x + dx, dot.r), width - dot.r);
      dot.y = Math.min(Math.max(dot.y + dy, dot.r), height - dot.r);

      // Update Quadtree
      quadtree.remove(dot);
      quadtree.add(dot);
    });

    // Move red dot towards closest blue dot
    if (blueDots.length > 0) {
      let closestDot = blueDots.reduce((prev, curr) => {
        let d1 = Math.hypot(redDot.x - prev.x, redDot.y - prev.y);
        let d2 = Math.hypot(redDot.x - curr.x, redDot.y - curr.y);
        return d1 < d2 ? prev : curr;
      });
      let dx = closestDot.x - redDot.x;
      let dy = closestDot.y - redDot.y;
      let dist = Math.hypot(dx, dy);
      redDot.x += (dx / dist) * redDot.speed;
      redDot.y += (dy / dist) * redDot.speed;
    }

    // Check for collisions
    blueDots = blueDots.filter((dot) => {
      if (Math.hypot(redDot.x - dot.x, redDot.y - dot.y) < redDot.r + dot.r) {
        redDot.r += dot.r * growthRate; // The red dot grows
        redDot.speed = redDot.speed * 0.999; // The red dot grows
        return false; // Remove the blue dot
      } else {
        return true;
      }
    });

    // Redraw
    redraw();

    // Check for end of game
    if (blueDots.length === 0) {
      return;
    }
  });
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
