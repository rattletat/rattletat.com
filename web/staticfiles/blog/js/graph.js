function plot_graph(data) {
    document.addEventListener('DOMContentLoaded', function (e) {
        data = JSON.parse(data)


        const dimensions = {
            width: window.innerWidth,
            height: window.innerHeight / 2,
            margin: {
                top: 10,
                right: 10,
                bottom: 10,
                left: 10,
            },
        }

        // Wrapper
        var wrapper = d3.select("#graph")
            .append("svg")
            .attr("viewBox", [0, 0, dimensions.width, dimensions.height])
            .classed("svg-content-responsive", true)

        // Objects
        const post_objects = data.map(post => Object.create({...post, "type": "post"}))
        const tag_objects = data.flatMap(post => post.tags)
            .filter((tag, i, tags) => tags.findIndex(t => (t.url === tag.url)) === i)
            .map(tag => Object.create({...tag, "type": "tag"}));

        const objects = post_objects.concat(tag_objects);
        const links = data.flatMap(post => post.tags.map(tag => Object.create({"source": tag.url, "target": post.url})))

        // Graph elements
        const edges = wrapper.append("g")
            .classed("edges", true)
            .attr("stroke", "black")
            .selectAll("line")
            .data(links)
            .join("line")

        const nodes = wrapper.append("g")
            .classed("nodes", true)

        // Create post rectangles
        const posts = nodes
            .append("g")
            .classed("posts", true)
            .selectAll("circle")
            .data(objects)
            .enter()
            .filter(d => d.type === "post")
            .append("circle")
            .attr("r", "0.8vw")
            .on("click", (_, post) => window.location = post.url)
            .style("cursor", "pointer")

        // Create tag circles
        const tags = nodes
            .append("g")
            .classed("tags", true)
            .selectAll("g")
            .data(objects)
            .enter()
            .filter(d => d.type === "tag")
            .append("g")

        posts
            .append("title")
            .text(d => d.title)

        tags.append("rect")
        tags
            .append("text")
            .attr("text-anchor", "start")
            .attr("fill", "white")
            .attr("font-size", "1.4vw")
            .text(d => d.title)
            .on("click", (_, tag) => window.location = tag.url)
            .style("cursor", "pointer")
            .attr("x", function () {return this.parentNode.getBBox().x - this.parentNode.getBBox().width / 2;})
            .attr("y", function () {return this.parentNode.getBBox().y + this.parentNode.getBBox().height;})

        tags.selectAll("rect")
            .attr("x", function () {return this.parentNode.getBBox().x - 5;})
            .attr("y", function () {return this.parentNode.getBBox().y - 5;})
            .attr("width", function () {return this.parentNode.getBBox().width + 10;})
            .attr("height", function () {return this.parentNode.getBBox().height + 10;})

        window.onresize = function () {
            tags.selectAll("rect")
                .attr("x", function () {return this.parentNode.lastElementChild.getBBox().x - 5;})
                .attr("y", function () {return this.parentNode.lastElementChild.getBBox().y - 5;})
                .attr("width", function () {return this.parentNode.lastElementChild.getBBox().width + 10;})
                .attr("height", function () {return this.parentNode.lastElementChild.getBBox().height + 10;})
        };

        // Simulation
        const centerForceX = d3.forceX(dimensions.width / 2).strength(0.04)
        const centerForceY = d3.forceY(dimensions.height / 2).strength(0.1)
        const centerForce = d3.forceCenter(dimensions.width / 2, dimensions.height / 2);
        const repelForce = d3.forceManyBody().strength(-300)
        const linkForce = d3.forceLink(links).id(d => d.url).distance(100)
        var simulation = d3.forceSimulation(objects)
            .force("linkForce", linkForce)
            .force("repelForce", repelForce)
            .force("center", centerForce)
            .force('centerForceX', centerForceX)
            .force('centerForceY', centerForceY)

        // Drag-Drop
        drag = simulation => {
            function dragstarted(event) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }

            function dragged(event) {
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }

            function dragended(event) {
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }

            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }

        drag(simulation)(tags);
        drag(simulation)(posts);

        // Start simulation
        simulation.on("tick", () => {
            edges
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            tags.attr("transform", d => `translate(${d.x},${d.y})`);
            posts.attr("transform", d => `translate(${d.x},${d.y})`);
        });

    })
}
