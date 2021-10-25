from models import Session , User, Playlist,Song
session = Session()

user1 = User(id= 1, username= 'oceaneyes' , password=  '1234abc' ,email= 'abc.@gmail.com')
song1 = Song(id= 1, name= '7 rings', singer= 'Ariana Grande',album= 'thank u,next ',duration= '3.05')
song2 = Song(id= 2, name= 'unstoppable', singer= 'Sia',album= 'This is acting ',duration= '3.41')
song3 = Song(id= 3, name='Cono', singer='Jason Derulo', album='Cono', duration='1.57')
song4 = Song(id= 4, name='Time', singer='NF', album='Paralyzed', duration='3.43')
playlist1 = Playlist(id= 1, title= 'Morning' , user = user1, private =True , songs= [song1,song2])
playlist2 = Playlist(id= 2, title= 'Workout' , user= user1, private =True , songs= [song2,song3,song4])


session.add(user1)
session.add(song1)
session.add(song2)
session.add(song3)
session.add(song4)
session.add(playlist1)
session.add(playlist2)
session.commit()

print(session.query(Playlist).all())
print(session.query(User).all())
print(session.query(Song).all())
session.close()
