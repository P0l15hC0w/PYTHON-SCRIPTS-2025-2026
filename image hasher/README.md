# IMAGE HASHER
-   # USE AT YOUR OWN RISK
    - THE **HASH FILES MIGHT GET VERY BIG IN SIZE** AND MIGHT NOT LIKE BIG IMAGES, WHICH WOULD STILL BE PROCESSED NO MATTER THEIR SIZE.

    - IT IS RECOMMENDED TO **USE SMALL PHOTOS** JUST TO HAVE FUN WITH HASHING/DEHASHING THEM.

- RECOMMENDED IMAGE SIZE IS UP TO **200x200** PIXELS.

- # basic information
- those apps use the sha256 algorythm to hash and store the image.
- it is very common for the output file with the hash to be **HUGE IN SIZE**.

- # how do the apps work?
- ## the image hasher
    it works as a base for the dehasher to work.
    
    1. it loads the size of the image and saves it in the file as an information for the dehasher to how big is the file and where to switch to the next line.

    2. for every pixel it divides the color values into R, G, B and hashes them marking down where the values begin and where the pixel starts/ends.

    3. in the end it saves the image in the **given format** of the file.
- ## the image dehasher
    it uses the base files of the hasher to work
    **AND WILL ONLY WORK WITH THE MAKRS OF THIS HASHER**.
    1. it finds the size of the image marked by the hasher and sets the length of one line to it's width.

    2. it divides the hash values for every pixel and color with the markings and uses sha256 to dehash the colors.
    
    3. in the end it joins the colors and pixels to form an image out of them, **saving them in the desired format**.