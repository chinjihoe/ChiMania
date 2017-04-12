import os

songList = []
totalSongs = 0 

#Print the available songs
def listSongs():
    global songList, totalSongs
    songList = os.listdir("./songs")
    totalSongs = len(songList)
    
    print("# |Song name")
    for i, song in enumerate(songList):
        print(i,"|"+song)
    
    try:
        chosenSong = int(input("\nSelect song: 0-"+str(totalSongs-1)+"\n#"))

        if isinstance(chosenSong, int):
            if chosenSong >= 0 and chosenSong <= totalSongs:
                print("Selected:",songList[chosenSong],"\n")
                return listDifficulties(songList[chosenSong])
                
        return listSongs()
    except:
        return listSongs()

#Print the available difficulties of the chosen song
def listDifficulties(song):
    totalDifficulties = 0
    diffList = []
    print("# |Difficulty name")
    for file in os.listdir("./songs/"+song):
        if file.endswith(".osu"):
            if searchLine("./songs/"+song+"/"+file, "Mode: 3"):
                diffList.append(file)
                print(totalDifficulties,"|"+file)
                totalDifficulties += 1

    try:
        if totalDifficulties > 0:
            chosenDiff = int(input("\nSelect difficulty: 0-"+str(totalDifficulties)+"\n#"))
            if isinstance(chosenDiff, int):
                if chosenDiff >= 0 and chosenDiff <= totalDifficulties:
                    print("Selected:",diffList[chosenDiff])
                    return song, diffList[chosenDiff]
        return listSongs()
    except:
        return listSongs()

#Search a line in the .osu file and return True if line is found, else False
def searchLine(song, line):
    with open(song, encoding='utf-8') as f:
        for l in f.readlines():
            if line in l:
                return True
    return False

#Load the beatmap of the chosen difficulty of the chosen song
#And return the path of the .mp3 file
def loadBeatmap():
    lines = []
    beatmap = []
    song, diff = listSongs()

    with open('./songs/'+song+"/"+diff, encoding='utf-8') as f:
        lines = f.readlines()
        
    lanes = ['64', '192', '320', '448']
    audioFile = "audio.mp3"

    found = False
    for l in lines:
        if found:
            ob = l.split(",",5)
            ob.pop(1)
            ob.pop(2)
            ob.pop(2)
            ob[2] = ob[2].split(":",1)[0]

            for x in range(4):
                if ob[0] == lanes[x]:
                    ob[0] = x
            beatmap.append(ob)

        if "[HitObjects]" in l:
            found = True

        if "AudioFilename" in l:
            audioFile = song+"/"+l.split(": ",1)[1].split(".mp3",1)[0]+".mp3"

    return beatmap, audioFile
