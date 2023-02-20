echo "---------------------------------------"
echo "TESTING I2S MICROPHONE"
echo "---------------------------------------"

echo "listing recording devices"

arecord -l

echo "---------------------------------------"
echo "recording with sound card 1"
echo "press ctrl-C to end"

arecord -D plughw:1 -c1 -r 48000 -f S32_LE -t wav -V mono -v file.wav

echo "---------------------------------------"
echo "playing recorded audio"

aplay file.wav