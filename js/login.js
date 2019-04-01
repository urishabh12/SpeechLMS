function checkFocus() {
  $("#username").focus(function() {
    name = "username";
    speech = new p5.Speech();
    speech.setVoice("Google हिन्दी");
    speech.speak(name);
    document.body.onkeyup = function(e) {
      if (e.keyCode == 17) {
        let speechRec = new p5.SpeechRec("Google हिन्दी", gotSpeech);
        speechRec.start();
        console.log(speechRec);
        function gotSpeech() {
          if (speechRec.resultValue) {
            ans = speechRec.resultString;
            ans = ans.replace(/ /g, "");
            document.getElementById("username").value = ans;
          }
        }
      }
    };
  });

  $("#password").focus(function() {
    name = "password";
    speech = new p5.Speech();
    console.log("run");
    speech.setVoice("Google हिन्दी");
    speech.speak(name);
    document.body.onkeyup = function(e) {
      if (e.keyCode == 17) {
        let speechRec = new p5.SpeechRec("Google हिन्दी", gotSpeech);
        speechRec.start();
        console.log(speechRec);
        function gotSpeech() {
          if (speechRec.resultValue) {
            ans = speechRec.resultString;
            ans = ans.replace(/ /g, "");
            document.getElementById("password").value = ans;
          }
        }
      }
    };
  });
}

window.onload = checkFocus;
