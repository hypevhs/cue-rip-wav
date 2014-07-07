#/usr/bin/env python
#./cuerip.sh "Lords_of_Thunder_(NTSC-U)_[TGXCD1033].cue"

import sys
import wave

isoFilename = sys.argv[1]
offsetSamples = 8582

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

isoFile = open(isoFilename, "rb")
thisTrackLoc = None
trackNum = 1
for line in sys.stdin:
	if thisTrackLoc == None:
		thisTrackLoc = timecodeToBytes(line)
		continue
	nextTrackLoc = timecodeToBytes(line)
	isoFile.seek(thisTrackLoc)
	bytes = isoFile.read(nextTrackLoc - thisTrackLoc)
	
	print("Track {0} from {1} to {2}".format(
		trackNum, thisTrackLoc/4, nextTrackLoc/4))
	
	thisTrackLoc = nextTrackLoc
	
	wf = wave.open("Track {0}.wav".format(trackNum),"w")
	wf.setnchannels(2)
	wf.setsampwidth(2)
	wf.setframerate(44100)
	wf.writeframes(bytes)
	wf.close()
	
	trackNum += 1
