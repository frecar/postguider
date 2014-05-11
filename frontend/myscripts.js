/**
 * Created by guillaume on 5/10/14.
 */


var semaphor = false;
var keypressedrecently = false;
var previoustextareavalue = "";
var data = [];
var buckets = [];
var bucket_average = 0;

function graph()
{
    var token = localStorage.getItem('postguider');
    plot_div = window.document.getElementById("omgbox-plot");
    plot_div.innerHTML = "<title>Like Analysis Graph</title><style>.chart {}.main text {font: 10px sans-serif;}.axis line, .axis path {shape-rendering: crispEdges;stroke: black;fill: none;}circle {fill: rgb(158,208,240);}div.tooltip {position: absolute;text-align: center;width: 60px;height: 28px;padding: 2px;font: 12px sans-serif;background: white;border: 0px;border-radius: 3px;pointer-events: none;}</style><div class='content'></div> ";
    $.getJSON( "http://luna.frecar.no/graph/"+token+ "/", function( dat ) {
           console.log(dat);
           data = dat["plot"];
           buckets = dat["buckets"];
           bucket_average = dat["average"];
           draw_like_time_chart();
    });

}
go();
upgrade();

$("body").on("click", function(){upgrade();});

function upgrade()
{
    var textfield_to_monitor_B = window.document.getElementsByTagName("textarea");
    var score = 0;

    var textfield_to_monitor = textfield_to_monitor_B[0];
    var container_textfield_to_monitor = window.document.getElementById("pagelet_composer");
    if(container_textfield_to_monitor == null)
    {
        container_textfield_to_monitor = window.document.getElementsByClassName("timelineUnitContainer fbTimelineComposerUnit")[0];
        container_textfield_to_monitor.style.margin = "10px;"
    }
    var div_box = window.document.createElement("div");
    var div_box_text = window.document.createElement("p");
    div_box.appendChild(div_box_text);
    div_box.className = "_4-u2 mbm ";
    div_box.style.backgroundColor = "#FFFFFF";
    div_box.style.padding = "10px";
    div_box.id = "omgbox";
    textfield_to_monitor.onkeydown = function()
    {
            if(window.document.getElementById("omgbox") == null)
            {
                container_textfield_to_monitor.appendChild(div_box);
            }
            keypressedrecently = true;

            check_if_needed();

    };
    $("body").on("click", function(){upgrade();});
}

var timer_is_running = false;
function check_if_needed()
{
    if((keypressedrecently == false)&&(previoustextareavalue != window.document.getElementsByTagName("textarea")[0].value))
    {
        keypressedrecently = true;
        updatedata();
        previoustextareavalue = window.document.getElementsByTagName("textarea")[0].value;
    }
    else if((timer_is_running == false)&&(keypressedrecently == true))
    {
        timer_is_running = true;
        setInterval("need_update_motherfucker()",2000);
    }
}



function need_update_motherfucker() {
    timer_is_running = false;
    keypressedrecently = false;
    check_if_needed();
}

function updatedata(){
        var textfield_to_monitor_B = window.document.getElementsByTagName("textarea");
        var score = 0;
        var textfield_to_monitor = textfield_to_monitor_B[0];
        var container_textfield_to_monitor = window.document.getElementById("pagelet_composer");
        if(container_textfield_to_monitor == null)
        {
            container_textfield_to_monitor = window.document.getElementsByClassName("timelineUnitContainer fbTimelineComposerUnit")[0];
        }
        var token = localStorage.getItem('postguider');
        $.getJSON( "http://luna.frecar.no/analyze_post/"+token+"/" + textfield_to_monitor.value, function( data ) {
               semaphor = true;
               score = 0;
               div_box = window.document.getElementById("omgbox");

               var text = "<h5>PostGuider</h5><br><hr>";
               if(data["text_score"] != undefined)
               {
                score = data["text_score"];
                console.log(score);
                text += "<h6>Quality</h6><br>";
                var quality = "";
                if(score<0.20)
                {
                    quality = "<span style='color:#97CD1A; font-size:20px;'>You can do better</span>";

                }
                   else if(score>0.5)
                {
                    quality = "<span style='color:yellowgreen; font-size:20px'>Excellent</span>";
                }
                else
                {
                    quality = "<span style='color:green; font-size:20px'>Promising</span>";
                }
                text += "The quality of this post is : " +  quality + " <br><hr>";
               }
               text += "<h6>Time analysis</h6><br>";
               if(data["post_now"] != undefined){
                   if(data["hours_to_wait"]==0)
                   {
                        text += 'Optimal period for posting.<br><div id="yay">details</div>';
                       div_box.style.backgroundColor = "rgb(" + (255-score).toString(10) + ", 255, " + (255-score).toString(10) + ")";
                   } else {
                        text += 'Non optimal period for posting, the optimal period start in : <span style="color:yellowgreen; font-size:20px">' + data["hours_to_wait"] + '  hours.</span><br><div id="yay" style="font-style:italic;"><a href="#">details</a></div>';
                        div_box.style.backgroundColor = "rgb(  255 ," +  (255-score).toString(10) +", " + (255-score).toString(10) + ")";
                   }
                    text += "<div id='omgbox-plot'></div>"
               }
               else
               {
                   div_box.style.backgroundColor = "rgb(" + (255-score).toString(10) + ", 255, " + (255-score).toString(10) + ")";
               }
               if(data["hint"] != undefined)
               {
                   if(data["hint"] == "Building index")
                   {
                    text = "<h5>Magic is happening</h5><br><p>Please be patient, our server are working hard to provide you the best services.</p>";
                    div_box.style.backgroundColor = "rgb(  255 ,250, 205)";
                   } else {
//                    text += "<br> hints :<br>";
//                    text += data["hint"];
                   }
               }
               div_box.innerHTML = text;
               if(window.document.getElementById("yay") != null)
               {
                    window.document.getElementById("yay").addEventListener("click",graph);
               }

              });

}

function go() {
        var match = location.search.match(/\?code=(.*)/);
        var persistent_data = "";
        console.log(match);
        if (match) {
                var code = match[1];
                $.get('https://graph.facebook.com/oauth/access_token?client_id=850183171661993&redirect_uri=http://luna.frecar.no:5002/&client_secret=f8e1d689eabd79a5726acb50d298581a&code=' + code, function (data) {
                        persistent_data = data.substring(data.indexOf("=")+1,data.indexOf("&expires"));
                        localStorage.setItem('postguider', persistent_data);
                })
        }
}
