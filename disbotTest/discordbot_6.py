from ast import alias
from ctypes import alignment
from http.client import ImproperConnectionState
import discord
from discord.ext import commands
from discord import Colour
import asyncio
from discord.ext import tasks
import datetime
import google_api
import os

service = google_api.get_service()

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

app = commands.Bot(command_prefix='!', description=description, intents=intents)

@app.event
async def on_ready():
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)

#####

@app.command(aliases=['일정'])
async def get_events(ctx, maxResult=5):
    await ctx.send(f'가까운 일정 {maxResult}개를 가져오고 있습니다...')

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=maxResult, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        await ctx.send('가까운 일정이 없습니다.')
        return

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        embed = discord.Embed(title=event.get('summary'),
                              url=event.get('htmlLink'),
                              description=f'{event.get("description")}\n날짜: {start}\nid: {event.get("id")}')
        await ctx.send(embed=embed)

    await ctx.send('가져오기 완료!')

#####

@app.command(aliases=['일정생성'])
async def create_event(ctx, summary, date):
    await ctx.send('일정 생성 중입니다...')
    
    event = {
        'summary': summary,
        'start': {
            'date': date,
            'timeZone': 'Asia/Seoul',
        },
        'end': {
            'date': date,
            'timeZone': 'Asia/Seoul',
        },
        'description' : f'주최자: {ctx.message.author.nick}\n참여원: '
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    start = event['start'].get('dateTime', event['start'].get('date'))
    embed = discord.Embed(title=event.get('summary'),
                          url=event.get('htmlLink'),
                          description=f'{event.get("description")}\n날짜: {start}\nid: {event.get("id")}')
    await ctx.send('일정을 생성하였습니다.', embed=embed)

#####

@app.command(aliases=['일정수정'])
async def update_event(ctx, eventId, key, value):
    await ctx.send('일정 수정 중입니다...')

    event = service.events().get(calendarId='primary', eventId=eventId).execute()

    if key == '제목':
        event['summary'] = value
    elif key == '날짜':
        event['start']['date'] = value
        event['end']['date'] = value

    updated_event = service.events().update(calendarId='primary', eventId=eventId, body=event).execute()

    start = event['start'].get('dateTime', event['start'].get('date'))
    embed = discord.Embed(title=event.get('summary'),
                          url=event.get('htmlLink'),
                          description=f'{event.get("description")}\n날짜: {start}\nid: {event.get("id")}')

    await ctx.send('일정이 수정되었습니다.', embed=embed)

#####

@app.command(aliases=['일정삭제'])
async def delete_event(ctx, eventId):
    await ctx.send('일정 삭제 중입니다...')
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    await ctx.send('일정이 삭제되었습니다.')


@app.command(aliases=['일정참여'])
async def Participation_event(ctx, eventId):
    await ctx.send('일정 참여 투표 중입니다...')
    event = service.events().get(calendarId='primary', eventId=eventId).execute()

    event['description'] += f'{ctx.message.author.nick}, '
    
    updated_event = service.events().update(calendarId='primary', eventId=eventId, body=event).execute()

    start = event['start'].get('dateTime', event['start'].get('date'))
    embed = discord.Embed(title=event.get('summary'),
                          url=event.get('htmlLink'),
                          description=f'{event.get("description")}\n날짜: {start}\nid: {event.get("id")}')
    
    await ctx.send('참여 투표가 완료되었습니다.', embed = embed)

#####

@app.command(aliases=['일정불참'])
async def Cancel_participation_event(ctx, eventId):

    await ctx.send('참여한 투표를 삭제 중입니다...')
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    if f'{event.get("description")}'.find(f'{ctx.message.author.nick}, ') >= 0:
        event['description'] = f'{event.get("description")}'.replace(f'{ctx.message.author.nick}, ', '')
    else: return

    updated_event = service.events().update(calendarId='primary', eventId=eventId, body=event).execute()

    start = event['start'].get('dateTime', event['start'].get('date'))
    embed = discord.Embed(title=event.get('summary'),
                          url=event.get('htmlLink'),
                          description=f'{event.get("description")}\n날짜: {start}\nid: {event.get("id")}')
    
    await ctx.send('참여한 투표를 삭제하였습니다.', embed = embed)


access_token = os.environ["BOT_TOKEN")
app.run(access_token)
