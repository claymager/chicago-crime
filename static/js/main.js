function reset_time(){
  var tzoffset = (new Date()).getTimezoneOffset() * 60000;
  var date_str = (new Date(Date.now() - tzoffset)).toISOString();
  document.getElementById("datetime").value = date_str.split(".")[0];
  console.log("updated time")
}

function toggle_detailed(){
  const detailed = document.getElementById("detailed")
  if (detailed.style.display === "none") {
    detailed.style.display = "block";
  } else {
    detailed.style.display = "none";
  }
}
    
function get_results(){
  const latitude = document.getElementById("latitude").value;
  const longitude = document.getElementById("longitude").value;
  const datetime = document.getElementById("datetime").value;
  const loc_desc = document.getElementById("location_desc").value;
  const prediction = document.getElementById("prediction");
  const accuracy = document.getElementById("accuracy");
  const dummyAccuracy = document.getElementById("dummyAccuracy");
  const precision = document.getElementById("precision");
  const recall = document.getElementById("recall");
  const f1 = document.getElementById("f1");
  const modelname = document.getElementById("modelNames").value;
  const target = document.getElementById("targetSelect").value;
  const resultsElement = document.getElementById("results");
  if (resultsElement.style.display === "") {
    resultsElement.style.display = "block";
  };

  console.log("called get_results()")
  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "/model/"+modelname+"_for_"+target,
    async: true,
    data: JSON.stringify({
      latitude: latitude,
      longitude: longitude,
      datetime: datetime,
      loc_desc: loc_desc
    }),
    success: (response) => {
      response = JSON.parse(response)
      prediction.textContent = response.prediction;
      accuracy.textContent = response.accuracy;
      dummyAccuracy.textContent = response.dummy_accuracy;
      precision.textContent = response.precision;
      recall.textContent = response.recall;
      f1.textContent = response.f1;
      console.log(response)
    },
    error: (response) => {
      console.log("failure");
      resultsElement.textContent = "INVALID";
    }
  })

}
