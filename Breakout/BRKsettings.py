windowWIDTH = 1280
windowHIEGHT = 720

blockMAP = [
    '666666666666',
    '444557755444',
    '333333333333',
    '222225522222',
    '111111111111',
    '            ',
    '            ',
    '            ',
    '            ']

colorLEGEND = {
    '1': 'blue',
    '2': 'green',
    '3': 'red',
    '4': 'orange',
    '5': 'purple',
    '6': 'bronze',
    '7': 'grey',
}

gapSIZE = 2
blockHEIGHT = windowHIEGHT/len(blockMAP) - gapSIZE
blockWIDTH = windowWIDTH/len(blockMAP[0]) - gapSIZE
topOFF = windowHIEGHT//30

UPGRADES = ["speed","laser","heart","size"]