# Brand assets manifest

`manifest.json` is the file list the loft331.ca brand assets page reads.
It mirrors the Google Drive folder "Loft 331 Brand Assets" (dan@loft331.ca):

- Logos  → Drive folder `1AhyHHVlNhTaqariigsk_sDC9zdpJrhBd`
- Photos → Drive folder `1B9Ts1Q6tz9J4G3kUqSXEpM5JKGWsqk5r`

A daily scheduled Claude task rebuilds it from those two folders. Do not edit by hand:
drop files into the Drive folders instead. Format: `{"logos":[{"id","name"}],"photos":[{"id","name"}]}`,
each list sorted by lowercase name.

`previews/` holds the four 16:10 logo card previews the page shows (g_inv = green, g = white on green,
b = black, w = white). Each is the designer's horizontal JPG centred on its own background colour, unaltered.
