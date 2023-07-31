function countWords() {
    var textarea = document.getElementById('my-textarea');
    var wordCount = document.getElementById('word-count');
  
    // Remove leading/trailing white spaces and split the text into words
    var words = textarea.value.trim().split(/\s+/);
  
    // Count the number of words
    var count = words.length;
  
    // Update the word count
    wordCount.textContent = `Words: ${count} / 150`;
  
    // Check if the word count exceeds 400
    if (count >= 150) {
      // Truncate the text to 400 words
      textarea.value = words.slice(0, 150).join(' ');
      textarea.setAttribute('readonly', 'readonly');
    } else {
      textarea.removeAttribute('readonly');
    }
  }
  
  function countCharacters() {
    const inputElement = document.getElementById('my-textarea');
    const characterCountElement = document.getElementById('characterCount');
  
    const currentLength = inputElement.value.length;
    const maxLength = parseInt(inputElement.getAttribute('maxlength'));
  
    characterCountElement.textContent = `Character Count: ${currentLength}/${maxLength}`;
  }
  