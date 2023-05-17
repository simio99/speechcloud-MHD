// JavaScript Document

// Make an HTTP request to the URL of the webpage
fetch('https://idos.idnes.cz/plzen/spojeni/vysledky/?f=Technick%C3%A1&fc=307003&t=Ko%C5%A1utka&tc=307003', {
  method: "GET",
  /*headers: {
    "origin": "sulis31.zcu.cz"
  }*/
})
  .then(response => response.text()) // Convert the response to a text string
  .then(html => {
    // Parse the HTML response using the DOMParser API
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');

    // Select the tbody element using querySelector
    const tbody = doc.querySelector('table');

    // Extract the HTML content inside the tbody
    const tbodyContent = tbody.innerHTML;

    const tabuleElement = document.getElementById('.left departures-table');
    tabuleElement.innerHTML = tbodyContent;
    console.log(tbodyContent);
  })
  .catch(error => {
    // Handle any errors that occur during the HTTP request
    console.error(error);
  });
  
// Create a new XMLHttpRequest object
/*var xhr = new XMLHttpRequest();

// Set the HTTP method and URL
xhr.open('GET', 'https://idos.idnes.cz/plzen/odjezdy/vysledky/?f=Technick%C3%A1&fc=307003');

// Set the response type to text
xhr.responseType = 'text';

// Set a callback function to run when the request is complete
xhr.onload = function() {
  // Check if the request was successful
  if (xhr.status === 200) {
    // Get the webpage content from the response text and assign it to a variable
    var webpageContent = xhr.responseText;
    
    // Use the webpageContent variable as needed
    console.log(webpageContent);
  }
};

// Send the request
xhr.send();*/

var jizdnirad = [];
jizdnirad[0] = [];
jizdnirad[1] = [];
jizdnirad[2] = [];
jizdnirad[3] = [];
jizdnirad[4] = [37,53];
jizdnirad[5] = [03, 09, 19, 28, 36, 44, 52];
jizdnirad[6] = [00, 08, 16, 24, 34, 41, 49, 58];
jizdnirad[7] = [07, 13, 19, 25, 31, 37, 43, 49, 53];
jizdnirad[8] = [01, 05, 14, 19, 26, 34, 39, 49, 56];
jizdnirad[9] = [09, 14, 24, 34, 44, 54];
jizdnirad[10] = [04, 14, 24, 34, 44, 54];
jizdnirad[11] = [04, 14, 24, 34, 44, 54];
jizdnirad[12] = [04, 14, 19, 24, 29, 34, 39, 44, 49];
jizdnirad[13] = [01, 09, 13, 21, 29, 33, 37, 41, 47];
jizdnirad[14] = [05, 10, 15, 20, 25, 30, 39, 48, 57];
jizdnirad[15] = [06, 15, 24, 34, 43, 52];
jizdnirad[16] = [01, 10, 16, 25, 29, 37, 45, 53];
jizdnirad[17] = [00, 08, 16, 24, 32, 40, 49, 59];
jizdnirad[18] = [09, 14, 23, 32, 42, 52];
jizdnirad[19] = [02, 12, 22, 32, 40, 48, 58];
jizdnirad[20] = [08, 26, 46];
jizdnirad[21] = [06, 26, 46, 56];
jizdnirad[22] = [06, 16, 21, 26, 38];
jizdnirad[23] = [08, 38];

window.onload = function() {
    var odjezd1 = document.getElementById("odjezd1");
    var odjezd2 = document.getElementById("odjezd2");
    var odjezd3 = document.getElementById("odjezd3");
    var odjezd4 = document.getElementById("odjezd4");
    var odjezd5 = document.getElementById("odjezd5");

    let today = new Date();
    let hodiny = today.getHours();
    let minuty = today.getMinutes();
    let minuty_dec = minuty;
    if (minuty<10) {
        minuty_dec = "0"+minuty;
    }
    let time = hodiny + ":" + minuty_dec;
    document.getElementById("aktcas").innerHTML ="Aktuální čas: "+time;
    
    const nejblizsiOdjezdy_first = jizdnirad[hodiny].filter(element => Number.isInteger(element) && element > minuty);
    for (let i = 0; i < nejblizsiOdjezdy_first.length; i++) {
        let tmp = nejblizsiOdjezdy_first[i]
        if (tmp<10) {
            tmp2 = tmp;
            tmp = "0"+tmp2;
        }
        nejblizsiOdjezdy_first[i] = hodiny+":"+tmp;
    }
    console.log(nejblizsiOdjezdy_first);
    
    const nejblizsiOdjezdy_second = jizdnirad[hodiny+1];
    for (let i = 0; i < nejblizsiOdjezdy_second.length; i++) {
        let tmp = nejblizsiOdjezdy_second[i]
        if (tmp<10) {
            tmp2 = tmp;
            tmp = "0"+tmp2;
        }
        nejblizsiOdjezdy_second[i] = (hodiny+1)+":"+tmp;
    }
    console.log(nejblizsiOdjezdy_second);
    
    nejblizsiOdjezdy = nejblizsiOdjezdy_first.concat(nejblizsiOdjezdy_second);
    
    odjezd1.innerHTML = nejblizsiOdjezdy[0];
    odjezd2.innerHTML = nejblizsiOdjezdy[1];
    odjezd3.innerHTML = nejblizsiOdjezdy[2];
    odjezd4.innerHTML = nejblizsiOdjezdy[3];
    odjezd5.innerHTML = nejblizsiOdjezdy[4];
    

    /*const nejblizsiOdjezdy_sec = jizdnirad[hodiny+1];
    
    const nejblizsiOdjezdy = nejblizsiOdjezdy_first.concat(nejblizsiOdjezdy_sec);
    console.log(nejblizsiOdjezdy);
    
    for(i = 0, i<*/
    
    
    
}
//let aktCas = document.getElementById("cas");
//aktCas.innerHTML = "ahoj";

vyhledavaciPole = document.querySelector("#process_text_input");
vyhledavaciTlacitko = document.querySelector("#process_text");

function changeImage() {
    var img = document.getElementById("send_message_empty");
    puvodniObrazek = img.src;
    img.src = "img/mic-recog.svg";
  }
  
function restoreImage() {
    var img = document.getElementById("send_message_empty");
    img.src = "img/mic-passive.svg";
  }

// SIP session, tj. hovor
var session;

// Výchozí URI, odkud se stáhne konfigurace ASR+TTS
//var SPEECHCLOUD_URI = "https://"+window.location.host.replace("444", "443")+"/v1/speechcloud/";
var SPEECHCLOUD_URI = "https://cak.zcu.cz:9443/v1/speechcloud/edu/bp/simio";
//var SPEECHCLOUD_URI = "https://cak.zcu.cz:9443/v1/speechcloud/edu_dialog_start/simio";
//var SPEECHCLOUD_DEFAULT_APP_ID = "numbers";
var SPEECHCLOUD_DEFAULT_APP_ID = "";

// Proměnná pro udržení odkazu na řídící WebSocket
var SPEECHCLOUD_WS = null;

/* Výběr prvků z pole */
function choose(choices) {
  var index = Math.floor(Math.random() * choices.length); return choices[index];
}

/* Logovací funkce */
function hlog(text) {
    $("#log").prepend("<div>"+text+"<br/></div>");
}


$( document ).ready(function() {

    /* Obsluha tlačítka barge-in*/
    $("#tts_stop").click(do_tts_stop);

    $("#slu_set_nbest_2").click(function () {
        speechCloud.slu_set_nbest({nbest: 2});
    });

    $("#slu_set_nbest_10").click(function () {
        speechCloud.slu_set_nbest({nbest: 10});
    });
    
    $("#slu_test").click(function () {
        speechCloud.slu_set_grammars(
            {"grammars": [
                {"entity":"ALT", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/ALT.abnf"},
                {"entity":"CMD", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/CMD.abnf"},
                {"entity":"CS","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/CS.abnf"},
                {"entity":"FL","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FL.abnf"},
                {"entity":"FR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FR.abnf"},
                {"entity":"HE","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/HE.abnf"},
                {"entity":"PO","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/PO.abnf"},
                {"entity":"QNH","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/QNH.abnf"},
                {"entity":"RA","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/RA.abnf"},
                {"entity":"SP","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SP.abnf"},
                {"entity":"SQ","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SQ.abnf"},
                {"entity":"TU","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TU.abnf"},
                {"entity":"TWR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TWR.abnf"}
            ]});
    });

    $("#grm_test").click(function () {
        speechCloud.itblp_gen_grammar({"se_type": "CS", "values": ["MTL572", "CSA024", "OKRHH", "AUA123"]});
    });

    $("#asr_set_grammar").click(function () {
        var grammar = "#ESGF V1.0;\n" +
"grammar prikaz;\n" +
"public <prikaz>=(zatoč <smer>|jeď <kam>|<vypln>)*;\n" +
"<smer>=(doleva|doprava);\n" +
"<kam>=(rovně|dopředu|dozadu);\n" +
"<vypln>=(a|potom);\n";
        speechCloud.asr_set_grammar({"grammar_type": "esgf", "grammar": grammar});
    });


    $("#asr_test").click(function () {
        speechCloud.asr_test({"words": ["Air_Prague", "Prague_Air"]});
    });

    $("#process_text").click(function () {
        text = $("#process_text_input").val();
        speechCloud.asr_process_text({text: text});
        $("#process_text_input").val("")
    });

    $("#send_message").click(function () {
        data = JSON.parse($("#send_message_input").val());
        speechCloud.dm_send_message({data: data});
        $("#send_message_input").val("")
    });

    $("#send_message_empty").click(function () {
        data = {};
        speechCloud.dm_send_message({data: data});
    });
    
    $(document).keypress(function (event) {
        if (event.which === 32) {
        data = {};
        speechCloud.dm_send_message({data: data});
        console.log("Prave byl stisknut mezernik.");
        }
    });


    $("#tts_text").click(function () {
        text = $("#process_text_input").val();
        do_tts(text);
        $("#process_text_input").val("")
    });


    var ignore_space = false;

    $("#process_text_input").focus(function () {
        console.log("ignore_space = true");
        ignore_space = true;
    });

    $("#process_text_input").focusout(function () {
        console.log("ignore_space = false");
        ignore_space = false;
    });

    $("#send_message_input").focus(function () {
        console.log("ignore_space = true");
        ignore_space = true;
    });

    $("send_message_input").focusout(function () {
        console.log("ignore_space = false");
        ignore_space = false;
    });



    /* Stavová proměnná a funkce pro spuštění/pozastavení rozpoznávání */
    var recognizing = false;

    function do_recognize() {
        if (!recognizing) {
            speechCloud.asr_recognize();
            recognizing = true;
            hlog("<i><small>ASR start</small></i>")
        };
    }

    function do_pause() {
        if (recognizing) {
            speechCloud.asr_pause();
            recognizing = false;
            hlog("<i><small>ASR stop</small></i>")
        }
    }

    /* Přerušení syntézy zasláním zprávy tts_stop */
    function do_tts_stop() {
        console.log("Sending tts_stop");
        speechCloud.tts_stop();
    }

    /* Syntéza řeči */
    function do_tts(text, voice) {
        speechCloud.tts_synthesize({
            text: text,
            voice: voice
        });
        if (text == "Žádný příkaz nerozpoznán") {
            vyhledavaciPole.style.visibility = 'visible';
            vyhledavaciTlacitko.style.visibility = 'visible';
            }
    }

    /* Obsluha tlačítka Restart dialog */
    $("#dialog_restart").click(function () {
        location.reload(true);
    });

    /* Obsluha tlačítka Stop dialog*/
    $("#dialog_stop").click(function () {
        hlog("<b>Dialog ukončen na žádost uživatele</b>");
        speechCloud.terminate();
    });

    /* Obsluha tlačítka Recognition start/stop */
    $("#recog").click(function () {
        if (recognizing) {
            do_pause();
        } else {
            do_recognize();
        };
    });


    /* Po stisk mezerníku je totéž jako stisknutí tlačítka #recog */
    $(window).keydown(function(evt) {
        if (ignore_space) return;

        if (evt.keyCode == 32) {
            evt.preventDefault();
        };
    });

    $(window).keyup(function(evt) {
        if (ignore_space) return;

        if (evt.keyCode == 32) {
            //setTimeout(function () {$("#recog").click()}, 100);
            $("#send_message_empty").click();
            
            evt.preventDefault();
        };
    });


    $("#file-input").change(function (e) {
        var file = e.target.files[0];
        if (!file) {
            return;
        }

        speechCloud.asr_offline_start();

        var reader = new FileReader();

        CHUNK_SIZE = 100*1024;
        start = 0;

        // Closure to capture the file information.
        reader.onloadend = function(evt) {
            if (evt.target.readyState == FileReader.DONE) {
                var result = evt.target.result;
                n_bytes = result.length;
                hlog("<b>Sending "+n_bytes+" bytes from "+file.name+"</b>");
                speechCloud.asr_offline_push_data({data: result});

                load_next()
            }
        }

        function load_next() {
            if (start < file.size) {
                var blob = file.slice(start, start+CHUNK_SIZE);
                reader.readAsBinaryString(blob);
                start += CHUNK_SIZE;
            } else {
                speechCloud.asr_offline_stop();
            };
        };

        load_next()
    });


    /* Proměnná, do které se uloží timeout pro SIP zavolání */
    var call_timeout = null;

    /* Model URI je SPEECHCLOUD_URI a parametr z location.search */
    if (location.search.length > 0) {
        model_uri = SPEECHCLOUD_URI + location.search.substring(1);
    } else {
        model_uri = SPEECHCLOUD_URI + SPEECHCLOUD_DEFAULT_APP_ID;
    }

    var options = {
        uri: model_uri,
        tts: "#audioout",
        disable_audio_processing: true
    }

    var speechCloud = new SpeechCloud(options);

    window.speechCloud = speechCloud

    speechCloud.on('error_init', function (data) {
        console.error('error.init event handler', data.status, data.text);
    });

    speechCloud.on('error_ws_initialized', function () {
        hlog('[WS] - ERROR: WS already initialized.');
    });

    speechCloud.on('_ws_connected', function () {
        hlog('[WS] - connected');
    });

    speechCloud.on('_ws_close', function () {
        hlog('[WS] - closed');
    });

    speechCloud.on('_ws_session', function (data) {
        hlog('[WS] - session started id=' + data.id);
    });

    speechCloud.on('_sip_closed', function (data) {
        hlog('[SIP] - closed');
    });

    speechCloud.on('_sip_initializing', function (data) {
        hlog('[SIP] - client id=' + data);
    });

    speechCloud.on('_sip_registered', function () {
        hlog('[SIP] - registered');
    }); 

    /* Při příchodu asr_ready (ASR připraveno) */
    speechCloud.on('asr_ready', function () {
        hlog("<b>ASR připraveno</b>");
        document.getElementById("send_message_empty").disabled = false;
        document.getElementById("send_message_empty").src = "img/mic-passive.svg";
        document.getElementById("instrukce").innerHTML = "Chcete-li mluvit, stiskněte tlačítko mikrofonu.";
    });

    /* Při příchodu požadavku na zobrazení z dialog manageru*/
    speechCloud.on('dm_display', function (msg) {
        hlog("<b>"+msg.text+"</b>");
        console.log("dm_display", msg);

    });

    /* Při příchodu dat z dialog manageru*/
    speechCloud.on('dm_receive_message', function (msg) {
        data = JSON.stringify(msg.data, null, 2);
        hlog("<b>dm_receive_message:</b><br><pre>"+data+"</pre>");
        console.log("dm_receive_message:", msg.data);

    });

    /* Při příchodu ASR výsledku */
    speechCloud.on('asr_result', function (msg) {
        if (msg.partial_result) {
            return;
        }
        hlog(msg.result);
        console.log("Result", msg);

        /* zastavíme TTS */
        // do_tts_stop();

        // tts_result = msg.result.replace(/\[[^ ]+\]/g, ' ');

        // /* sesyntetizujeme odpověď */
        // engine = 'BDL';
        // ssml = "<?xml version='1.0' encoding='UTF-8'?>\n<speak version='1.0'> \n \n  <noise name='plane_jet3' type='continuous' subtype='plane' fVolume='1.00'/> \n  <noise name='radioswitch1' type='instant' subtype='switch' fVolume='0.5' /> \n  \n <noise name='signal_drop' type='random' subtype='drop' start='0' end='-1' iDropMinLen='100' iDropMaxLen='200' fVolMin='0.20' fVolMax='0.50' iWaitMin='2000' iWaitMax='7000'/> \n  <noise name='radioswitch1' type='instant' subtype='switch' fVolume='0.5'/> \n \n  <voice engine='"+engine+"'> \n    <prosody rate='+40%' pitch='-0%' fVolume='+40%'> \n      <s>"+tts_result+"</s> \n    </prosody> \n  </voice> \n</speak>";
        // do_tts(ssml);
    });

    /* Při skončení TTS */
    speechCloud.on('tts_done', function () {
        /*hlog("<i>TTS finished</i>");*/
    });

    /* Při příchodu sémantických entit ze SLU */
    speechCloud.on('slu_nbest', function (msg) {
        html = "<table><tr><th>n</th><th>prob</th><th>hyp</th></tr>";
        $(msg.nbest).each(function(index, hyp) {
            prob = hyp.prob.toFixed(3);
            html += "<tr><td>"+(index+1)+"</td><td>"+prob+"</td><td>"+hyp.hyp+"</td></tr>";
        });
        html += "</table>";
        hlog(html);
        console.log(msg.nbest);
    });

    /* Při příchodu sémantických entit ze SLU */
    speechCloud.on('slu_entities', function (msg) {
        //html = "<table><tr><th>n</th><th>prob</th><th>entities</th></tr>";
        html="";
        $(msg.entities).each(function(index, hyp) {
            prob = hyp.prob.toFixed(3);
            str = hyp.values.join(', ');
            //html += "<tr><td>"+(index+1)+"</td><td>"+prob+"</td><td>"+str+"</td></tr>";
            html = "Entity: "+str;
        });
        //html += "</table>";
        hlog(html);
        console.log("slu_entities: ", msg);
    })

    speechCloud.on('asr_audio_record', function (msg) {
        /*hlog("<b>ASR audio</b> <a href='"+ msg.uri +"' target='_blank'>" + msg.id + "</a>, tstamp="+msg.tstamp);*/
        document.getElementById("send_message_empty").src = "img/mic-passive.svg";
    });

    speechCloud.on('sc_start_session', function (msg) {
        /*hlog("<b>Session started</b> <a href='"+ msg.session_uri +"?format=yaml.html' target='_blank'>" + msg.session_id + "</a>");
        hlog("<b>JSON schema URI</b> <a href='"+ msg.schema_uri +"?format=docson' target='_blank'>" + msg.schema_uri + "</a>");
        hlog("<b>SpeechCloud model URI</b> <a href='"+ model_uri +"' target='_blank'>" + model_uri + "</a>");*/

        console.log(msg.schema);

        /*hlog('[LIB] - Methods: ' + this.availableMethods().join(', '));
        hlog('[LIB] - Events: ' + this.availableEvents().join(', '));*/
    });

    speechCloud.on('sc_error', function (msg) {
        hlog("<b>Error</b> in method <b>"+msg.method_name+"</b> <br>" + msg.error);
        console.log(msg);
    });

    speechCloud.on('itblp_gen_grammar_result', function (msg) {
        hlog("<b>Generated grammar of type </b> " + msg.se_type + "<pre>"+msg.grammar+"</pre>");

        speechCloud.slu_set_grammars(
            {"grammars": [
                {"entity":"ALT", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/ALT.abnf"},
                {"entity":"CMD", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/CMD.abnf"},
                {"entity":"CS","type":"abnf-inline","data":msg.grammar},
                {"entity":"FL","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FL.abnf"},
                {"entity":"FR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FR.abnf"},
                {"entity":"HE","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/HE.abnf"},
                {"entity":"PO","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/PO.abnf"},
                {"entity":"QNH","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/QNH.abnf"},
                {"entity":"RA","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/RA.abnf"},
                {"entity":"SP","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SP.abnf"},
                {"entity":"SQ","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SQ.abnf"},
                {"entity":"TU","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TU.abnf"},
                {"entity":"TWR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TWR.abnf"}
            ]});
    });

    speechCloud.on("asr_offline_started", function (msg) {
        hlog("<i><small>ASR start / offline</small></i>")
    });

    speechCloud.on("asr_offline_finished", function (msg) {
        hlog("<i><small>ASR stop / offline</small></i>")
    });

    speechCloud.on("asr_offline_error", function (msg) {
        hlog("<i><small>ASR error / offline</small></i>")
    });
    
    speechCloud.on("asr_signal", function (msg) {
        document.getElementById("instrukce").innerHTML = "Mluvte...";
        document.getElementById("send_message_empty").src = "img/mic-active.svg";
        if (msg.speech == true) {
            document.getElementById("send_message_empty").src = "img/mic-recog1.svg";
            setTimeout(() => {  document.getElementById("send_message_empty").src = "img/mic-recog2.svg"; }, 500);
            setTimeout(() => {  document.getElementById("send_message_empty").src = "img/mic-recog3.svg"; }, 500);        
            /*setTimeout(() => {}, 500);*/
        }
        else {
            //restoreImage();
        }
        if (msg.finished == true) {
            /*document.getElementById("send_message_empty").src = "img/mic-active.svg";*/
            restoreImage();
            document.getElementById("instrukce").innerHTML = "Chcete-li mluvit, stiskněte tlačítko mikrofonu.";
        }
    });
    
    speechCloud.on("tts_started", function (msg) {
        document.getElementById("send_message_empty").src = "img/mic-passive.svg";
    });



    speechCloud.init();

});
