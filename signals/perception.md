# Designed for human senses

Last reviewed: 2026-11-03

A concept page in the signals and control family: the numbers a computer uses for images and sound aren't physical measurements. They're shaped around what people can see and hear, and doing arithmetic on them as if they were physics gives wrong answers.

## Problem

Output exists for people, and people don't perceive the world evenly. Eyes are far more sensitive to differences between dark shades than bright ones; ears hear only a limited range of pitches; motion looks smooth above a certain number of pictures a second. So the formats that store images and sound are built around human perception, which makes them compact and good-looking. The trouble starts when someone treats those numbers as plain quantities, and averages, mixes or scales them as if they measured light or sound directly.

## The story

In 2008 Zainab Qureshi built the image pipeline for a photo-sharing site. Every uploaded photo needed a thumbnail and three smaller sizes. She wrote the resizing herself, using the standard approach: to shrink an image to half its width and height, replace each block of four pixels with their average. The numbers in an image file were brightness, from 0 for black to 255 for white, so the average of four pixels' numbers was their average brightness. It was simple, fast and what every textbook example did.

A few months later a professional photographer wrote in, politely and in detail. Her thumbnails were darker and muddier than her photos. Night scenes lost their lights; a field of bright grass went dull; a black-and-white striped shirt turned into a dark grey one, much darker than the shirt looked from across a room. Zainab made a test image of alternating black and white lines and shrank it. Black was 0 and white was 255, so the average was 128, a middle grey. But the stripes, seen from a distance, looked much lighter than that grey.

She found the answer in the image format's documentation. The numbers weren't amounts of light. They were encoded on a curve, called *gamma*, that used more of the 256 available values for dark shades, where eyes notice small differences, and fewer for bright ones, where they don't. Halfway between black and white in light was about 188, not 128. A pixel stored as 128 gave off only about a fifth as much light as white. Her averaging had been correct arithmetic on the wrong quantity.

*Before reading on: the numbers were accurate, the averaging was correct, and the pictures came out wrong. What would you have changed?*

Zainab didn't change how images were stored. The curve was right for storage: with only 256 values, spacing them evenly by light would have wasted most of them on bright shades nobody could tell apart, and shown visible bands in shadows. Instead she changed where the arithmetic happened. Each pixel was converted from the stored curve into linear light, the resizing was done there with more precision, and the result was converted back. Thumbnails stopped going dark, and the striped shirt shrank to the grey it looked like from across a room.

The photographer's next email raised a second problem. Some of her photos looked washed out on the site, though they looked rich in her editing software. Her camera saved them in a wider range of colours than ordinary screens assumed, and recorded that in a small *colour profile* inside the file, which Zainab's pipeline had been throwing away as unnecessary metadata. The same numbers meant different colours depending on which profile they belonged to. The pipeline now converted every photo to the web's standard colour space before resizing, using its profile, instead of discarding it.

Looking back, Zainab thought every number in an image had already been shaped by a decision about people, about what eyes notice and what screens were assumed to be. Before doing arithmetic on a number, you had to know what it was actually measuring.

## Where it shows up

| Page | The format | What it was designed around |
| --- | --- | --- |
| [Compression](../info/compression.md) | JPEG and MP3 | Discarding what eyes and ears are least sensitive to: lossy compression with a good model of its receiver. |
| [Sampling and aliasing](sampling.md) | The CD's 44,100 samples a second | Just over twice the highest pitch people hear. |
| [Floating-point](../math/floating-point.md) | Numbers with more precision near zero | The same idea as gamma: spend the limited values where the differences matter. |
| [Labels and training data](../data/labels.md) | What raters judged in ten seconds | Human perception as the measuring instrument, with its own blind spots. |

It shows up elsewhere too: screens with red, green and blue sub-pixels because people have three kinds of colour receptor, film and video at 24 to 60 pictures a second because that's enough to see motion, decibels measured on a scale that follows how loudness is perceived, contrast rules for accessible text, and the "night mode" that shifts screens away from blue.

What these share is a hidden model of a person. Every format meant for eyes or ears decided what people would and wouldn't notice. That makes it compact and convincing, and it means its numbers mean something only relative to that model. Calculate with them as physics and the model breaks; ask whose eyes the model was built for and you sometimes find it was only some people's.

## It really happened

Zainab is fictional; the mistake was everywhere. In 2010 a page by Eric Brasseur drew wide attention by showing that many popular programs, including image editors and web browsers, scaled images without accounting for gamma, and darkened them ([Brasseur, "Gamma error in picture scaling"](http://www.ericbrasseur.org/gamma.html) <!-- verify -->). Gamma began as a property of cathode-ray-tube screens, whose brightness didn't rise in step with their input voltage. It survived the end of those screens because the curve also roughly matched human perception, which made it an efficient way to store images. The web's standard colour space, sRGB, was proposed by Hewlett-Packard and Microsoft in 1996 and standardised in 1999 ([W3C's copy of the proposal](https://www.w3.org/Graphics/Color/sRGB.html)).

Colour itself is defined by people. The CIE 1931 colour space was built from experiments in which observers matched colours by eye, and every colour standard since rests on it. And the model of a person can be narrow. For decades Kodak's colour film was calibrated against "Shirley cards", reference photos of a woman whose skin was used to set the colour balance in photo labs. Until the 1970s the model was always white, and film reproduced darker skin poorly. The communications researcher Lorna Roth has documented how that changed ([NPR](https://www.npr.org/transcripts/363517842) <!-- verify -->). In February 2015 a photograph of a dress divided millions of people over whether it was blue and black or white and gold, a reminder that colour is something the brain constructs, not something the numbers contain.

## What it is

Formats for images, video and sound encode values according to human perception, not physical units. Image values are usually gamma-encoded: they follow a curve that spends more precision on dark tones, where eyes are more sensitive. A colour is three numbers, one each for red, green and blue, because people have three kinds of colour receptor, and what those numbers mean depends on the colour space, recorded in a profile. Audio is sampled to cover the range of human hearing, and lossy formats discard what perception would miss. The working rule is to store in perceptual encoding and calculate in linear units: convert to light or sound pressure, blend, scale or mix there, then convert back.

## Where it gets misapplied

- **Arithmetic on encoded values.** Resizing, blurring, blending and averaging gamma-encoded pixels, which makes results too dark.
- **Discarding colour profiles.** The same numbers become different colours, usually duller ones.
- **A model of "the viewer" built from one group of people.** Shirley cards, and the systems trained on photographs that inherited their calibration.
- **The mirror:** storing everything in linear light with too few bits. Gamma isn't an error to remove; it's the right way to store images. The mistake is only calculating in it.

## Connections

- Learning this is also learning [compression](../info/compression.md), because lossy formats succeed by modelling what people notice, and fail when the model is wrong.
- Learning this is also learning [sampling](sampling.md), because the sample rate and bit depth of every output format were chosen from human limits.
- Learning this is also learning [floating-point](../math/floating-point.md), because both spend a limited supply of values unevenly, where the differences matter most.
- Learning this is also learning [labels and training data](../data/labels.md), because a model of human perception can be trained or calibrated on too narrow a group, and inherit its blind spots.
- Learning this is also learning [encodings](../info/encodings.md), because a colour profile is an encoding, and throwing it away is decoding with the wrong codebook.

## Resources

1. Eric Brasseur, ["Gamma error in picture scaling"](http://www.ericbrasseur.org/gamma.html) (start here: the striped-image test, and how to check your own software). <!-- verify -->
2. Charles Poynton, ["Gamma FAQ"](https://poynton.ca/GammaFAQ.html) (go deeper: why gamma exists, from someone who helped standardise video). <!-- verify -->
3. Michael Stokes and others, ["A Standard Default Color Space for the Internet: sRGB"](https://www.w3.org/Graphics/Color/sRGB.html) (1996) (reference).

## Names you'll hear

- **Gamma, transfer function:** the curve between stored values and light.
- **Linear light:** values proportional to physical light, where arithmetic works.
- **Colour space, sRGB, Display P3:** what a set of three numbers means; the web's default, and a wider one used by many phones.
- **Colour profile (ICC profile):** the label in a file saying which colour space its numbers belong to.
- **Banding:** visible steps where too few values cover a smooth gradient.
- **Perceptual coding:** compression that discards what people won't notice.

## Go and look

Find a photo with fine black-and-white detail, shrink it to a quarter of its size in two different programs, and compare them side by side with the original from a distance. If one is noticeably darker, that program averages encoded values.
