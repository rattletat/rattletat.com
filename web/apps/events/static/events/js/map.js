function plot_map(data) {
  document.addEventListener("DOMContentLoaded", function (e) {
    const dimensions = {
      width: window.innerWidth,
      height: window.innerHeight,
      margin: {
        top: 50,
        right: 10,
        bottom: 100,
        left: 10,
      },
    };

    // Wrapper
    var wrapper = d3
      .select("#map")
      .append("svg")
      .attr("viewBox", [0, 0, dimensions.width, dimensions.height])
      .classed("svg-content-responsive", true);

    const config = {
      speed: 0.005,
      verticalTilt: -30,
      horizontalTilt: 0,
    };
    let locations = [];
    const markerGroup = wrapper.append("g");
    const projection = d3
      .geoOrthographic()
      .scale(
        Math.min(
          dimensions.width - dimensions.margin.left - dimensions.margin.right,
          dimensions.height - dimensions.margin.top - dimensions.margin.bottom
        ) / 2
      )
      .translate([
        dimensions.margin.left +
          (dimensions.width -
            dimensions.margin.left -
            dimensions.margin.right) /
            2,
        dimensions.margin.top +
          (dimensions.height -
            dimensions.margin.top -
            dimensions.margin.bottom) /
            2,
      ]);
    const initialScale = projection.scale();
    const path = d3.geoPath().projection(projection);
    const center = [dimensions.width / 2, dimensions.height / 2];

    drawGlobe(wrapper);
    drawGraticule(wrapper);
    enableRotation(wrapper);

    function drawGlobe(svg) {
      d3.json(
        "https://gist.githubusercontent.com/mbostock/4090846/raw/d534aba169207548a8a3d670c9c2cc719ff05c47/world-110m.json"
      )
        .then((worldData) => {
          svg
            .selectAll(".segment")
            .data(
              topojson.feature(worldData, worldData.objects.countries).features
            )
            .enter()
            .append("path")
            .attr("class", "segment")
            .attr("d", path)
            .style("stroke", "blue")
            .style("stroke-width", "1px")
            .style("fill", (d, i) => "red")
            .style("opacity", ".6");
          locations = data;
          drawMarkers();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

    function drawGraticule(svg) {
      const graticule = d3.geoGraticule().step([10, 10]);

      svg
        .append("path")
        .datum(graticule)
        .attr("class", "graticule")
        .attr("d", path)
        .style("fill", "green")
        .style("stroke", "yellow");
    }

    function enableRotation(svg) {
      d3.timer(function (elapsed) {
        projection.rotate([
          config.speed * elapsed - 120,
          config.verticalTilt,
          config.horizontalTilt,
        ]);
        svg.selectAll("path").attr("d", path);
        drawMarkers();
      });
    }

    function drawMarkers() {
      const markers = markerGroup.selectAll("circle").data(locations);
      markers
        .enter()
        .append("circle")
        .merge(markers)
        .attr("cx", (d) => projection([d.longitude, d.latitude])[0])
        .attr("cy", (d) => projection([d.longitude, d.latitude])[1])
        .attr("fill", (d) => {
          const coordinate = [d.longitude, d.latitude];
          gdistance = d3.geoDistance(coordinate, projection.invert(center));
          return gdistance > 1.57 ? "none" : "steelblue";
        })
        .attr("r", 7);

      markerGroup.each(function () {
        this.parentNode.appendChild(this);
      });
    }
  });
}

var data = [
  { latitude: 22, longitude: 88 },
  { latitude: 12.61315, longitude: 38.37723 },
  { latitude: -30, longitude: -58 },
  { latitude: -14.270972, longitude: -170.132217 },
  { latitude: 28.033886, longitude: 1.659626 },
  { latitude: 40.463667, longitude: -3.74922 },
  { latitude: 35.907757, longitude: 127.766922 },
  { latitude: 23.634501, longitude: -102.552784 },
];
plot_map(data);
