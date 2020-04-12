function make_graph(data,id,cmap,fill_area=true){
  var m = [40, 40, 40, 80]; // margins
  var w = d3.select(id).node().offsetWidth - m[1] - m[3]; // width
  var h = 400 - m[0] - m[2]; // height

  // X scale will fit all values from data[] within pixels 0-w
  var x = d3.scaleLinear().domain([0, data[0].length]).range([0, w]);
  // Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
  var y = d3.scaleLinear().domain([0, 1.2*Math.max(...data[0])]).range([h, 0]);

  var line = d3.line()
    .x(function(d,i) {
      return x(i);
    })
    .y(function(d) {
      return y(d);
    })

    var area = d3.area()
        .x(function(d, i) { console.log(`Domain: ${d}`); return x(i); })
        .y0(function(d) { return y(d.source); })
        .y1(function(d) { return y(d.target); });

    // Add an SVG element with the desired dimensions and margin.
    var graph = d3.select(id).append("svg:svg");
    graph
          .append("rect")
          .attr("width", "100%")
          .attr("height", h + m[0] + m[2])
          .attr("class", "bg");
    graph = graph
          .attr("width", "100%")
          .attr("height", h + m[0] + m[2])
          .append("svg:g")
          .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    //Axis-------------------------------------------------------------
    var xAxis = d3.axisBottom(x).tickFormat(function(d){ return d.x;});
    var yAxisLeft = d3.axisLeft(y);

    graph.append("svg:g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + h + ")")
          .call(xAxis);

    graph.append("svg:g")
          .attr("class", "y axis")
          .attr("transform", "translate(-25,0)")
          .call(yAxisLeft);
    //-----------------------------------------------------------------
    var L = data.length;
    //Stacked----------------------------------------------------------
    var stacked = Array(L);
    for (let i = 0; i<L; i++){
      var data_transpose = Array(data[i].length)
      for (let j=0; j<data[i].length; j++){
        if (i>0){
          data_transpose[j] = {"source":data[i-1][j], "target":data[i][j]};
        }else{
          data_transpose[j] = {"source": 0, "target": data[i][j]}
        }
      }
      stacked[i] = data_transpose
    }


    //-----------------------------------------------------------------
    //Drawing----------------------------------------------------------
    for (let i = 0; i<L; i++){
      graph.append("svg:path")
            .datum(data[i])
            .attr("d", line)
            .attr("class", "line")
            .style("stroke", cmap[i]);

      if(fill_area){
        console.log(stacked[i])
        graph.append("path")
              .datum(stacked[i])
              .attr("class", "area")
              .attr("d", area)
              .style("stroke", "none")
              .style("fill", cmap[i]);
      }
    }
    //-----------------------------------------------------------------
}
