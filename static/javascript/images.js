
        // Initialize Swiper with custom options
        var swiper = new Swiper('.swiper-container', {
            direction: 'horizontal', // Scroll horizontally
            slidesPerView: 'auto', // Fit as many images in view as possible
            freeMode: true, // Enable free mode (dragging without snapping)
            mousewheel: true, // Enable mousewheel scrolling
        });

        // Function to handle selecting an image for editing
        function selectImageForEditing() {
            // Get the active slide index
            var activeIndex = swiper.activeIndex;
            // Get the image filename at the active index
            var imageElement=document.getElementById('img'+(activeIndex+1));
            var imageURL=imageElement.src;
            //move the location url_to /edit_image/<image> page
            window.location.replace('/edit_image/?imageURL='+encodeURIComponent(imageURL));
        }

