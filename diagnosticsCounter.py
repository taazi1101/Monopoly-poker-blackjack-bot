import os
import time

class diagnostic:
    path = "data/diagnostics.txt"
    rawPath = "data/rawDiagnostics.txt"
    saveRaw = False

    def clearFile(self):
        os.remove(self.path)

    def putAppend(self,data):
        with open(self.path,"a") as f:
            f.write(str(data)+"\n")

    def putAppendRaw(self,data):
        with open(self.rawPath,data) as f:
            f.write(str(data)+"\n")

    class count:
        def __init__(self):
            self.startTime = time.monotonic()

        def getDuration(self):
            return time.monotonic() - self.startTime
        
        def putCount(self,name = "", roundD = 3):
            newTime = time.monotonic()
            diagnostic.putAppend(diagnostic,name+str(round(newTime - self.startTime,roundD)))

            if diagnostic.saveRaw:
                with open(diagnostic.rawPath,"w") as f:
                    f.write(name+str(newTime - self.startTime) + "\n")

        def replaceCount(self,name,newName = "",roundD = 3): 
            newTime = time.monotonic()

            if diagnostic.saveRaw:
                with open(diagnostic.rawPath,"a") as f:
                    f.write(newName+str(newTime - self.startTime) + "\n")

            if os.path.exists(diagnostic.path):
                with open(diagnostic.path,"r") as f:
                    raw = f.read()
                    fileData = raw.split("\n")
            else:
                with open(diagnostic.path,"w") as f:
                    f.write(newName+str(round(newTime - self.startTime,roundD)) + "\n")
                return

            if name in raw:
                outData = ""
                for line in fileData:
                    if name in line:
                        outData = outData + newName+str(round(newTime - self.startTime,roundD)) + "\n"
                    elif line == "":
                        continue
                    else:
                        outData = outData + line + "\n"
                with open(diagnostic.path,"w") as f:
                    f.write(outData)
            else:
                with open(diagnostic.path,"a") as f:
                    f.write(newName+str(round(newTime - self.startTime,roundD)) + "\n")
                return