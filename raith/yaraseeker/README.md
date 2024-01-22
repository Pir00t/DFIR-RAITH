# YaraSeeker

After disliking poring over results in a terminal window, I decided to make reviewing Yara output a bit more interactive.


![Hagrid](seeker.jpg)

## Use Cases

Personally, I use this for playing around with rule development and filtering results to allow for tuning. I've also found this useful when Reverse Engineering, being able to obtain a match offset and locate it in Ghidra.

## Usage

The provided Dockerfile can be used to create an image in order to spin up a container with the necessary requirements. This is the recommended method for use given the scripts utilise libraries and functions specific to Jupyter Notebooks for output.

To run the Docker container and interact with the notebook, firstly ensure you are in the **raith/** folder then run:

- docker run -it --rm -p 8888:8888 -v .:/home/analyst/workdir <image-name> (PowerShell)
- docker run -it --rm -p 8888:8888 -v "${PWD}":/home/analyst/workdir <image-name> (bash) 

This will start the container, mapping the current directory to `/home/analyst/workdir`. Feel free to set Docker CPU limits etc. as I've just provided a basic command to get up and running.