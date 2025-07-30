from aiogram.dispatcher.filters.state import State,StatesGroup


class addchannel(StatesGroup):
    name = State()    
    username = State()    
    channelid = State()

class detelechannel(StatesGroup):
    channelid = State()        

class addmoviestate(StatesGroup):
    Video = State()          
    VideoName = State()    
    VideoCaption = State()    
    FilmCode = State()    
    Trailer = State()         
    TrailerVideo = State()    



# class addmoviestate(StatesGroup):
#     Video = State()          
#     VideoCaption = State()    
#     Trailer = State()         
#     TrailerVideo = State()    


# class addserialstate(StatesGroup):
#     Video = State()
#     SerialPart = State()
#     VideoCaption = State()
#     Trailer = State()
#     TrailerVideo = State()
#     Confirm = State()
class addserialstate(StatesGroup):
    ChooseOption = State()  # Yangi yoki eski serial tanlash
    ExistingSerial = State()  # Eski serial uchun SerialNumber kiritish
    Video = State()
    SerialPart = State()
    VideoCaption = State()
    Trailer = State()
    TrailerVideo = State()
    Confirm = State()

class detelemovie(StatesGroup):
    moviecode = State()    


class deteleserial(StatesGroup):
    NumberOrPart = State()    
    serialNumber = State()    
    serialPart = State()    

class reklama(StatesGroup):
    videoandcaption = State()     
    description = State()          


class AdminAddState(StatesGroup):
    admin_id = State()

class AdminRemoveState(StatesGroup):
    admin_id = State()
