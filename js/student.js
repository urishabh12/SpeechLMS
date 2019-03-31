function readIt() {
  let speech = new p5.Speech();
  speech.setVoice("Google हिन्दी");
  speech.speak("News or Subject");
  $(document).ready(function() {
    $("body").keyup(function(e) {
      if (e.keyCode == 32) {
        let speechRec = new p5.SpeechRec("Google हिन्दी", gotSpeech);
        let speech = new p5.Speech();
        speechRec.start();
        console.log(speechRec);
        console.log("IN");
        function gotSpeech() {
          if (speechRec.resultValue) {
            a = speechRec.resultString;
            a = a.toLowerCase();
            if (a == "news") {
                var news = {{ news|safe }}
                for (var i; i<news.length(); i++){
                    speech.speak(news[i])
                }
            }
          }
        }
      }
    });
  });
}

window.onload = readIt();
