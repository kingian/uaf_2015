from server_control import *

sct = ServerControl()

sct.camConResponse('pi9:register')
sct.camConResponse('pi8:register')
sct.camConResponse('pi6:register')
print(sct.listControllers())
sct.stopFlag = True
sct.camConResponse('pi9:paused')
sct.camConResponse('pi8:paused')
sct.camConResponse('pi6:paused')
print(sct.listControllers())
sct.camConResponse('pi9:compressed')
sct.camConResponse('pi8:compressed')
sct.camConResponse('pi6:compressed')
print(sct.listControllers())
sct.camConResponse('pi9:sent')
sct.camConResponse('pi8:sent')
sct.camConResponse('pi6:sent')