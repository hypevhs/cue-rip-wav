#/usr/bin/env python
#./cuerip.sh "Lords_of_Thunder_(NTSC-U)_[TGXCD1033].cue"

import sys
import wave

isoFilename = sys.argv[1]
offsetSamples = 8000

print(("Using an offset of {0} samples " +
	"({1} bytes at stereo and 16 bits)").format(
		offsetSamples, offsetSamples*4))

def timecodeToBytes(timecode):
	minutes = timecode[:2]
	seconds = timecode[3:5]
	hundredths = timecode[6:]
	totalSecs = int(minutes) * 60
	totalSecs += int(seconds)
	totalSecs += int(hundredths) / 100.0
	samples = int(totalSecs*44100) + offsetSamples
	return int(samples*2*2) # stereo@2 bytes per seconds

def extractTrack(isoFile, bFrom, bTo, trackNum):
	isoFile.seek(bFrom)
	bytes = isoFile.read(bTo - bFrom)
	
	print("Track {0} from {1} to {2}".format(
		trackNum, bFrom/4, bTo/4))
	
	wf = wave.open("Track {0}.wav".format(trackNum), "w")
	wf.setnchannels(2)
	wf.setsampwidth(2)
	wf.setframerate(44100)
	wf.writeframes(bytes)
	wf.close()

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

def main():
	isoFile = open(isoFilename, "rb")
	thisTrackLoc = None
	trackNum = 1
	for line in sys.stdin:
		if thisTrackLoc == None:
			thisTrackLoc = timecodeToBytes(line)
			continue
		nextTrackLoc = timecodeToBytes(line)
		
		extractTrack(isoFile, thisTrackLoc, nextTrackLoc, trackNum)
		
		thisTrackLoc = nextTrackLoc
		trackNum += 1
	# last track doesn't have an end marker, extract the rest of the bytes
	extractTrack(isoFile, thisTrackLoc, getSize(isoFile), trackNum)

if __name__ == "__main__":
	main()