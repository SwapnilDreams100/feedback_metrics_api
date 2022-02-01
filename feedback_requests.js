base_url = "https://localhost:5000/"; // or a global url

function getMochaScores(passage_no, q_no){
   $.ajax({
          type: "GET",
          url: base_url + "get_mocha_scores",
          async:false,
          data:{
            "passage_no":passage_no.toString(),
            "q_no":q_no.toString()
          },
          dataType: "json",
          success: function(result) {
            //Do whatever you want with the result
              console.log("Done")
          },
          error: function(XMLHttpRequest, textStatus, errorThrown){
                  alert(errorThrown, textStatus);
          },
        });  
}

function getTypingSpeed(path){
   $.ajax({
          type: "GET",
          url: base_url + "get_typing_speed",
          async:false,
          data:{
            "path":path.toString(),
          },
          dataType: "json",
          success: function(result) {
              console.log("Done")
          },
          error: function(XMLHttpRequest, textStatus, errorThrown){
                  alert(errorThrown, textStatus);
          },
        });  
}

function getMistakes(path){
   $.ajax({
          type: "GET",
          url: base_url + "get_mistakes",
          async:false,
          data:{
            "path":path.toString(),
          },
          dataType: "json",
          success: function(result) {
              console.log("Done")
          },
          error: function(XMLHttpRequest, textStatus, errorThrown){
                  alert(errorThrown, textStatus);
          },
        });  
}