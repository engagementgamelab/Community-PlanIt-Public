var windowX;
var windowY;

$(document).ready(function() {
    console.log("Readdy");
    windowX = $(window).width();
    windowY = $(window).height();
    $("body").append("<p id='load'>loading...</p>");
    $("#load").css({
        position: 'absolute',
        width: '150px',
        color:'#333',
        top: windowY/2,
        left: windowX/2
    });

    $("#gender").change(function(){
        var v = $("#gender option:selected").val();
        var p5 = Processing.getInstanceById('viz'); 
        p5.selectGender(v);
        setDes();
    });
    $("#age").change(function(){
        var v = $("#age option:selected").val();
        var p5 = Processing.getInstanceById('viz'); 
        p5.selectAge(v);
        setDes();

    });
    $("#race").change(function(){
        var v = $("#race option:selected").val();
        var p5 = Processing.getInstanceById('viz'); 
        p5.selectRace(v);
        setDes();
    });
    $("#income").change(function(){
        var v = $("#income option:selected").val();
        var p5 = Processing.getInstanceById('viz'); 
        p5.selectIncome(v);
        setDes();
    });
    $("#stake").change(function(){
        var v = $("#stake option:selected").val();
        var p5 = Processing.getInstanceById('viz'); 
        p5.selectStake(v);
        setDes();
    });

    $("#reset").click(function(e){
        e.preventDefault();
        $("#gender").val("-1");
        $("#age").val("-1");
        $("#race").val("-1");
        $("#income").val("-1");
        $("#stake").val("-1");
        var p5 = Processing.getInstanceById('viz'); 
        p5.resetAll();
        setDes();

    });
    $('input').click(function (){
        var p5 = Processing.getInstanceById('viz'); 
        var thischeck = $(this);
        if (thischeck.is (':checked')){
            p5.toggleLurkers(1);
            console.log("show");
        }
        else{
            p5.toggleLurkers(0);
            console.log("hide");
        }
        setDes();
    });
    // var canvasRef = document.createElement('canvas');
    // var p = Processing.loadSketchFromSources(canvasRef, ['js/viz.pde']);
    // $('body').append(canvasRef);
    console.log("Reset");
    resetCanvas();


});
function setDes(){
    var filt = false;
    var des = "";
    var g = $("#gender option:selected").text();
    if(g!="All"){
        filt = true;
        des = des+"("+g+")  ";
    }
    var a = $("#age option:selected").text();
    if(a!="All"){
        filt = true;
        des = des+"("+a+")  ";
    }
    var r = $("#race option:selected").text();
    if(r!="All"){
        filt = true;
        des = des+"("+r+")  ";
    }
    var i = $("#income option:selected").text();
    if(i!="All"){
        filt = true;
        des = des+"("+i+")  ";
    }
    var s = $("#stake option:selected").text();
    if(s!="All"){
        filt = true;
        des = des+"("+s+")  ";
    }
    var thischeck = $("input");
       
    if(!filt){
        des="All Users";
    }
     if (thischeck.is (':checked')){
            des = des+" (including lurkers)";
        }
        else{
            des = des+" (excluding lurkers)";
        }
    console.log(des);
    $("#description").text(des);

}

$(window).resize(function(){
    resetCanvas();
});

function resetCanvas(){
    console.log("doing");
    // $("canvas").attr("id","viz");
    windowX = $(window).width();
    windowY = $(window).height();
    console.log(windowX);
    var offset = (windowX-1024)/2;

    console.log("off: "+offset);
    $("#detroitTitle").css({
        left:windowX/2-64
    });
    $("canvas").css({
        left: offset,
        position:"absolute",
        'z-index':'998',
        top:"100px",
        outline:"none"
    });
    
    
}
