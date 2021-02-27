import math
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from sp_bot.modules.misc import Fonts


def truncate(text, font, limit):
    edited = True if font.getsize(text)[0] > limit else False
    while font.getsize(text)[0] > limit:
        text = text[:-1]
    if edited:
        return(text.strip() + '..')
    else:
        return(text.strip())


def drawImage(res, username, pfp):
    songname = res['item']['name']
    albumname = res['item']['album']['name']
    totaltime = res['item']['duration_ms']
    currtime = res['progress_ms']
    coverart = res['item']['album']['images'][1]['url']
    song_url = res['item']['external_urls']['spotify']
    artists = ', '.join([x['name']
                         for x in res['item']['artists']])

    # background object
    canvas = Image.new("RGB", (600, 250), (18, 18, 18))
    draw = ImageDraw.Draw(canvas)

    # album art
    try:
        link = coverart
        r = requests.get(link)
        art = Image.open(BytesIO(r.content))
        art.thumbnail((200, 200), Image.ANTIALIAS)
        canvas.paste(art, (25, 25))
    except Exception as ex:
        print(ex)

    # profile pic
    profile_pic = Image.open(BytesIO(pfp.content))
    profile_pic.thumbnail((48, 48), Image.ANTIALIAS)
    canvas.paste(profile_pic, (527, 25))

    # assign fonts
    namefont = ImageFont.truetype(Fonts.POPPINS, 26)

    if not songname == str(songname.encode('utf-8'))[2:-1]:
        songfont = ImageFont.truetype(Fonts.ARIAL, 26)
    else:
        songfont = namefont

    if not artists == str(artists.encode('utf-8'))[2:-1]:
        artistfont = ImageFont.truetype(Fonts.ARIAL, 26)
    else:
        artistfont = ImageFont.truetype(Fonts.OPEN_SANS, 24)

    if not albumname == str(albumname.encode('utf-8'))[2:-1]:
        albumfont = ImageFont.truetype(Fonts.ARIAL, 21)
    else:
        albumfont = ImageFont.truetype(Fonts.OPEN_SANS, 21)

    # draw text on canvas
    white = '#ffffff'
    draw.text((248, 25), truncate(username, songfont, 250),
              fill=white, font=namefont)
    draw.text((248, 57), "is listening to...",
              fill=white, font=artistfont)
    draw.text((248, 105), truncate(songname, songfont, 315),
              fill=white, font=songfont)
    draw.text((248, 140), f'by {truncate(artists, artistfont, 285)}',
              fill=white, font=artistfont)
    draw.text((248, 175), truncate(albumname, albumfont, 315),
              fill=white, font=albumfont)

    # draw progress bar on canvas
    draw.rectangle([(578, 219), (248, 220)],
                   fill='#404040')
    draw.rectangle([(248 + (currtime / totaltime * 330), 219),
                    (248, 220)], fill='#B3B3B3')

    # return canvas
    image = BytesIO()
    canvas.save(image, 'JPEG', quality=200)
    image.seek(0)
    return image
