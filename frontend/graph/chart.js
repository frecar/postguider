function draw_like_time_chart(){
	var maxLikes = d3.max(data, function(d) { return d[1]; });


    var margin = {top: 20, right: 15, bottom: 60, left: 35}
      , width = document.getElementById('omgbox-plot').offsetWidth - margin.left - margin.right
      , height =  200;

    var x = d3.scale.linear()
              .domain([0, 1440])
              .range([ 0, width ]);

    var y = d3.scale.linear()
    	      .domain([0, maxLikes])
    	      .range([ height, 0 ]);
    var chart = d3.select('#omgbox-plot')
	.append('svg:svg')
	.attr('width', width + margin.right + margin.left)
	.attr('height', height + margin.top + margin.bottom)
	.attr('class', 'chart')

    var main = chart.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
	.attr('width', width)
	.attr('height', height)
	.attr('class', 'main')

    // draw the x axis
    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.tickValues(d3.range(0, 1440, 120))
	.tickFormat(function(d, i){
	if(Math.ceil(d/60) < 10){
		return "0" + Math.ceil(d/60) + ":00";
	} else {
		return Math.ceil(d/60) + ":00";
	}});

    main.append('g')
	.attr('transform', 'translate(0,' + height + ')')
	.attr('class', 'main axis date')
	.call(xAxis);
	
	main.append('text')
	.attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width)
    .attr("y", height - 6)
    .text("time");

    // draw the y axis
    var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left')
	.ticks(5);

    main.append('g')
	.attr('transform', 'translate(0,0)')
	.attr('class', 'main axis date')
	.call(yAxis);
	
	main.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", 6)
    .attr("dy", ".75em")
    .attr("transform", "rotate(-90)")
    .text("likes");

    var g = main.append("svg:g");
    
    function setX(d){
    	return x(d[0]);
    }
    
    function setY(d){
    	return y(d[1]);
    }
    
    //Set radius of plot-circles according to number of likes
    function setR(d){
    	return (11*(Math.log(Math.E, 1 + (d[1]+1)/maxLikes) * Math.log(d[1]+1)/Math.LN2) / (1.5*Math.log(maxLikes)));
    }
    
    function setOpacity(d){
    	var bucket_index = Math.ceil(d[0]/60)-1;
    	
    	//bucket_average = 7
    	
    	var bucket = buckets[bucket_index]
    	, prev_bucket = buckets[bucket_index-1]
    	, next_bucket = buckets[bucket_index+1];
    	
    	if(bucket === bucket_average){
    		return 0.5;
    	} else if(bucket < bucket_average){
    		if(prev_bucket > bucket_average && next_bucket > bucket_average){
    			return 0.6;
    		}
    		var diff = bucket_average - bucket;
    		return Math.max(0.15, 0.5 - diff/bucket_average);
    	} else if(bucket > bucket_average){
    		var diff = bucket - bucket_average;
    		return Math.min(0.5 + diff/bucket_average, 0.8);
    	}
    }
    
    var tooltip = d3.select('#omgbox-plot').append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

    
    function mouseoverEvent(d){
    	d3.select(this)
    	.style("fill", "rgb(174,185,191)")
        .style("opacity", 0.8)
        
        tooltip.transition()
        .duration(50)
        .style("opacity", .9);
        
        var hour = Math.floor(d[0]/60);
    	var minutes = (d[0] - hour*60)%60;
    	var timestring = "";
    	
    	if(hour < 10){
    		timestring = timestring + "0";
    	}
    	
    	timestring = timestring + hour.toString() + ":";
    	
    	if(minutes < 10){
    		timestring = timestring + "0";
    	}
    	
    	timestring = timestring + minutes.toString();
        
        tooltip.html(timestring
        + "<br>" + d[1] + " likes")
        .style("left", (d3.select(this).attr("cx")+ 100) + "px")
  		.style("top", (d3.select(this).attr("cy")) + "px");
    }
    
    function mouseoutEvent(d){
    	d3.select(this)
    	.style("fill", "rgb(158,208,240)")
    	.style("opacity", setOpacity);
    	
    	tooltip.transition()
    	.duration(50)
    	.style("opacity", 0);
    }

    g.selectAll("scatter-dots")
      .data(data)
      .enter().append("svg:circle")
          .attr("cx", setX )
          .attr("cy", setY )
          .attr("r", setR )
          .attr("stroke", "rgb(107,146,166)")
          .style("opacity", setOpacity)
          .on("mouseover", mouseoverEvent)
    	  .on("mouseout", mouseoutEvent);
}