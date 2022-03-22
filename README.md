# Project: eProof helper
This repository is meant to help eProof easier when the manuscript is under the production process. The working scenario would be when the manuscript is returned after modified by the copyeditor with redlines indicating the changes which are usually not very perceivable. (See Before below)

This snippet can help eProof a bit easier by (1) converting the thin strikethroughs into background colors; (2) adding a colored block before each line whenever there is a change in that line (red indicates deletions, blue indicates addition). (See After below) 

After that, the authors should catch the changes more easily, which may be further helpful, for example, in updating the arXiv version of the manuscript.

| Before | After |
| ------ | ----- |
| ![original](original.png)| ![converted](converted.png)|


# Methods
1. Convert the redline PDF file to html. [https://cloudconvert.com/pdf-converter]
2. `python eproof.py`, then enter the path of the HTML file. The filename of the converted HTML will be appended `_mod`.


# To Do
1. Remove the mysterious blue block at the end of each page.
2. When the equations are rendered in red, the fraction lines and square root signs may be misidentified as strikethroughs. 

# Note
The template is the APS journals such as [Physical Reviews Letters](https://journals.aps.org/elecproofs.html).  