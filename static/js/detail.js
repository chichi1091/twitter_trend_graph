$(function(){
    $.ajax({
        url:'/dashboards/api/trends/' + day,
        type:'GET',
        data:{}
    }).done((data) => {
        // Ajaxリクエストが成功した時発動
        bubbleChart(data);
    }).fail((data) => {
        // Ajaxリクエストが失敗した時発動
        console.log(data);
    }).always((data) => {
        // Ajaxリクエストが成功・失敗どちらでも発動
    });
});

function bubbleChart(data_set) {
    var width=1200, height=600;
    var bubble = d3.pack().size([width, height]).padding(1.5);

    var nodes = d3.hierarchy( data_set ).sum(function(d){ return d.val });

    var bubble_data = bubble(nodes).descendants();

    var no_root_bubble = bubble_data.filter( function(d){ return d.parent != null ;} );

    var max_val = d3.max(no_root_bubble, function(d){ return d.r ;});
    var min_val = d3.min(no_root_bubble, function(d){return d.r ; });

    var color_scale = d3.scaleLinear().domain( [min_val, max_val] ).range(d3.schemeCategory10 );
    var font_scale = d3.scaleLinear().domain([min_val, max_val]).range([9, 28]);

    var bubbles = d3.select("#bubble_chart")
        .selectAll(".bubble")
        .data(no_root_bubble)
        .enter()
        .append("g")
        .attr("class", "bubble")
        .attr("transform", function(d){ return "translate("+d.x+","+d.y+")" ;});

    bubbles.append("circle")
        .attr("r", function(d){ return d.r })
        .style("fill", function(d,i){
            return color_scale(d.r);
        });

    bubbles.append("text")
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "central")
        .text(function(d){ return d.data.name ; })
        .style("font-size", function(d){ return font_scale(d.r) ; });
}
