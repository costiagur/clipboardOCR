myfunc = new Object();

//*********************************************************************************** */
myfunc.submit = function(){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');

    fdata.append("brighten_in",document.getElementById("brighten_in").value);

    fdata.append("enlarge_in",document.getElementById("enlarge_in").value);

    fdata.append("rollangle_in",document.getElementById("rollangle_in").value);

    fdata.append("lang_in",document.getElementById("lang_in").value);

    xhr.open('POST',"http://localhost:"+ui.port,true)

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            //console.log(this.responseText)

            resobj = JSON.parse(this.responseText);

            if(resobj[0] == 'Error'){
                alert(resobj[1])
            }
            else if(resobj[0] == 'success'){
                document.getElementById("res_txt").value = resobj[1];

                const hebregex = /[א-ת]/g;

                if(hebregex.test(resobj[1])){ //if includes hebrew text, align test to right
                    document.getElementById("res_txt").style.textAlign="right";
                    canvas.style.float = "right";
                }
                else{
                    document.getElementById("res_txt").style.textAlign="left";
                    canvas.style.float = "none";
                }

                var resimg = new Image();
  
                resimg.onload = function() {
                    ctx.drawImage(resimg, 0, 0, canvas.width,resimg.naturalHeight * canvas.width/resimg.naturalWidth);
                };

                resimg.src = 'data:img/jpeg;base64,' + resobj[2];

            }

        }
    }

    xhr.send(fdata);     
}


//********************************************************************************************* */
myfunc.download = function(filename, filetext){

    var a = document.createElement("a");

    document.body.appendChild(a);

    a.style = "display: none";

    a.href = 'data:application/octet-stream;base64,' + filetext;

    a.download = filename;

    a.click();

    document.body.removeChild(a);

}
