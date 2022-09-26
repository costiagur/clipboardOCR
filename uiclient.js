ui = new Object();

ui.port = 50000

//********************************************************************************** */
window.addEventListener('beforeunload',function(event){ //when closing browser, close python
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("request",'close'); //prepare files

    xhr.open('POST',"http://localhost:"+ui.port, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);
        }
    };
    
    xhr.send(fdata);
    
})
//********************************************************************************** */
window.addEventListener('load',function(event){
    ui.onloadfunc()
})
//******************************************************************************************** */

ui.onloadfunc = function(){

    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    codeword = document.getElementsByTagName("body")[0].dataset.codeword

    fdata.append("request",codeword); //parol

    xhr.open('POST',"http://localhost:"+ui.port, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);

            res = JSON.parse(xhr.responseText);

            ui.port = res.port;

            if(res.args != null){

                for(key of Object.keys(res.args)){

                    if (document.getElementById(key)){ //if such id doesn't exists, than object will return null which is false
            
                        document.getElementById(key).value = res.args[key];
                    }
                }           
            }
        }
    };
    
    xhr.send(fdata);
}

