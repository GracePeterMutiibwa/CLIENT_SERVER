document.addEventListener("DOMContentLoaded", () => {
  // input fields and buttons
  const allLoginInputs = document.querySelectorAll(".login-input");

  const loginButton = document.getElementById('login-button');


  function trackChangesAndUpdate() {
    // count of how many fields have data :
    let thoseWithText = 0;

    allLoginInputs.forEach((eachInputField) => {
      // get the text size
      let textSize = eachInputField.value.length;

      if (textSize > 0) {
        // update the count
        thoseWithText += 1;
      } else {
      }
    });

    // if more than one field has data: activate the login button else deactivate it
    if (thoseWithText > 1){
        loginButton.disabled = false;

    } else {
        loginButton.disabled = true;
    }

  }

  allLoginInputs.forEach((eachLoginInputField) => {
    eachLoginInputField.addEventListener("input", () => {
        // check if all fields have data in them
        trackChangesAndUpdate();
    });
  });


});
