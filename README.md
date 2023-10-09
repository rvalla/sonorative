![icon](https://gitlab.com/azarte/sonorative/-/raw/master/assets/img/logo_64.png)

# sonorative

Here I am exploring options to transform data from images into sound. The idea is to test
different algorithms and play (I am talking about having fun and also listening to the output
audio files). This is not my priority project now but I came back to it from time to time.  

## ColorsSound()

With **ColorsSound()** I explore different ways of taking an image color data (grayscale or
rgb values) and map it to the amplitude of an audio signal. I am working in 3 specific
*modes* in this stage:

- **amplitude**: the amplitude of the signal is directly taken from pixel data (some sort of *am synthesis*).
- **frequency**: the amplitude of the signal depends on the output of a sine functions which frequency is the
color value (some sort of *fm synthesis*).
- **sceptral**: the amplitude of the signal depends on the combinations of the amplitudes from a set of partials
(3 different frequencies, one for each color). Some sort of spectral modulation (ok, this doesn't exist).  

You can check the results at */colorssound/output*.  

Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
