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


def checkUnicode(text):
    return text == str(text.encode('utf-8'))[2:-1]


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
    profile_pic.thumbnail((52, 52), Image.ANTIALIAS)
    canvas.paste(profile_pic, (523, 25))

    # set font sizes
    open_sans = ImageFont.truetype(Fonts.OPEN_SANS, 23)
    # open_bold = ImageFont.truetype(Fonts.OPEN_BOLD, 23)
    poppins = ImageFont.truetype(Fonts.POPPINS, 25)
    arial = ImageFont.truetype(Fonts.ARIAL, 25)
    arial23 = ImageFont.truetype(Fonts.ARIAL, 23)

    # assign fonts
    songfont = poppins if checkUnicode(songname) else arial
    artistfont = open_sans if checkUnicode(artists) else arial23
    albumfont = open_sans if checkUnicode(albumname) else arial23

    # draw text on canvas
    white = '#ffffff'
    draw.text((248, 18), truncate(username, poppins, 250),
              fill=white, font=poppins)
    draw.text((248, 53), "is listening to",
              fill=white, font=open_sans)
    draw.text((248, 115), truncate(songname, songfont, 315),
              fill=white, font=songfont)
    draw.text((248, 150), truncate(artists, artistfont, 315),
              fill=white, font=artistfont)
    draw.text((248, 180), truncate(albumname, albumfont, 315),
              fill=white, font=albumfont)

    # draw progress bar on canvas
    draw.rectangle([(578, 222), (248, 224)],
                   fill='#404040')
    draw.rectangle([(248 + (currtime / totaltime * 330), 222),
                    (248, 224)], fill='#B3B3B3')

    # return canvas
    image = BytesIO()
    canvas.save(image, 'JPEG', quality=200)
    image.seek(0)
    return image
