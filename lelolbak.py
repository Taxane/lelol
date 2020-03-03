# Wrappers for Riot API
# By: Darian R.
# Date: 2020-02-21

import requests
import json
import trueskill
import pickle
import os, sys
from time import sleep

APIKey = 'RGAPI-564ae690-7212-4181-a378-386a494c3dad'
summonerName = 'Taxane'

def requestSummonerData(summonerName, APIKey):
    URL = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()


summonerInfo = requestSummonerData(summonerName, APIKey)

def getSummonerAccountId(summonerName):
    thisSummonerInfo = requestSummonerData(summonerName, APIKey)
    return thisSummonerInfo['accountId']

def getSummonerMatchlist(summonerName, APIKey):
    summonerAccountId = getSummonerAccountId(summonerName)
    URL2 = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summonerAccountId + '?api_key=' + APIKey
    response2 = requests.get(URL2)
    return response2.json()

def getParticipantGameIds(summonerName, APIKey):
    matchList = getSummonerMatchlist(summonerName, APIKey)
    gameIdList = []
    for games in matchList['matches']:
        gameIdList.append(games['gameId'])
    return gameIdList

def getMatchInfo(gameId):
    URL3 = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + str(gameId) + '?api_key=' + APIKey
    response3 = requests.get(URL3)
    matchJSON = response3.json()
    participantList = []
    gameCreationTime = matchJSON['gameCreation']
    participantList.append(gameId)
    participantList.append(gameCreationTime)
    fullParticipantInfo = matchJSON['participantIdentities']
    fullTeamInfo = matchJSON['participants']
    #return fullParticipantInfo

    for i in range(len(fullParticipantInfo)):
        sumoAcctId = fullParticipantInfo[i]['player']['accountId']
        sumoName = fullParticipantInfo[i]['player']['summonerName']
        participantId = fullParticipantInfo[i]['participantId']
        participantTeamId = fullTeamInfo[i]['teamId']
        participantWorL = fullTeamInfo[i]['stats']['win']
        
        participantList.append({sumoAcctId: [sumoAcctId, sumoName, participantId, participantTeamId, participantWorL]})
    return participantList



# print(getMatchInfo(3302754274))

def checkRecords(records='records.txt', gamesRecorded='gamesRecorded.txt', gameIdToAdd=3302754274):
    with open(os.path.join(sys.path[0], gamesRecorded), 'a+') as gr:
        gr.seek(0)
        gamesRecordedLoaded = gr.readlines()
        if (str(gameIdToAdd) + '\n') not in gamesRecordedLoaded:
            with open(records, 'a+') as f:
                recordsLoaded = f.readlines()
                infoToAdd = getMatchInfo(gameIdToAdd)
                recordsLoaded.append(infoToAdd)
                f.write(str(infoToAdd) + '\n')
                gr.write(str(gameIdToAdd) + '\n')
                print(str(gameIdToAdd) + ' has been recorded!')

        elif (str(gameIdToAdd) + '\n') in gamesRecordedLoaded:
            print('This game has already been recorded!')
            pass
        else:
            print("'Sumtin ain't right fella")
            pass

def recordMatchListData():
    for game in getParticipantGameIds(summonerName, APIKey):
        checkRecords(gameIdToAdd=game)
        sleep(6)

# recordMatchListData()

def genTrueskillRatingObj(ratingsDB='ratings.txt', records='records.txt'):
    with open(records, 'r+') as recs:
        matchInfoList = recs.readlines()
    for matches in matchInfoList:
        print(matches[0])


genTrueskillRatingObj()



