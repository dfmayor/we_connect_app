// Get the input element and preview container
var imageInput = document.getElementById('image-input');
var imagePreview = document.getElementById('image-preview');

// Add an event listener to the input element
imageInput.addEventListener('change', function(event) {
  // Clear the previous preview
  imagePreview.innerHTML = '';

  // Get the selected file
  var file = event.target.files[0];

  // Ensure the file is an image
  if (file && file.type.startsWith('image/')) {
    // Create a FileReader object
    var reader = new FileReader();

    // Define the callback function for when the file is read
    reader.onload = function(e) {
      // Create an image element and set the source
      var image = document.createElement('img');
      image.src = e.target.result;
      image.classList.add('img-thumbnail');
      image.alt = "image preview"

      // Append the image to the preview container
      imagePreview.appendChild(image);
    };

    // Read the file as a data URL
    reader.readAsDataURL(file);
  }
});
