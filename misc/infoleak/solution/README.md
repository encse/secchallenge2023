# Infoleak

I read the news about the depixelation challenge and how it was solved last year in Twitter or HackerNews. I might have also found the blog post about it (https://bishopfox.com/blog/unredacter-tool-never-pixelation), so I tried this tool but it didn't work on my mac unfortunately. I also tried [Depix](https://github.com/beurtschipper/Depix) very briefly but haven't spent enough time to experiment with the parameters. But I liked this challenge so much that asked for help from the author after the contest.

The tool that we had to use was indeed Depix, with the following parameters:

```shell
depix -p ./cut.png -s ./Depix-main/images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png -o depixelized.png --averagetype linear
```

The `--averagetype linear` part is very important here!

The trick was of course about the proper cutting of the image so that it works properly with `depix`. If you just run it on the whole image it will not find too much info, but I realized that it can depixelate some narrow vertical stripes completely, so after lots of experimentation I decided to slice up the image to 4px wide columns like a shredder, run `depix` on them one by one then glue them together once again.

<img width="1018" alt="image" src="https://user-images.githubusercontent.com/6275775/233265786-e2957aaf-57e7-4026-90a7-1c047985ecb1.png">

The output is some restaurant menu with some orders, where the amount people are paying can be translated to ascii codes resulting the flag.

The idea was great, the tools of depixelation are little bit odd, but it was a fun experiment anyway.