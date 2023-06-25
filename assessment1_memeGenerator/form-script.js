document.addEventListener("DOMContentLoaded", function() {

  window.onload = function() {
    const el = document.createElement("img");
    el.setAttribute("src", "images/meme.png");
    el.setAttribute("width", "85%");
    document.getElementById("demoDiv").appendChild(el);
  }

  let img = document.getElementsByTagName("img");
  let form = document.querySelector("#newForm");
  let newButton = document.querySelector("button");

  newForm.addEventListener("submit", function(event){
    event.preventDefault();

    const meme = document.createElement("div");
    const textTop = document.createElement("div");
    const textBottom = document.createElement("div");
    const img = document.createElement("img");
    const newButton = document.createElement("button");
    newButton.innerText = "x";

    newButton.addEventListener("click", function(event) {
      event.target.parentElement.remove();
    });

    img.src = document.getElementById("imageUrl").value;
    textTop.classList.add("textTop");
    textTop.innerHTML = document.getElementById("topText").value;
    textBottom.classList.add("textBottom");
    textBottom.innerHTML = document.getElementById("bottomText").value;

    meme.classList.add("meme");
    meme.append(textTop);
    meme.append(textBottom);
    meme.append(img);
    meme.append(newButton);
    newForm.reset()
    
    const memeLocation = document.querySelector("#memeList");
    memeLocation.appendChild(meme);
    memeLocation.addEventListener('click', (event) => {
          event.target.parentElement.remove();
    });
  
  });

})


  

