# Wrappers for Riot API
# By: Darian R.
# Date: 2020-02-21

import requests
import json
import trueskill
import pickle
import os, sys
from time import sleep

APIKey = 'RGAPI-1614f160-c74e-4e2e-b188-b94b71ed41ce'
summonerName = 'Taxane'
gamesRecdFileName = 'gamesRec.txt'
recordsFileName = 'records.json'
gameId = 3301832021


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
    # return fullParticipantInfo

    for i in range(len(fullParticipantInfo)):
        sumoAcctId = fullParticipantInfo[i]['player']['accountId']
        sumoName = fullParticipantInfo[i]['player']['summonerName']
        participantId = fullParticipantInfo[i]['participantId']
        participantTeamId = fullTeamInfo[i]['teamId']
        participantWorL = fullTeamInfo[i]['stats']['win']

        participantList.append({sumoAcctId: [sumoAcctId, sumoName, participantId, participantTeamId, participantWorL]})
    return participantList


# print(getMatchInfo(3302754274))

def checkForGamesRecdFile(gamesRecd=gamesRecdFileName):
    with open(os.path.join(sys.path[0], gamesRecd), 'a+') as grd:
        grd.seek(0)
        try:
            gamesRecdLoadedJson = grd.readlines()
            print('Found the file!')
            return (True)
        except:
            list1 = []
            grd.write(list1)
            print('Did not find file. No worries... Creating new one')
            return (False)


def checkForRecordsFile(records=recordsFileName):
    with open(os.path.join(sys.path[0], records), 'a+') as fRecords:
        fRecords.seek(0)
        try:
            recordsJson = json.load(fRecords)
            print('Found the file!')
            return (True)
        except:
            list2 = {}
            json.dump(list2, fRecords)
            print('Did not find file. No worries... Creating new one')
            return (False)


# print(checkForRecordsFile())
# print(checkForGamesRecdFile())

def checkRecords(records=recordsFileName, gamesRecd=gamesRecdFileName, gameIdToAdd=gameId):
    goodToGo = False
    recordedGame = False
    if checkForGamesRecdFile() == True and checkForRecordsFile() == True:
        goodToGo = True
    with open(os.path.join(sys.path[0], gamesRecd), 'a+') as gral:
        listOfRecGamesByID = gral.readlines()
        if gameIdToAdd in listOfRecGamesByID:
            recordedGame = True
        elif gameIdToAdd not in listOfRecGamesByID:
            recordedGame = False
        else:
            return(999)
    if recordedGame is False:
        with open(os.path.join(sys.path[0], records), 'r+') as recs:
            allrecs = dict(json.load(recs))
            gameMatchInfo = getMatchInfo(gameIdToAdd)
            allrecs.update({gameIdToAdd : gameMatchInfo})
            json.dump(allrecs, recs)
            print(allrecs)



checkRecords()


def recordMatchListData():
    listToDump = []
    for game in getParticipantGameIds(summonerName, APIKey):
        checkRecords(gameIdToAdd=game)
        sleep(6)


# recordMatchListData()

def genTrueskillRatingObj(ratingsDB='ratings.txt', records='records.txt'):
    with open(records, 'rb') as recs:
        matchInfoList = json.loads(records)
    for matches in matchInfoList:
        print(matches[0])

# genTrueskillRatingObj()
