const wordleURLs = ["powerlanguage.co.uk/wordle/"];

let nextWord = document.getElementById("next");

nextWord.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (wordleURLs.some(url => tab.url.includes(url))) {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: fillWord,
    });
  }
  else {
    alert("You need to be on the official Wordle site for this to work!");
  }
});

function fillWord() {
  fetch(chrome.runtime.getURL("./words/knuth.txt"))
  .then(r => r.text())
  .then(result => {
    let feasibleWords = result.split("\n");

    fetch(chrome.runtime.getURL("./words/word_counts.txt"))
    .then(c => c.text())
    .then(counts => {

      let gameApp = document.querySelector("game-app").shadowRoot;
      gameApp.querySelectorAll("game-row").forEach(row => {
          row.shadowRoot.querySelectorAll("[evaluation='absent']").forEach(
            absent => { 
              feasibleWords = feasibleWords.filter(word => !word.includes(absent.getAttribute("letter")));
            }
          );
          row.shadowRoot.querySelectorAll("[evaluation='present']").forEach(
            present => { 
              feasibleWords = feasibleWords.filter(word => word.includes(present.getAttribute("letter")));
            }
          );
          row.shadowRoot.querySelectorAll("[evaluation='correct']").forEach(
            correct => { 
              let index = Array.prototype.indexOf.call(correct.parentNode.children, correct);
              feasibleWords = feasibleWords.filter(word => word[index] === correct.getAttribute("letter"));
            }
          );
        }
      );

      if (feasibleWords.length == 0) {
        alert("Oh no, we've run out of words!");
      }
      else {
        console.log(feasibleWords);

        counts = counts.split("\n");
        let minScore = Number.MAX_VALUE;
        let bestWord = feasibleWords[0];

        feasibleWords.forEach(candidate => {
          let score = 0;
          
          counts.forEach(count => {
            count = count.split(" ");
            if (candidate.includes(count[0])) {
              score += parseInt(count[1]);
            } 
          });
          
          if (feasibleWords.length < 250) {
            console.log(candidate + " " + score);
          }
          if (score < minScore) {
            minScore = score;
            bestWord = candidate;
          }
        });

        console.log(bestWord);
        
        let keyboard = gameApp.querySelector("game-keyboard").shadowRoot;
        [...bestWord].forEach(letter => keyboard.querySelector(`[data-key='${letter}']`).click());
        keyboard.querySelector(".row:last-child").children[0].click();
      }
    });
  });
}
