let speech;
let speechRec;
function setup() {
  noCanvas();
  //Speech-to-Text
  let speechRec = new p5.SpeechRec("Google हिन्दी", gotSpeech);
  //let continous = true;
  //let interim = false;
  //speechRec.start(continous, interim);

  function gotSpeech() {
    if (speechRec.resultValue) {
      createP(speechRec.resultString);
    }
    console.log(speechRec);
  }

  //Text-to-Speech
  speech = new p5.Speech(); // speech synthesis object
  speech.onLoad = voiceReady;

  function voiceReady() {
    console.log("voice ready");
    //console.log(speech.voices);
  }
}

function mousePressed() {
  //console.log(speech.voices);
  // speech.setRate(1);
  // speech.setPitch(3);
  let speechRec = new p5.SpeechRec("en-IN");
  speechRec.start();
  if (speechRec.resultValue) {
    createP(speechRec.resultString);
  }
  console.log(speechRec);
  //speech.setVoice("Google हिन्दी");
  //speech.speak("This is how I speak. This is the text to speech module"); // say something
}

function spacebar() {
  document.body.onkeyup = function(e) {
    if (e.keyCode == 17) {
      speech.setVoice("Google हिन्दी");
      speech.speak("This is how I speak. This is the text to speech module"); // say something
    }
  };
}
window.onload = spacebar;
