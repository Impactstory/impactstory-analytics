// UTILITY FUNCTIONS

function capitalize(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}


// PAGE FUNCTIONS

function load_widget_data(widget, dataUrl) {
    $.ajax({
               url: dataUrl,
               type:"GET",
               success: function(data){
                       widget.create.call(widget, data)
               }
           })
}

// OBJECTS

var SparklineSet = function(container$, options){
    var defaultOptions = {
        iaPrimaryValueLabel:'',
        iaSecondaryValueLabel: "max",
        iaHref: "#",
        maxSpotColor: false,
        minSpotColor: false,
        spotColor: false,
        chartRangeMin:0
    }
    this.options = _.extend(defaultOptions, options)
    this.container$ = container$
    this.init()
}
SparklineSet.prototype = {
    init: function(){
        console.log("init IsaSparkline")
    }
    ,createSparklineBar: function(name, values){
        var defaultOptions = {
            iaPrimaryValue: _.reduce(values, function(memo, num) { return memo + num}),
            iaSecondaryValue: _.max(values),
            tooltipFomatter: function(sparkline, options, fields) {
                return "still working on it..."
            },
            type:"bar",
            iaName: name,
            barWidth: 2
        }
        var options = _.extend(defaultOptions, this.options)
        this.renderSparkline(name, values, options)

    }
    ,createSparklineLine: function(name, xValues, yValues){
        var weekDays = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
        var defaultOptions = {
            iaPrimaryValue: _.last(yValues),
            iaSecondaryValue: _.max(yValues),
            iaName: name,
            type:"line",
            xvalues: xValues,
            tooltipFormatter:function(sparkline, options, fields){
                var d = new Date(fields.x * 1000)
                var mins = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes()
                var dateStr = weekDays[d.getDay()] + ' ' + d.getHours() + ':' + mins
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var options = _.extend(defaultOptions, this.options)
        this.renderSparkline(name, yValues, options)

    }
    ,renderSparkline: function(name, values, options) {
        var elem$ = ich.sparklineWithNumbers(options)
        this.container$.find("div.container").append(elem$)
        this.container$.find(".sparkline."+name).sparkline(values, options)
    }
}




// PROCEDURAL CODE
$(document).ready(function(){

    _.each(widgetNames, function(name){
        var widget = new window[capitalize(name)]()
        var dataUrl = "/widget_data/"+name
        load_widget_data(widget, dataUrl)
    })

})