'use strict';

const likeButtonArray = document.querySelectorAll(".likes");
console.log(likeButtonArray);

for (const likeButton of likeButtonArray) {
    likeButton.addEventListener("click", () => {
        alert("Thank you for your like!");
    })
}



const quoteBtn = document.getElementById("affirmation-button");
console.log('reached here!')
console.log(quoteBtn);

quoteBtn.addEventListener('click', () => {
    fetch('/show_affirmations')
        .then(response => response.text())
        .then(affirmation => {
            document.getElementById("quote").innerHTML = affirmation;
        });


});



